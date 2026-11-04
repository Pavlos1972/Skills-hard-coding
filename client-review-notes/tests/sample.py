"""INVENTED raw notes and records for the client-review-notes test (Pat Samplecase, Robin Testcase, the invented insurers Samplelife, Testco and
Samplecover, example.invalid). IDs are computed here, never typed as digits. No real client, ever."""


def make_id(prefix12, ok=True):
    tot = 0
    for i, ch in enumerate(prefix12):
        x = int(ch)
        if i % 2:
            x = x * 2
            x = x - 9 if x > 9 else x
        tot += x
    chk = (10 - tot % 10) % 10
    if not ok:
        chk = (chk + 1) % 10
    return prefix12 + str(chk)


PAT_ID = make_id("800101" + "5009" + "08")
URL = "https://planner.cloud.microsoft/webui/task/AbC123"


def raw_notes():
    return "\n".join([
        "Pat Samplecase",
        "Full name: Pat Samplecase",
        "Last name: Samplecase",
        "First name: Pat",
        "Known as: Patty",
        "Categories: Client / BrightRock Lead",
        "First meeting: 12/03/2018",
        "First policy signed: 02/04/2018",
        "Portfolio Review Month: March",
        "Got details from: Referral from Robin Testcase",
        "Client ID No: " + PAT_ID,
        "Income Tax Number: 1234567890",
        "Adviser Allocation: Paul",
        "Medical Aid: Samplecover, contract 5500123, premium R 3 200.00",
        "Short Term Insurance: not brokers yet",
        "Family: Robin Testcase (son), also a client, cell 082 555 0100",
        "Previous: Contract: SL-123456 (Samplelife Risk Cover) DOC 01/06/2015 / R 950.00 / REPLACED",
        "Current: Contract: BR-778899 (BrightRock Personal Covers) DOC 02/04/2018 / R 1 000.00 / IN FORCE",
        "Lapsed: Contract: 4455667 (Testco Endowment) DOC 15/09/2012 / R 500.00 / LAPSED",
        "Commission: BrightRock – Personal Covers (March '20)",
        "1st year comm: R 5 500.00",
        "",
        "14/02/2022 10:15 Paul: Client asked which OM products (RA 123456789, Tax-Free 987654321) to withdraw R70k from. Paul advised on options; client deciding. Called Alwyn Van Tonder.",
        "MARCH 2024 Old Mutual AML reminder REF 5566778 completed. Do not contact the client by phone before 10:00.",
        "05/11/2026 08:00 Planner task " + URL + " created for the review; LOA sent to 4455667.",
    ]) + "\n"


def record():
    return {
        "fields": {
            "Full Name": "Pat Samplecase", "Last Name": "Samplecase", "First Name": "Pat", "Known As": "Patty", "Categories": "Client / BrightRock Lead",
            "First meeting": "12/03/2018", "First policy signed": "02/04/2018", "Portfolio Review Month": "March", "Got details from": "Referral from Robin Testcase",
            "Client ID No": PAT_ID, "Income Tax Number": "1234567890", "Adviser Allocation": "Paul",
            "Medical Aid": "Samplecover, contract 5500123, premium R 3 200.00",
            "Short Term Insurance": "Contract: Not recorded / not brokers yet.",
            "Family Information": ["Robin Testcase (son), also a client, cell 082 555 0100"],
            "Life & Investments": {
                "previous": [{"contract": "SL-123456", "product": "Samplelife Risk Cover", "doc": "01/06/2015", "premium": "R 950.00", "status": "REPLACED"}],
                "current": [{"contract": "BR-778899", "product": "BrightRock Personal Covers", "doc": "02/04/2018", "premium": "R 1 000.00", "status": "IN FORCE"}],
                "inactive": [{"contract": "4455667", "product": "Testco Endowment", "doc": "15/09/2012", "premium": "R 500.00", "status": "LAPSED"}]},
            "Commission": [{"title": "BrightRock – Personal Covers (March '20)", "lines": ["1st year comm: R 5 500.00"]}],
        },
        "notes": {"blocks": [
            {"from": [1], "bullets": ["Client asked which OM products (RA 123456789, Tax-Free 987654321) to withdraw R70k from; Paul advised on options; client deciding which to use. Called Alwyn Van Tonder."]},
            {"from": [2], "bullets": ["Old Mutual AML reminder REF 5566778 completed.", "Do not contact the client by phone before 10:00."]},
            {"from": [3], "bullets": ["Review task created: [Planner – Review task](%s). LOA sent to 4455667." % URL]},
        ]},
    }
