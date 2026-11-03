#!/usr/bin/env python3
"""
WR ROA Builder — construction script.

Takes the pristine ROA_Template_2026.docx and a structured data dict and produces
a finished, client-ready ROA .docx matching the real delivered format (verified
against a real delivered ROA), not the raw template look.

Usage (as a library):
    from build_roa import build_roa
    build_roa('ROA_Template_2026.docx', 'output.docx', data)

See references/roa_data_schema.md in the skill for the full `data` shape.
"""
import copy
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from lxml import etree

W_URI = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_URI}
W = '{%s}' % W_URI

NOT_CONSIDERED = "This need was not considered in this Review meeting."
INCOME_AFTER_24_FIXED = "This need has been worked into the client's Lump Sum Disability Cover Benefit."
DECLINED_NEED = "The client did not want to consider this need at this time."

# Section descriptors: heading substring used to locate each section robustly,
# whether its amount fields are single (lump sum only) or dual (lump/monthly),
# and any hardcoded Need Identified override.
SECTIONS = [
    dict(key='death', heading='Death Planning - Status', amount_type='single',
         need_override='Life Cover'),
    dict(key='disability', heading='Lump Sum Disability Planning', amount_type='single'),
    dict(key='income_1st24', heading='Sickness Benefit OR Income Protector Planning',
         amount_type='dual'),
    dict(key='income_after24', heading='Income Protector Planning After 24 Months',
         amount_type='dual'),
    dict(key='dread', heading='Dread Disease Planning', amount_type='single',
         need_override='Comprehensive Severe Illness'),
    dict(key='retirement', heading='Retirement Planning', amount_type='dual',
         merged_table=True, need_override='Retirement Planning',
         remove_amount_rows=True),
    dict(key='investment', heading='Investment Planning', amount_type='dual',
         remove_amount_rows=True),
]


def _q(text):
    return f'{W}{text}'


def find_body_children(root):
    body = root.find('w:body', NS)
    return body, list(body)


def find_heading_index(children, substring):
    for i, el in enumerate(children):
        if el.tag == _q('p'):
            text = ''.join(el.itertext())
            if substring in text:
                return i
    raise ValueError(f"Heading containing {substring!r} not found")


def get_all_sdts(el):
    return el.findall('.//w:sdt', NS)


def sdt_alias(sdt):
    pr = sdt.find('w:sdtPr', NS)
    if pr is None:
        return None
    alias = pr.find('w:alias', NS)
    return alias.get(_q('val')) if alias is not None else None


PPR_ORDER = [
    'pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widowControl',
    'numPr', 'suppressLineNumbers', 'pBdr', 'shd', 'tabs', 'suppressAutoHyphens',
    'kinsoku', 'wordWrap', 'overflowPunct', 'topLinePunct', 'autoSpaceDE',
    'autoSpaceDN', 'bidi', 'adjustRightInd', 'snapToGrid', 'spacing', 'ind',
    'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection',
    'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr',
    'sectPr', 'pPrChange',
]
TCMAR_ORDER = ['top', 'left', 'bottom', 'right']


def insert_ordered(parent, tagname, order_list):
    """Insert a new child element into parent at the schema-correct position,
    given the canonical child order for that parent type. Returns the new element."""
    idx_new = order_list.index(tagname)
    insert_pos = len(parent)
    for i, child in enumerate(parent):
        local = etree.QName(child).localname
        if local in order_list and order_list.index(local) > idx_new:
            insert_pos = i
            break
    el = etree.Element(_q(tagname))
    parent.insert(insert_pos, el)
    return el


def force_left_align(p):
    """Force explicit left alignment on a paragraph, overriding any inherited
    justify/center — filled-in content should never appear centered or justified."""
    if p is None:
        return
    pPr = p.find('w:pPr', NS)
    if pPr is None:
        pPr = etree.Element(_q('pPr'))
        p.insert(0, pPr)
    jc = pPr.find('w:jc', NS)
    if jc is None:
        jc = insert_ordered(pPr, 'jc', PPR_ORDER)
    jc.set(_q('val'), 'left')


