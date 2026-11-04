"""Invented documents and plans for the one test of the prospect-review-funnel-at-knowledge. Nothing here is a real client or a real document: the lines are made up
in the style of the funnel documents (Mr John Snow is the invented AdviceTech test client)."""
import datetime as dt
import zipfile

STREAMLINED = [
    "WR Prospect & Review Pipeline Templates - STREAMLINED (invented test copy)",
    "A6d Acceptance (PK): the application, the DOC date, the COC date and the RAR answer are completed with the client.",
    "G5b Sub-tasks Running (SR): Sitamah keeps the main Task open while the sub-tasks run and ticks when every sub-task has ended.",
    "A12 Compliance Audit (SR): the audit items are ticked and the signed ROA or SROA is saved to the client's folder.",
    "G2 Prospect Call (PK): Paul phones the prospect for a short intro call and confirms the meeting.",
]
MASTER_PLAN_ROWS = [
    ["MA32", "Acceptance (Personal Cover - New Business)", "PK – Complete the application with the client"],
    ["MP35", "SR – Monitor progress on all open sub-tasks", "Done opens the Family monitor modules"],
    ["MA66", "SR – Signed ROA saved to the client's Fact Find folder", "Sub-task finished"],
    ["MP1", "PK – Prospect proceeds, meeting still on?", "No opens the not-proceeding question"],
]
REGISTER_ROWS = [["233", "MP35", "G5b", "SR – Monitor progress on all open sub-tasks", "Done"], ["234", "MA32", "A6d", "PK – QUESTION: SERVICING CASE?", "Done"]]
LOGIC_FLOW = "# Logic & Flow (invented test copy)\n\nG5b is the monitor stage: Sitamah follows each sub-task and ticks when every sub-task has ended.\n"
FLOW_PAGE = "<html><body><h1>Flow comparison (invented test copy)</h1><p>G5b Sub-tasks Running leads to G6 Review Monitor and Close.</p></body></html>"

EV = {  # lines quoted exactly as written in the invented documents
    ("A6d", "streamlined"): "the application, the DOC date, the COC date and the RAR answer are completed with the client",
    ("A6d", "master_plan"): "PK – Complete the application with the client",
    ("G5b", "streamlined"): "Sitamah keeps the main Task open while the sub-tasks run",
    ("G5b", "master_plan"): "SR – Monitor progress on all open sub-tasks",
    ("A12", "streamlined"): "the audit items are ticked and the signed ROA or SROA is saved",
    ("A12", "master_plan"): "SR – Signed ROA saved to the client's Fact Find folder",
}


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_docx(path, paragraphs, table_rows=None):
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    body = "".join('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % _esc(p) for p in paragraphs)
    if table_rows:
        body += "<w:tbl>" + "".join("<w:tr>" + "".join('<w:tc><w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p></w:tc>' % _esc(c) for c in row) + "</w:tr>" for row in table_rows) + "</w:tbl>"
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document %s><w:body>%s</w:body></w:document>' % (ns, body)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/xml"/></Types>')
        z.writestr("word/document.xml", xml)


def make_xlsx(path, rows):
    strings, cells = [], []
    for r, row in enumerate(rows, 1):
        cs = []
        for c, v in enumerate(row):
            strings.append(v)
            cs.append('<c r="%s%d" t="s"><v>%d</v></c>' % ("ABCDEFG"[c], r, len(strings) - 1))
        cells.append('<row r="%d">%s</row>' % (r, "".join(cs)))
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("xl/sharedStrings.xml", '<?xml version="1.0"?><sst %s>%s</sst>' % (ns, "".join("<si><t>%s</t></si>" % _esc(s) for s in strings)))
        z.writestr("xl/worksheets/sheet1.xml", '<?xml version="1.0"?><worksheet %s><sheetData>%s</sheetData></worksheet>' % (ns, "".join(cells)))


def write_docs(d):
    import os
    paths = {"streamlined": os.path.join(d, "STREAMLINED.docx"), "master_plan": os.path.join(d, "MASTER PLAN.docx"), "register": os.path.join(d, "REGISTER.xlsx"),
             "logic_flow": os.path.join(d, "Logic.md"), "flow_comparison": os.path.join(d, "Flow.html")}
    make_docx(paths["streamlined"], STREAMLINED)
    make_docx(paths["master_plan"], ["AT MASTER PLAN (invented test copy)"], MASTER_PLAN_ROWS)
    make_xlsx(paths["register"], REGISTER_ROWS)
    with open(paths["logic_flow"], "w", encoding="utf-8") as f:
        f.write(LOGIC_FLOW)
    with open(paths["flow_comparison"], "w", encoding="utf-8") as f:
        f.write(FLOW_PAGE)
    return paths


def plan():
    return {"decision": "Decision 56 – invented test change", "paul_request": "Please add the monitor line to G5b and the servicing question to A6d", "stages": ["A6d", "G5b"],
            "documents": [{"role": "streamlined", "change": "wording of the G5b monitor line"}, {"role": "master_plan", "change": "the MP35 table and the MA32 table"},
                          {"role": "register", "change": "rows 233 and 234"}],
            "objects": [
                {"type": "checklist", "id": 233, "title": "MP35 – G5b monitor", "stage": "G5b", "expect_lines": 3,
                 "lines": [{"text": "SR – Monitor progress on all open sub-tasks", "kind": "action"}, {"text": "SR – Update Task Notes for this stage", "kind": "action"},
                           {"text": "SR – AUTOMATION: MOVE THE TASK TO COLUMN \"G6\" — TICK DONE TO OPEN BELOW", "kind": "automation"}]},
                {"type": "checklist", "id": 234, "title": "MA32 – Acceptance", "stage": "A6d", "expect_lines": 6,
                 "lines": [{"text": "ACCEPTANCE", "kind": "subheading"}, {"text": "PK – QUESTION: SERVICING CASE? — TICK DONE = YES / SKIP = NO", "kind": "question"},
                           {"text": "PK – Client happy to sign LOA MSIGN – YES / NO?", "kind": "yesno"}, {"text": "PK – Proof of Tax Number — Received", "kind": "received"},
                           {"text": "PK – Replacement policy details — if applicable", "kind": "applicable"}, {"text": "ACCEPTED", "kind": "outcome"}]},
                {"type": "section", "id": 104, "title": "G5b — Sub-tasks Running (SR)", "stage": "G5b"}],
            "next": "the Family A starters"}


def now_iso(plus_minutes=0):
    return (dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(minutes=plus_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
