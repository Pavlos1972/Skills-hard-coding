These rules apply from the first message to the last. The program shows the right page at each step, so you do not work from memory of them.

1. **Source first - never invent.** Write only what is in the Astute report, what Paul told you, or what the insurer's own current public product information says. Every client figure (cover amount, premium, dates, policy number, fund values) comes from the report itself; research confirms product names, structure and terms only. If something is unclear, flag it. "It seems implied" is not a source.
2. **The deliverable is always a PDF**, never chat text alone. The program draws it; you never write drawing code and never edit the PDF.
3. **Never write a figure that is not in the report.** A figure that is unclear or absent is left empty and flagged, not guessed. The program refuses what it cannot find in the report's text.
4. **Cession status is not in Astute's data:** never state that a policy is or is not ceded. The cession note is always in the General Verification Notes, and a policy held with a bank's insurance arm is flagged for direct verification with the insurer.
5. **Contradictions in the report** (for example a package marked Active whose underlying policies are Inactive) are flagged in the document, never silently resolved.
6. **Missing or zero values** returned by a provider are flagged as absent data needing verification, not treated as real zeros. An unknown product type is flagged prominently, never assumed.
7. **Only policies Astute labels paid-up go in Section 3.** A policy with zero values but no paid-up label is flagged, not declared paid-up. Surrendered, lapsed and other inactive policies go in Additional Notes.
8. **A provider that returned no row at all is not proof of no cover:** say so in the flag.
9. **Every benefit carries a stand-alone or accelerated label** (or "unable", when the report does not allow it) **and every policy a premium pattern.**
10. **Never touch another broker's folder** under `Company - WR Clients`. This skill does not draw the Astute report (Sitamah does) and does not analyse policies (`life-policy-schedule-analyzer`).
11. **Check before you claim.** Never say the summary is saved until the folder was listed and the size matched. Say what you checked.
12. **The programs run as they are.** Never rewrite one during a run, and never type the file name, a total or the content.
13. **Every correction re-opens the whole task.** Fix the data, run the later steps again; the program re-opens them. If a rule cannot be met, stop and say so; never hand over partial work as complete.
14. **The reply** is the saved file's name and folder, the numbered flag list (most important first), the PDF in the chat, then the SHORT AUDIT (Paul, 03/11/2026): one line per check with a green tick or a red cross, one closing line for what is only attested. Never a long printout. Nothing is sent to anyone. Never say a skill change is live before Paul confirms.