def set_sdt_plain_text(sdt, new_text, strip_databinding=False):
    """Replace the visible content of a plaintext/dropdown/date SDT with new_text,
    using a single run so we never end up with split/duplicated runs."""
    pr = sdt.find('w:sdtPr', NS)
    if strip_databinding and pr is not None:
        db = pr.find('w:dataBinding', NS)
        if db is not None:
            pr.remove(db)
    # Remove "showing placeholder" flag so Word renders it as real content, not grey hint text
    if pr is not None:
        plc = pr.find('w:showingPlcHdr', NS)
        if plc is not None:
            pr.remove(plc)
    content = sdt.find('w:sdtContent', NS)
    if content is None:
        return
    # Find an existing run to copy formatting (rPr) from, then wipe all children and
    # rebuild with exactly one run containing new_text.
    existing_runs = content.findall('.//w:r', NS)
    rpr = None
    if existing_runs:
        rpr_el = existing_runs[0].find('w:rPr', NS)
        if rpr_el is not None:
            rpr = copy.deepcopy(rpr_el)
            # Strip the "PlaceholderText" character style (grey #808080) — real
            # content should render in normal black text, not placeholder-grey.
            rstyle = rpr.find('w:rStyle', NS)
            if rstyle is not None and rstyle.get(_q('val')) == 'PlaceholderText':
                rpr.remove(rstyle)
    for child in list(content):
        content.remove(child)
    r = etree.SubElement(content, _q('r'))
    if rpr is not None:
        r.append(rpr)
    t = etree.SubElement(r, _q('t'))
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = new_text
    # Find the containing paragraph (may be several levels up if wrapped in
    # bookmarks etc.) and force left alignment.
    parent = sdt.getparent()
    while parent is not None and parent.tag != _q('p'):
        parent = parent.getparent()
    force_left_align(parent)


def set_cell_reason_text(tbl, row_index, text):
    """Set the plain paragraph text of a single-cell reason-box table row, with
    comfortable cell padding (the raw template has none, making text look
    squashed against the borders)."""
    rows = tbl.findall('.//w:tr', NS)
    row = rows[row_index]
    tc = row.find('w:tc', NS)
    tcPr = tc.find('w:tcPr', NS)
    if tcPr is None:
        tcPr = etree.SubElement(tc, _q('tcPr'))
        tc.insert(0, tcPr)
    if tcPr.find('w:tcMar', NS) is None:
        tcMar = etree.SubElement(tcPr, _q('tcMar'))
        for side in TCMAR_ORDER:
            m = etree.SubElement(tcMar, _q(side))
            m.set(_q('w'), '120')
            m.set(_q('type'), 'dxa')
    p = tc.find('w:p', NS)
    # wipe existing runs/sdt in this paragraph, keep pPr
    for child in list(p):
        if child.tag != _q('pPr'):
            p.remove(child)
    r = etree.SubElement(p, _q('r'))
    t = etree.SubElement(r, _q('t'))
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    force_left_align(p)


def remove_element(el):
    parent = el.getparent()
    if parent is not None:
        parent.remove(el)


def remove_table_row(tbl, row_index):
    rows = tbl.findall('.//w:tr', NS)
    remove_element(rows[row_index])


def format_amount(value, amount_type, is_monthly=False):
    """value: number or None. amount_type: 'single' or 'dual'.
    For dual fields collapse to a single clean 'R x,xxx monthly' or 'R x,xxx' string —
    never leave the unused lump/monthly scaffolding in place."""
    if value is None:
        return ""
    formatted = f"R {value:,.0f}"
    if amount_type == 'dual' and is_monthly:
        formatted += " monthly"
    return formatted


def fill_data_table_row(tbl, row_index, value_text):
    rows = tbl.findall('.//w:tr', NS)
    row = rows[row_index]
    tcs = row.findall('w:tc', NS)
    value_tc = tcs[1]
    p = value_tc.find('w:p', NS)
    for child in list(p):
        if child.tag != _q('pPr'):
            p.remove(child)
    r = etree.SubElement(p, _q('r'))
    t = etree.SubElement(r, _q('t'))
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = value_text
    force_left_align(p)


def strip_tab_runs(p):
    """Remove any direct-child run in this paragraph that is a bare <w:tab/>, and
    strip a purely-whitespace leading run — the template has these baked in before
    several dropdowns (2 tabs before Insurers Considered/Recommended Insurer, 1 tab
    or a stray space before most Recommendation for Identified Need fields), which
    pushes the filled-in text away from the left edge using default tab stops. Once
    a value is filled in, these serve no purpose."""
    if p is None:
        return
    children_list = list(p)
    for idx, child in enumerate(children_list):
        if etree.QName(child).localname != 'r':
            continue
        has_tab = child.find('w:tab', NS) is not None
        t = child.find('w:t', NS)
        is_pure_whitespace_leading = (
            idx <= 1 and t is not None and t.text is not None and t.text.strip() == ''
        )
        if has_tab or is_pure_whitespace_leading:
            p.remove(child)


