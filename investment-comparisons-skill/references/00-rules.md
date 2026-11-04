# Standing rules for the whole job (investment-comparisons-skill)

**What this is.** This skill builds a client-facing comparison of two or more providers' quotes for the SAME product type: RA against RA, Tax-Free (TFSA) against TFSA, endowment against endowment, living annuity against living annuity, never across product types. Examples: Old Mutual against Sanlam, Sanlam against Momentum, Old Mutual against Allan Gray. The output is one HTML email for Paul Kafentzis (FSP45946), built by a program in a fixed structure of four short tables, saved as a no-logo copy in the client's Comparative Quotes folder, put into an **unsent Outlook draft** (To the client, Cc Sitamah Nathoo) and flagged to Sitamah on Teams so she attaches the quotes and fund fact sheets and **emails the client**. **Claude never sends the client email.**

**What this is not.** Not for life or risk cover (that is `life-insurer-comparison`), and not for a single provider's proposal (that is `om-optimal-ra-proposal`, `om-tax-free-skill` or `rgar-skill`). The signature belongs to `paul-email-signature`.

**Core principle: actual cost, not EAC.** Every comparison breaks the fees into their real percentage line items. EAC (Effective Annual Cost) is never the headline cost figure: it blends several different fee types into one number and hides which line is driving the cost. If a quote only shows EAC and not the underlying fee breakdown, flag it to Paul and ask for the fee schedule or fund fact sheet that shows the components: never back-calculate or estimate a breakdown from an EAC figure.

**Core principle: plain English, not adviser jargon.** The document is written for the client to read and understand. Industry shorthand (TER, TIC, EAC, "as-and-when commission", "payment layer", "fund-based fee") is replaced by a plain description or explained in brackets where it appears. A short intro line sits above each table saying what it shows and why it matters. Fee rows are labelled by what they are for. Numbers stay exact; the words around them are short and simple. A mechanism that is not clear from one sentence (see the loyalty benefits) gets its own plain explanation before the numbers.

**Who does what.** A program drives the job one step at a time, checks every figure you enter against the quotes' and fact sheets' own text, adds up the totals, compares the quotes, builds the email from the fixed template and checks what comes back from Outlook and Teams. You (Claude) find the documents, fetch the fund fact sheets and save their text, read everything page by page, type the answers with their sources, ask Paul only what the documents cannot tell you, do the Outlook and Teams steps and run the programs as they are. You never rewrite or "fix" a program, the template or the HTML during a run.

**Rules that apply to every step**
1. Say the version line first, in exactly the words the program gives. Run the steps in order; none is skipped.
2. Source first, never invent. Write only what is in the client's own documents, the saved fund fact sheets or Paul's own words (recorded with the words). "It seems implied", "it is usual" and "it would make sense" are not sources. If a line is unclear, garbled or ambiguous, flag it to Paul instead of turning it into a fact. If sources disagree, STOP and ask Paul, quoting both values and where each came from.
3. Read before you write: the program serves the pages one at a time; read each fully before you acknowledge it (scanned or image pages must be looked at as images). Searching for keywords is not reading. Fees, funds and figures always come from THIS client's quotes and fact sheets, never from a previous client's comparison.
4. Check before you claim: never say a file is saved, a draft made or a message sent until the program's proof says so. Say what was checked and what is only attested.
5. Nothing is sent without Paul's yes. His one yes (at the confirmation table) covers building, saving, the Outlook draft and the Teams message to Sitamah; the message goes only after the draft has been read back and checked. Claude never sends the client email.
6. Never overwrite a file in the client's folder without Paul's clear yes in this chat.
7. Never lower the standard: a correction, a frustrated user, a short request or a "quick" task relaxes no rule here.
8. A correction from Paul re-opens the task: fix the answer, run answers and check and show again (his earlier yes no longer counts), rebuild, and repeat the save, the draft and the message for everything that changed.
9. If a rule cannot be met, stop and say exactly which and why. Never hand over partial work as complete.
10. No client data is ever kept in the skill. Skill changes are made only in Claude Code and uploaded as a zip; never say a change is live until Paul confirms.

**Fixed:** the email is from Paul Kafentzis (FSP45946), the Cc is always Sitamah Nathoo (admin@liferisk.co.za), the importance is High.

**Words Paul uses for this job:** "compare these quotes", "investment comparison for [Name]", "Old Mutual vs Sanlam", or two or more providers' investment quotes being weighed against each other.
