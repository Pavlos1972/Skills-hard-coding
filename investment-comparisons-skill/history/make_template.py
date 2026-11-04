#!/usr/bin/env python3
"""Makes assets/Investment_Comparison_Email_TEMPLATE.html once, for the record.

  python3 make_template.py <the OM Optimal RA proposal template> <assets folder to write into>

The header block, the closing lines and Paul's signature block with the logo are taken unchanged from the OM Optimal RA proposal template (the same email conventions);
the body is new: the four tables of the old skill's Step 7 with one intro line each, in the fixed order. The tables themselves are built by the program from the data file.
No client data is in the template (checked by lint).
"""
import os
import sys

SP = lambda n: '<table width="100%%" cellpadding="0" cellspacing="0" border="0"><tr><td height="%d" style="font-size:1px;line-height:%dpx;">&nbsp;</td></tr></table>\n' % (n, n)
P = '<p style="font-size:12pt;margin:0;">%s</p>\n'
H = '<p style="font-size:12pt;font-weight:bold;margin:0;">%s</p>\n'
BODY = ("<!-- BODY START -->\n"
        + P % "Dear [CLIENT FIRST NAME]," + SP(8)
        + P % "Following our Teams Meeting on <strong>[MEETING DATES LIST]</strong>, herewith please find a comparison of the [PRODUCT NAME] quotes from [PROVIDERS LIST]:" + SP(16)
        + "[THINGS TO KNOW]"
        + H % "[TABLE1 TITLE]" + SP(6) + P % "[TABLE1 INTRO]" + SP(8) + "[TABLE1]" + SP(16)
        + H % "Total Ongoing Fees &#8211; Per Annum (Excluding EAC)" + SP(6) + P % "[TABLE2 INTRO]" + SP(8) + "[TABLE2]" + "[FEE NOTES]" + SP(16)
        + H % "Investment Fund Comparison" + SP(6) + P % "[TABLE3 INTRO]" + SP(8) + "[TABLE3]" + "[FUND NOTES]" + SP(16)
        + H % "Loyalty and Value-Add Benefits" + SP(6) + P % "[TABLE4 INTRO]" + SP(8) + "[LOYALTY EXPLANATIONS]" + "[TABLE4]" + SP(16)
        + "[EXTRAS]"
        + P % "Hoping that above is in order." + SP(12)
        + P % "[NEXT MEETING LINE]" + SP(12))


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        t = f.read()
    head, rest = t.split("<!-- BODY START -->", 1)
    tail = "<!-- BODY END -->" + rest.split("<!-- BODY END -->", 1)[1]
    head = head.replace("<title>OM Optimal RA Proposal</title>", "<title>Investment Comparison</title>")
    assert "[SUBJECT]" in head and "[CC NAME(S)]" in head and "<!-- LOGO START -->" in tail
    out = head + BODY + tail
    with open(os.path.join(sys.argv[2], "Investment_Comparison_Email_TEMPLATE.html"), "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print("wrote the template,", len(out), "bytes")


if __name__ == "__main__":
    main()