def fill_insurer_dropdowns(tbl, row_index, insurers):
    """insurers: list of up to 3 strings for 'Insurers Considered' row, or a single
    string for 'Recommended Insurer' row. Unused slots are left visually blank
    (not 'Choose an item.')."""
    rows = tbl.findall('.//w:tr', NS)
    row = rows[row_index]
    sdts = get_all_sdts(row)
    for i, sdt in enumerate(sdts):
        val = insurers[i] if i < len(insurers) else ""
        set_sdt_plain_text(sdt, val)
    # strip leading/trailing tab runs from the value cell's paragraph(s) now that
    # real content has been set
    tcs = row.findall('w:tc', NS)
    if len(tcs) > 1:
        for p in tcs[1].findall('w:p', NS):
            strip_tab_runs(p)


def remove_table_rows(tbl, indices):
    """Remove multiple rows from a table by index, safely regardless of order."""
    rows = tbl.findall('.//w:tr', NS)
    for i in sorted(indices, reverse=True):
        remove_element(rows[i])


def build_section(children, section, data, active):
    idx = find_heading_index(children, section['heading'])
    heading_p = children[idx]

    if section.get('merged_table'):
        # Retirement: data table (3 rows) at idx+1, reason heading somewhere after,
        # then a merged table (row0=reason, rows1-3=insurers/recinsurer/recommendation)
        data_tbl = children[idx + 1]
        # find the reason heading and merged table after it
        reason_head_idx = None
        for j in range(idx + 2, min(idx + 8, len(children))):
            if children[j].tag == _q('p') and 'Reason this product suits' in ''.join(children[j].itertext()):
                reason_head_idx = j
                break
        merged_tbl = children[reason_head_idx + 1]

        # KNOWN RECURRING BUG (must be re-verified before every Retirement build):
        # the raw template physically places the Reason row BEFORE the insurer rows
        # in this merged table (row0=reason, rows1-3=insurers/recinsurer/recommendation).
        # Move the reason row to the end so the fill order matches s9(1)(c)/(b) intent:
        # 0=insurers considered, 1=recommended insurer, 2=recommended product, 3=reason.
        mrows = merged_tbl.findall('.//w:tr', NS)
        if len(mrows) == 4:
            reason_row = mrows[0]
            parent = reason_row.getparent()
            parent.remove(reason_row)
            parent.append(reason_row)

        # Status dropdown lives in heading_p
        status_sdt = get_all_sdts(heading_p)[0]

        if not active:
            set_sdt_plain_text(status_sdt, "DO NOT REVIEW")
            remove_element(data_tbl)
            # strip insurer/recinsurer/recommendation rows (0,1,2), keep row 3 (reason)
            rows = merged_tbl.findall('.//w:tr', NS)
            for r in rows[:3][::-1]:
                remove_element(r)
            set_cell_reason_text(merged_tbl, 0, data.get('reason_text', NOT_CONSIDERED))
            return

        set_sdt_plain_text(status_sdt, data.get('status', 'IMPORTANT'))
        need_val = section.get('need_override', data.get('need_identified', ''))
        fill_data_table_row(data_tbl, 0, need_val)
        if section.get('remove_amount_rows'):
            # Recommended/Taken Up Amount aren't relevant for Retirement — remove
            # both rows entirely rather than leaving them blank or "N/A"
            remove_table_rows(data_tbl, [1, 2])
        else:
            rec_amt = format_amount(data.get('recommended_amount'), 'dual', data.get('is_monthly', False))
            taken_amt = format_amount(data.get('taken_up_amount'), 'dual', data.get('is_monthly', False))
            fill_data_table_row(data_tbl, 1, rec_amt)
            fill_data_table_row(data_tbl, 2, taken_amt)
        fill_insurer_dropdowns(merged_tbl, 0, data.get('insurers_considered', []))
        fill_insurer_dropdowns(merged_tbl, 1, [data.get('recommended_insurer', '')])
        fill_insurer_dropdowns(merged_tbl, 2, [data.get('recommended_product', '')])
        set_cell_reason_text(merged_tbl, 3, data.get('reason_text', ''))
        return

    # Standard section layout: heading -> data table (6 rows) -> ... -> reason heading -> reason table (1 row)
    data_tbl = children[idx + 1]
    reason_head_idx = None
    for j in range(idx + 2, min(idx + 8, len(children))):
        if children[j].tag == _q('p') and 'Reason this product suits' in ''.join(children[j].itertext()):
            reason_head_idx = j
            break
    reason_tbl = children[reason_head_idx + 1]

    status_sdt = get_all_sdts(heading_p)[0]

    if not active:
        set_sdt_plain_text(status_sdt, "DO NOT REVIEW")
        remove_element(data_tbl)
        default_reason = NOT_CONSIDERED
        if section['key'] == 'income_after24':
            default_reason = INCOME_AFTER_24_FIXED
        set_cell_reason_text(reason_tbl, 0, data.get('reason_text', default_reason))
        return

    set_sdt_plain_text(status_sdt, data.get('status', 'IMPORTANT'))
    need_val = section.get('need_override', data.get('need_identified', ''))
    fill_data_table_row(data_tbl, 0, need_val)
    amt_type = section['amount_type']
    rec_amt = format_amount(data.get('recommended_amount'), amt_type, data.get('is_monthly', False))
    taken_amt = format_amount(data.get('taken_up_amount'), amt_type, data.get('is_monthly', False))
    fill_data_table_row(data_tbl, 1, rec_amt)
    fill_data_table_row(data_tbl, 2, taken_amt)
    fill_insurer_dropdowns(data_tbl, 3, data.get('insurers_considered', []))
    fill_insurer_dropdowns(data_tbl, 4, [data.get('recommended_insurer', '')])
    fill_insurer_dropdowns(data_tbl, 5, [data.get('recommended_product', '')])
    if section.get('remove_amount_rows'):
        # Recommended/Taken Up Amount aren't relevant for Investment — remove both
        # rows entirely now that the insurer rows (filled by original index above)
        # are safely in place
        remove_table_rows(data_tbl, [1, 2])
    set_cell_reason_text(reason_tbl, 0, data.get('reason_text', ''))


