#!/usr/bin/env python3
"""Makes the two fixed email templates of om-optimal-ra-proposal from Paul's two live templates (14/10/2026 build), once, for the record.

  python3 make_templates.py <folder with the two old templates> <assets folder to write into>

Every change is listed in CHANGES-FOR-PAUL.md. Each replacement must hit exactly the number of times stated, so a changed source stops the script.
No client data is in either template (checked by lint). The old files are never changed.
"""
import os
import re
import sys

MAIN_IN, LUMP_IN = "OM_Optimal_RA_Proposal_TEMPLATE.html", "OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html"
MAIN_OUT, LUMP_OUT = "OM_Optimal_RA_Proposal_TEMPLATE.html", "OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html"


def rep(t, old, new, n=1):
    c = t.count(old)
    if c != n:
        raise SystemExit("the source has %d x %r, expected %d" % (c, old[:90], n))
    return t.replace(old, new)


def rx(t, pattern, new, flags=re.S):
    ms = list(re.finditer(pattern, t, flags))
    if len(ms) != 1:
        raise SystemExit("the source has %d x pattern %r, expected 1" % (len(ms), pattern[:90]))
    m = ms[0]
    return t[:m.start()] + m.expand(new) + t[m.end():]


def common(t):
    t = rep(t, "[CC EMAIL]", "[CC NAME(S)]")
    t = rep(t, "<!-- OPENING -->", "<!-- BODY START -->\n<!-- OPENING -->")
    t = rep(t, "<p style=\"font-size:12pt;margin:0;\">Kind regards,</p>", "<!-- BODY END -->\n<p style=\"font-size:12pt;margin:0;\">Kind regards,</p>")
    t = rx(t, r"<p style=\"margin:0;\"><img src=\"data:image/png;base64,[A-Za-z0-9+/=]+\" width=\"260\" alt=\"Wealth Revolution\"></p>",
           "<!-- LOGO START -->" + re.search(r"<p style=\"margin:0;\"><img src=\"data:image/png;base64,[A-Za-z0-9+/=]+\" width=\"260\" alt=\"Wealth Revolution\"></p>", t).group(0) + "<!-- LOGO END -->")
    return t


