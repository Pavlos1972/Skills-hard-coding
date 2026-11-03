#!/usr/bin/env python3
"""Insert the accepted-proposal email pages (as images) into the Investment
section of a built ROA, per Step 4 of the wr-roa-builder skill: standalone
bordered picture paragraphs after the section's data/reason table, never
inside a table cell.
"""
import shutil
import subprocess
import sys
import os
from lxml import etree

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}
W = '{%s}' % NS['w']


def qn(tag):
    return '{%s}%s' % (NS['w'], tag)


def build_image_paragraphs(rid, cx, cy, page_num, total_pages):
    """Return (picture_paragraph_xml, caption_paragraph_xml) as lxml elements."""
    pic_xml = f'''<w:p xmlns:w="{NS['w']}">
  <w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="120" w:after="40"/><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing xmlns:wp="{NS['wp']}">
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{900 + page_num}" name="Proposal Email Page {page_num}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="Proposal Email Page {page_num}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rid}" xmlns:r="{NS['r']}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{cx}" cy="{cy}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                <a:ln w="9525">
                  <a:solidFill><a:srgbClr val="808080"/></a:solidFill>
                </a:ln>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''
    cap_xml = f'''<w:p xmlns:w="{NS['w']}">
  <w:pPr><w:spacing w:after="200"/><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:rPr><w:i/><w:sz w:val="18"/><w:color w:val="595959"/></w:rPr>
    <w:t>page {page_num} of {total_pages}</w:t>
  </w:r>
</w:p>'''
    return etree.fromstring(pic_xml.encode()), etree.fromstring(cap_xml.encode())


def embed(src_docx, images_dir, out_docx, insert_before_heading='POLICY REPLACEMENT'):
    """Embed the page images (JPEG files in images_dir, in name order) into the ROA. insert_before_heading is the heading of the section that
    follows the active bundle's own section: 'Investment Planning' for a Retirement ROA, 'POLICY REPLACEMENT' for an Investment ROA."""
    src_docx = os.path.abspath(src_docx)
    images_dir = os.path.abspath(images_dir)
    out_docx = os.path.abspath(out_docx)
    import tempfile
    work = tempfile.mkdtemp(prefix='embed_work_')
    subprocess.run(['unzip', '-q', '-o', src_docx, '-d', work], check=True)

    image_files = sorted(
        f for f in os.listdir(images_dir) if f.lower().endswith('.jpg')
    )
    total_pages = len(image_files)
    assert total_pages > 0, "no images found"

    media_dir = os.path.join(work, 'word', 'media')
    rels_path = os.path.join(work, 'word', '_rels', 'document.xml.rels')
    ct_path = os.path.join(work, '[Content_Types].xml')
    doc_path = os.path.join(work, 'word', 'document.xml')

    # 1. Copy images into word/media with distinct names
    new_names = []
    for i, fname in enumerate(image_files, start=1):
        new_name = f'image_email{i}.jpg'
        shutil.copy(os.path.join(images_dir, fname), os.path.join(media_dir, new_name))
        new_names.append(new_name)

    # 2. Add relationships
    rels_tree = etree.parse(rels_path)
    rels_root = rels_tree.getroot()
    RELS_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'
    existing_ids = [
        int(r.get('Id')[3:]) for r in rels_root
        if r.get('Id', '').startswith('rId') and r.get('Id')[3:].isdigit()
    ]
    next_id = max(existing_ids) + 1
    rids = []
    for new_name in new_names:
        rid = f'rId{next_id}'
        next_id += 1
        rel = etree.SubElement(rels_root, '{%s}Relationship' % RELS_NS)
        rel.set('Id', rid)
        rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
        rel.set('Target', f'media/{new_name}')
        rids.append(rid)
    rels_tree.write(rels_path, xml_declaration=True, encoding='UTF-8', standalone=True)

    # 3. Ensure jpg content type default exists
    ct_tree = etree.parse(ct_path)
    ct_root = ct_tree.getroot()
    CT_NS = 'http://schemas.openxmlformats.org/package/2006/content-types'
    has_jpg = any(
        el.tag == '{%s}Default' % CT_NS and el.get('Extension', '').lower() == 'jpg'
        for el in ct_root
    )
    if not has_jpg:
        default = etree.Element('{%s}Default' % CT_NS)
        default.set('Extension', 'jpg')
        default.set('ContentType', 'image/jpeg')
        ct_root.insert(0, default)
        ct_tree.write(ct_path, xml_declaration=True, encoding='UTF-8', standalone=True)

    # 4. Insert paragraphs into document.xml right after Investment's reason table,
    #    before the "POLICY REPLACEMENT" heading.
    doc_tree = etree.parse(doc_path)
    root = doc_tree.getroot()
    body = root.find('w:body', NS)
    children = list(body)

    def heading_idx(substr):
        for i, el in enumerate(children):
            if el.tag == qn('p') and substr in ''.join(el.itertext()):
                return i
        raise ValueError(f'heading {substr!r} not found')

    # Optional 4th CLI arg: the heading of the section that immediately follows
    # the active bundle's own section in document order. Images are inserted
    # right before that heading, i.e. right after the active section's own
    # reason table. Defaults to "POLICY REPLACEMENT" for Investment bundles
    # (Investment is the last active section before that block). Retirement
    # bundles MUST pass "Investment Planning" here, since Retirement's section
    # is immediately followed by the (inactive) Investment section, not by
    # POLICY REPLACEMENT directly.
    pr_idx = heading_idx(insert_before_heading)
    insert_before = children[pr_idx]

    # Target width per skill: <=5,000,000 EMU wide.
    cx = 5000000
    from PIL import Image
    new_elems = []
    for i, (new_name, rid) in enumerate(zip(new_names, rids), start=1):
        im = Image.open(os.path.join(images_dir, image_files[i - 1]))
        w_px, h_px = im.size
        cy = int(cx * (h_px / w_px))
        pic_p, cap_p = build_image_paragraphs(rid, cx, cy, i, total_pages)
        new_elems.append(pic_p)
        new_elems.append(cap_p)

    for el in new_elems:
        insert_before.addprevious(el)

    doc_tree.write(doc_path, xml_declaration=True, encoding='UTF-8', standalone=True)

    # 5. Rezip
    if os.path.exists(out_docx):
        os.remove(out_docx)
    subprocess.run(
        ['zip', '-X', '-r', out_docx, '.'],
        cwd=work, check=True, stdout=subprocess.DEVNULL,
    )
    shutil.rmtree(work, ignore_errors=True)
    return out_docx


def main():
    if len(sys.argv) < 4:
        print("Usage: embed_email_images.py <built.docx> <images_dir> <out.docx> [heading to insert before]")
        sys.exit(1)
    print('Wrote', embed(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else 'POLICY REPLACEMENT'))


if __name__ == '__main__':
    main()