INSURER_FILENAME_SHORT = {
    'BRIGHTROCK': 'BR',
}


def build_filename(insurer, cover_scope, premium, roa_date, client_name):
    """Build the required delivery filename:
    'ROA - [Insurer] [Personal/Business] Cover - R [premium] p.m. - [DD.MM.YY] - ([Client Name])'
    - insurer: as stored in the dropdown (e.g. 'BRIGHTROCK', 'OLD MUTUAL') — mapped to
      title case for the filename, except BrightRock which is always shortened to 'BR'.
    - cover_scope: 'Personal' or 'Business'
    - premium: number (e.g. 4097.96) — formatted with no thousands comma, 2 decimals
    - roa_date: 'YYYY-MM-DD' — reformatted to DD.MM.YY
    - client_name: full client name
    """
    insurer_upper = insurer.strip().upper()
    if insurer_upper in INSURER_FILENAME_SHORT:
        insurer_display = INSURER_FILENAME_SHORT[insurer_upper]
    else:
        insurer_display = insurer.strip().title()
    premium_str = f"R {premium:,.2f}".replace(',', '')
    dt = datetime.strptime(roa_date, '%Y-%m-%d')
    date_str = dt.strftime('%d.%m.%y')
    return f"ROA - {insurer_display} {cover_scope} Cover - {premium_str} p.m. - {date_str} - ({client_name})"