def main_template(t):
    t = common(t)
    t = rep(t, "[CLIENT FULL NAME] / Old Mutual Retirement Annuity Proposal &#8211; R [PREMIUM] p.m.", "[SUBJECT]")
    t = rep(t, "<strong>[DAY], [DD/MM/YYYY],</strong> herewith", "<strong>[MEETING DATES LIST]</strong>, herewith")
    # the stale wording Paul's skill told the chat to override by hand on every run (found 01/10/2026)
    t = rep(t, "You will be working [EMPLOYER NAME] in the position of [POSITION].", "You are working at [EMPLOYER NAME] in the position of [POSITION].")
    # existing retirement annuities: the rows are built by the program (one per policy); with none the whole table is replaced by one sentence
    t = rx(t, r"(<table width=\"100%\" cellpadding=\"5\" cellspacing=\"0\" border=\"1\" bordercolor=\"#dddddd\" style=\"border-collapse:collapse;font-size:12pt;\">\s*<tr>\s*<td style=\"font-weight:bold;padding:5px 10px;background:#f5f5f5;\">Insurer</td>.*?</tr>)\s*<tr>\s*<td style=\"padding:5px 10px;\">\[INSURER NAME\]</td>.*?</tr>\s*</table>",
           "<!-- RA TABLE START -->\n\\1\n[RA_ROWS]</table>\n<!-- RA TABLE END -->")
    t = rep(t, "<!-- RA TABLE START -->\n", "<!-- RA TABLE START -->\n", 1)
    # the 'what you can save' sentence: six scenario sentences chosen by the program ([TOTAL CAP MONTHLY]), not the stale static one
    t = rx(t, r"<p style=\"font-size:12pt;margin:0;\">Based on your current earnings, you can personally save a sum of <strong>R \[MAXIMUM RA CONTRIBUTION\]</strong>.*?</p>", "[SAVE SENTENCE]")
    # the RGAR paragraph, or the sentence that none was requested
    t = rx(t, r"<p style=\"font-size:12pt;margin:0;\">According to the Retirement Goal Analysis Report that was sent to you.*?</p>", "[RGAR PARAGRAPH]")
    # Table 1: fund rows + the existing retirement annuities (or one dash row), and the fund's own tax-saved row (Pension or Provident label)
    t = rx(t, r"\[T1_FUND_ROWS\]<tr><td bgcolor=\"#c8e6c9\" style=\"padding:4px 8px;font-size:10pt;\">Monthly Retirement Annuity Contribution</td>.*?</tr>", "[T1_FUND_ROWS][T1_RA_ROWS]")
    fund_row = re.search(r"<tr><td bgcolor=\"#ffffff\"[^>]*>Tax Saved from Pension Fund Deduction</td>.*?</tr>", t, re.S).group(0)
    new_row = fund_row.replace("Tax Saved from Pension Fund Deduction", "[FUND TAX LABEL]").replace("[TAX SAVED PENSION]", "[TAX SAVED FUND]")
    t = rep(t, fund_row, "<!-- FUND TAX START -->" + new_row + "<!-- FUND TAX END -->")
    # Tables 2 and 3 never had a place for the fund's rows (the rule says they appear in all three tables)
    t = rep(t, "[T2_RA_ROWS]", "[T2_FUND_ROWS][T2_RA_ROWS]")
    t = rep(t, "[T3_RA_ROWS]", "[T3_FUND_ROWS][T3_RA_ROWS]")
    # the orange messages under Tables 1 and 3: the program picks 'you can still use X%' or 'you have maximised'
    t = rep(t, "You can still use [T1 PCT REMAINING]% of your allowable deductions. If you increase your contributions to your retirement annuity you will be able to increase your tax savings.", "[T1 MESSAGE]")
    t = rep(t, "You can still use [T3 PCT REMAINING]% of your allowable deductions. If you increase your contributions to your retirement annuity you will be able to increase your tax savings.", "[T3 MESSAGE]")
    # funds: any number of funds (the old template had room for exactly two)
    t = rx(t, r"The funds that are recommended is the <strong>\[FUND NAME 1\] &amp; the \[FUND NAME 2\]</strong> \(See attached\)\.", "[FUNDS SENTENCE]")
    t = rx(t, r"<tr><td style=\"font-size:10pt;padding:4px 12px 4px 24px;\">&#8211; \[FUND NAME 1\]</td>.*?</tr>\s*<tr><td style=\"font-size:10pt;padding:4px 12px 4px 24px;\">&#8211; \[FUND NAME 2\]</td>.*?</tr>", "[FUND_ROWS]")
    t = rep(t, "([FUND NAME 1] &amp; [FUND NAME 2])", "([FUND NAMES LIST])")
    # fees that were typed into the template: each is read from the quote every time
    t = rep(t, ">3.05%</td>", ">[NET ADMIN FEE]%</td>")
    t = rep(t, ">0.575%</td>", ">[ADVICE FEE]%</td>")
    t = rep(t, ">0.00%</td>", ">[ADVISER CHARGE]%</td>")
    return t


def lump_template(t):
    t = common(t)
    t = rep(t, "[CLIENT FULL NAME] / Old Mutual Retirement Annuity &#8211; Lump Sum Investment (R [LUMP SUM AMOUNT])", "[SUBJECT]")
    t = rep(t, "<strong>[DAY], [DD/MM/YYYY],</strong> herewith", "<strong>[MEETING DATES LIST]</strong>, herewith")
    t = rep(t, "<p style=\"font-size:12pt;margin:0;\">[LS_TAX_TREATMENT_NOTE]</p>", "[LS_TAX_TREATMENT_NOTE]")
    return t


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    for fin, fout, fn in ((MAIN_IN, MAIN_OUT, main_template), (LUMP_IN, LUMP_OUT, lump_template)):
        with open(os.path.join(src, fin), encoding="utf-8") as f:
            t = fn(f.read())
        with open(os.path.join(dst, fout), "w", encoding="utf-8", newline="") as f:
            f.write(t)
        print("wrote", fout, len(t), "bytes")


if __name__ == "__main__":
    main()