def build_roa(template_path, output_path, data):
    """
    data keys:
      bundle: 'risk' | 'retirement' | 'investment'
      client_name, client_id (13 digits no spaces), roa_date (YYYY-MM-DD),
      roa_reference_no, risk_profile,
      policy_replacement: bool,
      sections: dict keyed by section key -> section data dict, only needed for
                sections in the active bundle (see build_section for shape)
    """
    workdir = Path(tempfile.mkdtemp(prefix='roa_build_'))      # always a fresh temporary folder, never a fixed path
    subprocess.run(['unzip', '-o', str(template_path), '-d', str(workdir)],
                    check=True, capture_output=True)

    doc_path = workdir / 'word' / 'document.xml'
    tree = etree.parse(str(doc_path))
    root = tree.getroot()
    body, children = find_body_children(root)

    # --- Client Name (appears twice: greeting block + confirmation block) ---
    name_sdts = [s for s in get_all_sdts(body) if sdt_alias(s) == 'Client Name']
    for s in name_sdts:
        set_sdt_plain_text(s, data['client_name'], strip_databinding=True)

    # --- ROA Reference Number (appears at top; the "Your ROA reference number is X"
    # sentence near the bottom is a plain-text mail-merge field on the same binding,
    # already covered by stripping+resetting all matching SDTs) ---
    ref_sdts = [s for s in get_all_sdts(body) if sdt_alias(s) == 'ROA Reference Number']
    for s in ref_sdts:
        set_sdt_plain_text(s, data['roa_reference_no'], strip_databinding=True)

    # --- Client ID confirmation line: "I, (Name) [Comments]    (ID)  hereby confirm"
    # -> "I, [Client Name], (ID: <13 digits>), hereby confirm". Handled as
    # precise run-level edits (not a blind substring replace) to avoid stray commas
    # or leftover double spaces. ---
    id_idx = find_heading_index(children, '(ID)')
    id_p = children[id_idx]
    literal_runs = [r for r in id_p.findall('w:r', NS) if r.find('w:t', NS) is not None]
    for r in literal_runs:
        t = r.find('w:t', NS)
        if t.text and '(Name) ' in t.text:
            t.text = t.text.replace('(Name) ', '')
        elif t.text and '(ID)' in t.text:
            rest = t.text.lstrip()  # drop leading run of spaces before "(ID)"
            rest = rest.replace('(ID)', f"(ID: {data['client_id']}),")
            rest = re.sub(r'\s+hereby', ' hereby', rest)
            t.text = rest
        elif t.text is not None and t.text.strip() == '' and t is not literal_runs[-1].find('w:t', NS):
            # the lone spacer run between the Name SDT and the "(ID)" run —
            # replace with ", " so the name is followed by exactly one comma+space
            t.text = ', '

    # --- Health Care is never produced as an ROA: remove the section entirely
    # (heading + reason table + surrounding spacer paragraphs), not just left inactive ---
    hc_idx = find_heading_index(children, 'Health Care Planning - Status')
    hc_heading = children[hc_idx]
    # collect heading, reason-heading paragraph, reason table, and trailing spacer
    # paragraphs up to (not including) the next real heading ("POLICY REPLACEMENT")
    to_remove = [hc_heading]
    j = hc_idx + 1
    while j < len(children) and 'POLICY REPLACEMENT' not in ''.join(children[j].itertext()):
        to_remove.append(children[j])
        j += 1
    for el in to_remove:
        remove_element(el)

    # --- Risk Profile dropdown ---
    risk_idx = find_heading_index(children, 'RISK PROFILE')
    # the dropdown sits in the paragraph right after the RISK PROFILE heading
    for j in range(risk_idx, risk_idx + 3):
        sdts = get_all_sdts(children[j])
        if sdts:
            set_sdt_plain_text(sdts[0], data['risk_profile'])
            break

    # --- Top Date field (native date picker) ---
    date_idx = find_heading_index(children, 'Date: ')
    date_sdt = get_all_sdts(children[date_idx])[0]
    set_sdt_plain_text(date_sdt, data['roa_date'])

    # --- Bundle sections ---
    # income_after24 is NEVER actively completed, even within the risk bundle — BR's
    # Income Protection only ever covers the first 24 months; permanence beyond that
    # is always folded into Lump Sum Disability instead (see INCOME_AFTER_24_FIXED).
    bundle_map = {
        'risk': {'death', 'disability', 'income_1st24', 'dread'},
        'retirement': {'retirement'},
        'investment': {'investment'},
    }
    active_keys = bundle_map[data['bundle']]
    for section in SECTIONS:
        # re-derive children list each time since prior edits may have removed elements
        body, children = find_body_children(root)
        sect_data = data.get('sections', {}).get(section['key'], {})
        # A cover type can be in the active bundle but still declined by the client —
        # treat it the same as an inactive section (table removed, "Do not Review"),
        # but it must carry its own explicit reason (no generic "not considered in
        # this Review meeting" default, since the need WAS considered and declined).
        declined = sect_data.get('declined', False)
        if declined and 'reason_text' not in sect_data:
            raise ValueError(
                f"Section '{section['key']}' is marked declined but has no "
                f"reason_text — a declined need must carry an explicit reason, "
                f"asked for directly rather than defaulted."
            )
        active = (section['key'] in active_keys) and not declined
        build_section(children, section, sect_data, active)

    # --- Policy Replacement ---
    body, children = find_body_children(root)
    pr_idx = find_heading_index(children, 'The product recommended will')
    pr_p = children[pr_idx]
    pr_sdt = get_all_sdts(pr_p)[0]
    set_sdt_plain_text(pr_sdt, 'replace' if data.get('policy_replacement') else 'not replace')

    # --- RAR reference number: removed entirely, every time (there is no reference
    # number on the RAR). Strip the trailing "RAR reference number: [field]" phrase
    # from its sentence, keeping the rest of the s9(1)(d)/Rule 19 explanation intact. ---
    rar_idx = find_heading_index(children, 'RAR reference number')
    rar_p = children[rar_idx]
    for r in rar_p.findall('w:r', NS):
        t = r.find('w:t', NS)
        if t is not None and t.text and 'RAR reference number:' in t.text:
            t.text = t.text.split('RAR reference number:')[0].rstrip()
    for s in get_all_sdts(rar_p):
        if sdt_alias(s) == 'rarreference':
            remove_element(s)

    # --- Next meeting date = ROA date + 12 months ---
    roa_dt = datetime.strptime(data['roa_date'], '%Y-%m-%d')
    try:
        next_dt = roa_dt.replace(year=roa_dt.year + 1)
    except ValueError:
        next_dt = roa_dt + timedelta(days=365)
    next_date_str = next_dt.strftime('%Y-%m-%d')
    next_idx = find_heading_index(children, 'Our next meeting to review')
    next_p = children[next_idx]
    next_sdt = get_all_sdts(next_p)[0]
    set_sdt_plain_text(next_sdt, next_date_str)

    # --- Advisor's bottom signature date: no fillable control exists here (it's
    # blank literal text after "Date:"), so append the ROA date directly onto that
    # run. Always auto-filled with the ROA date, per standing instruction. ---
    body, children = find_body_children(root)
    sig_idx = find_heading_index(children, 'Signature:')
    sig_p = children[sig_idx]
    for r in sig_p.findall('.//w:r', NS):
        t = r.find('w:t', NS)
        if t is not None and t.text and t.text.strip().endswith('Date:'):
            t.text = t.text + ' ' + data['roa_date']
            break

    # --- The entire client decision block — "I hereby accept...", "My final
    # decision is as follows:-", "I decline ... reasons:" and its blank input
    # lines — must stay together on one page. Chain keepNext/keepLines through
    # every paragraph from "I hereby accept" up to (not including) "CLIENT:
    # SIGNATORIES" so no page break can fall inside this block. ---
    accept_idx = find_heading_index(children, 'I hereby accept the advice')
    sig_heading_idx = find_heading_index(children, 'CLIENT: SIGNATORIES')
    for j in range(accept_idx, sig_heading_idx):
        p = children[j]
        pPr = p.find('w:pPr', NS)
        if pPr is None:
            pPr = etree.Element(_q('pPr'))
            p.insert(0, pPr)
        if pPr.find('w:keepNext', NS) is None:
            insert_ordered(pPr, 'keepNext', PPR_ORDER)
        if pPr.find('w:keepLines', NS) is None:
            insert_ordered(pPr, 'keepLines', PPR_ORDER)

    # --- Author / Financial Planner dropdown (fixed) ---
    author_candidates = [s for s in get_all_sdts(body) if sdt_alias(s) in ('Author', 'author', 'Financial Planner')]
    for s in author_candidates:
        set_sdt_plain_text(s, 'PAUL KAFENTZIS')

    # --- Trim the run of empty trailing paragraphs before the final sectPr. The
    # template ships with ~11 blank paragraphs after the signature line, which is
    # enough to push out an extra, entirely blank final page. Keep a couple for
    # visual breathing room and drop the rest — this only removes empty paragraphs,
    # nothing with content is touched. ---
    body, children = find_body_children(root)
    KEEP_TRAILING_BLANKS = 2
    trailing_blank_idxs = []
    for el in reversed(children):
        if el.tag == _q('sectPr'):
            continue
        if el.tag == _q('p') and ''.join(el.itertext()).strip() == '':
            trailing_blank_idxs.append(el)
            continue
        break
    for el in trailing_blank_idxs[KEEP_TRAILING_BLANKS:]:
        remove_element(el)

    tree.write(str(doc_path), xml_declaration=True, encoding='UTF-8', standalone=True)

    # rezip
    out = Path(output_path).resolve()
    if out.exists():
        out.unlink()
    subprocess.run(['zip', '-Xr', str(out), '.'], cwd=str(workdir), check=True, capture_output=True)
    shutil.rmtree(workdir, ignore_errors=True)
    return str(out)


if __name__ == '__main__':
    import json
    if len(sys.argv) != 4:
        print("Usage: build_roa.py <template.docx> <data.json> <output.docx>")
        sys.exit(1)
    with open(sys.argv[2]) as f:
        data = json.load(f)
    result = build_roa(sys.argv[1], sys.argv[3], data)
    print(f"Built: {result}")
