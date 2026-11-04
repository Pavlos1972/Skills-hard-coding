INVENTORY of the old skill: 365 sentences
  kept (word for word or nearly): 126
  reworded, with a recorded change: 164
  dropped, with a recorded decision: 75
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 59: Insurers and the FSCA don't accept a lookalike PDF — they accept *their* form, filled in.
    now: Insurers and the FSCA accept THEIR form, filled in.
    why: Kept; the program fills the real blank form and refuses one that changed.
- old line 59: Open the firm's real AcroForm template (bundled in assets/), write values into its real named fields, and hand back that same PDF — never a recreation.
    now: The program writes values into the real named fields of the blank form in assets/ and hands back that same PDF.
    why: Kept; the program fills the real blank form and refuses one that changed.
- old line 59: save it into the client's OneDrive folder on Paul's machine instead (Step 6).
    now: save it into the client's folder by the routes (page 05).
    why: Kept; the program fills the real blank form and refuses one that changed.
- old line 61: ## How this skill is used (the application life-cycle)
    now: Find this skill's folder (the "Base directory" shown when the skill loaded;
    why: The life-cycle is now two run modes, prefill and correct.
- old line 63: Before a follow-up meeting where the client may accept a quote (Life, RA, Invest, Risk), this skill pre-fills the applications (Steps 1–6) and saves them in the Applications folder of the correct tran
    now: A client's folder can hold several transaction folders, and an older unnamed folder (<Surname, Firstname>\<Surname, Firstname>\, with archived applications) as well as the current transaction folder.
    why: The life-cycle is now two run modes, prefill and correct.
- old line 64: In the meeting, once the client accepts, Paul completes the same application form live with the client and saves it over the pre-filled one, so there is ONE copy per application.
    now: "Fills in the real Old Mutual and General Short Risk application forms for a client, and corrects completed applications after a meeting, for Paul Kafentzis (FSP45946).
    why: The life-cycle is now two run modes, prefill and correct.
- old line 64: Paul's live-typed form is the accurate record.
    now: A form Paul completed live is never overwritten without a fresh yes.
    why: The life-cycle is now two run modes, prefill and correct.
- old line 65: After the meeting, client-teams-transcript-skill reads the applications, reports the differences, and calls this skill in Correction / Sync mode (Step 7).
    now: client-teams-transcript-skill reports differences in WORDS only (it never writes ID or account numbers), so the new values come from Paul's live-completed application, which is the accurate record;
    why: The life-cycle is now two run modes, prefill and correct.
- old line 67: ## Step 1 — Work out which application(s) are needed
    now: """One short block per application (Paul's rule 7.7):
    why: Kept; the plan file holds one entry per application.
- old line 69: From the proposal, RGAR, fact find, or the client's own instruction, identify each product/transaction that needs its own application:
    now: The files sent in the chat and saved in the client's Applications folder after Paul's one yes, the transaction folder renamed only when planned and approved, each checked in a saved listing.
    why: Kept; the plan file holds one entry per application.
- old line 71: one OM Application Template fill per product *and* per contribution type — a recurring RA and a lump-sum Section 14 transfer into the same plan are two separate applications.
    now: one per product AND per contribution type (a recurring RA and a lump sum Section 14 transfer into the same plan are two).
    why: Kept; the plan file holds one entry per application.
- old line 72: a short-term/risk product (with OM or any other insurer) uses the General Short Risk Application Template instead — see references/field-mappings.md §2.
    now: "Fills in the real Old Mutual and General Short Risk application forms for a client, and corrects completed applications after a meeting, for Paul Kafentzis (FSP45946).
    why: Kept; the plan file holds one entry per application.
- old line 72: if the layout ever stops matching the documented mapping, flag it back and re-derive the mapping.
    now: "If it refuses, put every listed problem right in the file and run it again.
    why: Kept; the plan file holds one entry per application.
- old line 74: ## Step 2 — Gather the client's bio data once
    now: "sent in the chat and saved in the client's Applications folder after Paul's yes;
    why: The bio data are entered once as fields with sources; 'CRM record' is dropped (Paul agreed, 04/11/2026).
- old line 76: Every OM application for the same client shares one set of personal/bio fields (full list in references/field-mappings.md §1).
    now: "Fills in the real Old Mutual and General Short Risk application forms for a client, and corrects completed applications after a meeting, for Paul Kafentzis (FSP45946).
    why: The bio data are entered once as fields with sources; 'CRM record' is dropped (Paul agreed, 04/11/2026).
- old line 76: Pull these once from the client's Fact Find, prior applications, or CRM record, and reuse the same dict across every product sheet for that client.
    now: option = one of the form's own products, type = Recurring, Lump Sum or Section 14 transfer, and for a product the program does not know short and short_paul_said;
    why: The bio data are entered once as fields with sources; 'CRM record' is dropped (Paul agreed, 04/11/2026).
- old line 78: (This is the initial pre-fill before a meeting.
    now: *The documents (a pre-fill).
    why: The bio data are entered once as fields with sources; 'CRM record' is dropped (Paul agreed, 04/11/2026).
- old line 78: The stricter "current application only" source rule in Step 7.3 applies to Correction / Sync mode, not to this step.)
    now: the program does not read the text it draws" % ("blank form" if mode == "prefill" else "application before the correction") if okap and not pbad else
    why: The bio data are entered once as fields with sources; 'CRM record' is dropped (Paul agreed, 04/11/2026).
- old line 80: ## Step 3 — Get the transaction-specific fields right
    now: fields = app.get("fields") or {}
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 82: *Product name always carries the amount.
    now: Product is the form's own product plus the amount:
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 82: Build the Product value as "<base product> - R <amount> p.m." for recurring, or "<base product> - R <amount>" for a lump sum — e.g.
    now: return None if a is None else (money_r(a) + " p.m." if kind_of(app) == "recurring" else money_r(a) + " - Lump Sum")
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 82: "OM Tax Free recurring - R 1,000 p.m.", "OM RA - Lump Sum - R 100,000.00".
    now: "OM Optimal RA – Recurring - R 2,800 p.m.")
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 82: Product is a closed dropdown, so add the new value first with add_product_option().
    now: Product is a closed dropdown (/Opt array), not free text, and per the
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 84: *Every application needs a real answer on replacement, not a guess.
    now: replacement needs a real answer, Yes or No (never a guess)" % tag)
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 85: If it genuinely isn't a replacement, set IsReplacement = No and ReplacedPolicyNumbers = N/A.
    now: if g("IsReplacement") == "No" and g("ReplacedPolicyNumbers") != "N/A":
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 86: If it is a replacement, find the actual insurer name and policy number being replaced — search the client's proposal comparison documents, fact find, RGAR, or the policy schedule itself.
    now: a replacement needs the insurer and policy number of each replaced policy" % tag)
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 86: Write it as "<Insurer>, Policy No.
    now: A replacement is written <Insurer>, Policy No.
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 86: Check the policy number against the schedule document, not an older draft (an earlier Brightrock draft once had the replaced Outsurance policy number typed with a digit missing).
    now: the number is checked against the policy schedule document, not an older draft (or Paul's words)" % (tag, i))
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 89: *Foreign tax number follows foreign tax obligation.
    now: Foreign tax number follows foreign tax obligation (No gives N/A).
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 89: When ForeignTaxObligation = No, ForeignTaxNumber = N/A.
    now: if g("ForeignTaxObligation") == "No" and g("ForeignTaxNumber") != "N/A":
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 91: *Any field with an N/A option that doesn't apply gets N/A, not blank.
    now: Any field with an N/A option that does not apply gets N/A, not blank (a Single, Divorced, Widowed or Separated client's marriage contract type is N/A).
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 91: DeferredPremiumFacility for a lump-sum transaction is N/A.
    now: DeferredPremiumFacility is N/A for a lump sum.
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 93: OriginateFrom is only filled when OwnKnowledge = No;
    now: OriginateFrom is filled only when OwnKnowledge = No, otherwise N/A.
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 95: *Signature date is the meeting date, filled in by the advisor — never left blank.
    now: The signature date is the meeting date, DD/MM/YY, never blank.
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 97: If a field (banking details, ID numbers, beneficiaries, doctor, debit date, address, declarations) isn't in the file and Paul hasn't supplied it, leave it blank and list it plainly in the hand-back me
    now: If a field (banking, ID, beneficiaries, doctor, debit date, address, declarations) is not in the file and Paul has not supplied it, leave it blank:
    why: Every rule is a program check: Product value, replacement, N/A discipline, signature date, never invent.
- old line 99: ## Step 4 — Fill the template
    now: STEP_IDS = ["locate", "plan", "confirm", "fill", "save", "final"]
    why: One way for both forms; the program fills the real form and sets the chosen option so dropdowns draw.
- old line 101: Use scripts/fill_om_form.py for OM (fill_om_application()).
    now: the field value — see scripts/fill_om_form.py's add_product_option() for
    why: One way for both forms; the program fills the real form and sets the chosen option so dropdowns draw.
- old line 101: For the General Short Risk form, write values into the named fields listed in references/field-mappings.md §2 with PdfWriter and auto_regenerate=True so appearances are generated.
    now: The program writes values into the real named fields of the blank form in assets/ and hands back that same PDF.
    why: One way for both forms; the program fills the real form and sets the chosen option so dropdowns draw.
- old line 101: One output PDF per application, never one PDF covering two products.
    now: """One short block per application (Paul's rule 7.7):
    why: One way for both forms; the program fills the real form and sets the chosen option so dropdowns draw.
- old line 103: ## Step 5 — Verify before delivering
    now: nothing is saved before Paul's yes for exactly this version.")
    why: Every field is read back and every filled box is compared with the blank form (Paul agreed, 04/11/2026).
- old line 105: Read back the field values from the saved PDF and compare against what was intended — at minimum Product / INSURER, IsReplacement, ReplacedPolicyNumbers / policy number, ForeignTaxNumber, OriginateFro
    now: Product, SignatureDate, IsReplacement, ReplacedPolicyNumbers and, where they do not apply, ForeignTaxNumber, OriginateFrom, DeferredPremiumFacility, MaritalContractType;
    why: Every field is read back and every filled box is compared with the blank form (Paul agreed, 04/11/2026).
- old line 106: pdftoppm -png -r 100 out.pdf page, then read the PNGs.
    now: "Send each out/*.pdf in the chat, then record:
    why: Every field is read back and every filled box is compared with the blank form (Paul agreed, 04/11/2026).
- old line 106: If a dropdown value (INSURER, COVER LINES, WILL THIS POLICY REPLACE) is set in the field dump but does not appear in the render, that is a viewer/appearance-stream issue, not necessarily a data error:
    now: If a dropdown value is set but does not draw, that is a viewer or appearance issue, not necessarily a data error:
    why: Every field is read back and every filled box is compared with the blank form (Paul agreed, 04/11/2026).
- old line 108: Only proceed to delivery once both checks pass (or the render gap is disclosed as above).
    now: The audit has one line per check with a green tick or a red cross, and one closing line for what is only attested.
    why: Every field is read back and every filled box is compared with the blank form (Paul agreed, 04/11/2026).
- old line 110: ## Step 6 — Where the finished file goes
    now: "Any red cross means the job is not finished:
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 114: Send it in chat with the file-delivery tool so Paul has it in the conversation immediately.
    now: send each file in the chat (the file-delivery tool, so Paul has it at once), and save it into the client's folder by the routes in order (computer, Microsoft 365, Zapier).
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 115: Save it directly into the client's OneDrive folder on Paul's own machine — the reliable path (do not push base64 into SharePoint).
    now: "Save each file into the client's Applications folder through the routes in order (a correction:
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 117: To find the right local folder for a client:
    now: "Find the client's folder and documents, log every try;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 119: sharepoint_folder_search for the client's surname.
    now: In SharePoint, sharepoint_folder_search for the surname:
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 119: The webUrl reveals the advisor's site (/Paul/, /Cameron/, etc.) and the folder path, typically New Business/<Surname, Firstname>/<transaction folder>/Applications.
    now: its web address shows the advisor's site (/Paul/, /Cameron/) and the path.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 119: Some clients have several transaction folders;
    now: "List the transaction folders and each Applications folder.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 119: use the one holding the current quote/proposal documents.
    now: Use the CURRENT transaction folder (the one holding the current quote or proposal documents).
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 120: On Paul's machine the root is C:\Users\Paul\liferisk.co.za\Company - Paul\New Business\ (grant access with device_request_folder_access if not already connected).
    now: Under C:\Users\Paul\liferisk.co.za\Company - Paul\ in New Business\<Surname, Firstname> (a prospect) or WR Clients\<Surname, Firstname> (an existing client):
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 120: The client's top folder can contain an older unnamed folder (<Surname, Firstname>\<Surname, Firstname>\, with archived applications) AND the current transaction folder.
    now: A client's folder can hold several transaction folders, and an older unnamed folder (<Surname, Firstname>\<Surname, Firstname>\, with archived applications) as well as the current transaction folder.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 120: Use the current transaction folder;
    now: Use the CURRENT transaction folder (the one holding the current quote or proposal documents).
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 121: Confirm the Applications subfolder exists with device_list_dir before writing;
    now: Confirm the Applications subfolder exists and list it;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 122: send it in chat first, then device_commit_files with the full Windows path, using the naming convention below.
    now: Send each file in the chat, then save it into the client's folder (step save).")
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 124: once a transaction is chosen (accepted, or the current quote being applied for), rename the current transaction folder to one of these two forms, depending on whether the amount is a monthly premium o
    now: Once a transaction is chosen (accepted, or the current quote being applied for), the current transaction folder is renamed to one of these, built by the program:
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 126: "<Surname, Firstname> - (<Insurer> - <Investment name> - <Type> - R <premium> p.m.)"
    now: monthly premium <Surname, Firstname> - (<Insurer> - <Investment name> - <Type> - R <premium> p.m.);
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 129: Insurer — the abbreviation used on the application (e.g.
    now: The insurer is the abbreviation used on the application (BR Brightrock, OM Old Mutual;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 129: BR for Brightrock, OM for Old Mutual;
    now: multiple insurers (Momentum, Brightrock, Discovery, Old Mutual, Liberty,
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 129: for investment providers the provider name).
    now: CURRENT_DIR = "current"                 # the current applications read for a correction (staged copies)
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 129: Confirm with Paul if it's a new insurer or provider.
    now: a new insurer or product needs Paul's words)" % aid)
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 130: Investment name — the product or fund/portfolio name for RA and investment transactions (e.g.
    now: The investment name (Optimal RA, Tax-Free, Flexi) is for RA and investment transactions;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 130: Optimal RA, Tax-Free, Flexi).
    now: "Optimal RA", "OM Tax Free recurring":
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 130: Life cover has no investment, so omit this segment entirely — life cover uses (<Insurer> - <Type> - R <premium> p.m.).
    now: life cover has no investment, so that segment is omitted ((BR - Personal Covers - R 1,000.00 p.m.)).
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 130: Confirm with Paul when unsure.
    now: R.add(not rbd, "%d transaction folder(s) renamed with mv -n after Paul's yes;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 131: Type — for life/risk cover exactly one of Personal Covers, Buy & Sell, Contingent Liability or Keyman.
    now: The type is, for risk cover, one of Personal Covers, Business Covers, Buy & Sell, Contingent Liability or Keyman;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 131: For RA/investment transactions use the transaction type Paul gives (e.g.
    now: The files sent in the chat and saved in the client's Applications folder after Paul's one yes, the transaction folder renamed only when planned and approved, each checked in a saved listing.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 131: Recurring, Lump Sum, Section 14 transfer) and confirm if it is not obvious.
    now: ["Recurring", "Lump Sum", "Section 14 transfer"],
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 132: Premium / amount — R <premium> p.m.
    now: monthly premium <Surname, Firstname> - (<Insurer> - <Investment name> - <Type> - R <premium> p.m.);
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 132: for a monthly premium, or R <lump sum amount> - Lump Sum for a lump sum being invested, using the figures from the chosen quote.
    now: option = one of the form's own products, type = Recurring, Lump Sum or Section 14 transfer, and for a product the program does not know short and short_paul_said;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 135: Surname, Firstname - (BR - Personal Covers - R 1,000.00 p.m.)
    now: - (First Last).pdf and BR - Personal Covers Application - 20.11.26 - R 1,000.00 p.m.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 136: Surname, Firstname - (OM - Optimal RA - Recurring - R 2,800 p.m.)
    now: "OM Optimal RA – Recurring - R 2,800 p.m.")
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 137: Surname, Firstname - (Ninety One - Flexi - Lump Sum - R 100,000.00 - Lump Sum)
    now: lump sum <Surname, Firstname> - (<Insurer> - <Investment name> - <Type> - R <lump sum amount> - Lump Sum).
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 139: Rename with mv -n inside the connected folder (device_bash), never by overwriting.
    now: Rename with mv -n inside the connected folder, never by overwriting, only with Paul's yes (it is in the table).
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 139: Do not rename the older unnamed folder without asking Paul.
    now: Never rename the older unnamed folder.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 139: Confirm the new path with device_list_dir before writing to it.
    now: Confirm the Applications subfolder exists and list it;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 141: one unified pattern across every application type — the filename must always include the word "Application" directly after the product type.
    now: role must be one of %s (a current application is registered with run.py current)" % ", ".join(r for r in roles if r != "application_current"))
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 143: OR R amount - Lump Sum> - (<Client First Last>).pdf"
    now: OR R amount - Lump Sum> - (<First Last>).pdf, for example OM - Optimal RA Application - 20.11.26 - R 2,800.00 p.m.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 145: Insurer — the abbreviation (e.g.
    now: The insurer is the abbreviation used on the application (BR Brightrock, OM Old Mutual;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 145: OM for Old Mutual, BR for Brightrock);
    now: Momentum / Brightrock / Discovery / Old Mutual / Liberty / Sanlam / Stanlib) |
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 145: confirm with Paul if new.
    now: "If a line is red, tell Paul exactly which one.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 146: Product type — for OM applications the base product name (e.g.
    now: """The product type as the file name needs it:
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 146: Optimal RA, Tax-Free, Flexi);
    now: "Optimal RA", "OM Tax Free recurring":
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 146: for Risk Cover applications the cover line matching the template's selector — Personal Covers, Business Covers, Buy & Sell, Contingent Liability, or Keyman Cover.
    now: The type is, for risk cover, one of Personal Covers, Business Covers, Buy & Sell, Contingent Liability or Keyman;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 147: Date — DD.MM.YY, the application's signature/meeting date.
    now: The date is the signature (meeting) date.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 148: Amount — R <amount> p.m.
    now: <base product> - R 2,800.00 p.m.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 148: for recurring, or R <amount> - Lump Sum for lump sum.
    now: (recurring) or <base product> - R 100,000.00 (lump sum);
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 149: Name — first name then surname inside parentheses.
    now: w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 152: "OM - Optimal RA Application - 27.08.26 - R 1,000 p.m.
    now: "OM Optimal RA – Recurring - R 2,800 p.m.")
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 153: "OM - Optimal RA Application - 27.08.26 - R 100,000.00 - Lump Sum - (Client First Last).pdf"
    now: - (First Last).pdf and BR - Personal Covers Application - 20.11.26 - R 1,000.00 p.m.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 154: "BR - Personal Covers Application - 30.09.26 - R 1,000.00 p.m.
    now: - (First Last).pdf and BR - Personal Covers Application - 20.11.26 - R 1,000.00 p.m.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 156: When a new application replaces an older draft for the same transaction, the older draft is removed only after Paul approves:
    now: *A superseded draft is removed only after Paul approves:
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 156: request delete permission with device_request_delete_permission for the connected root, name the file in the reason, and only then delete it.
    now: To delete, request delete permission for the connected root, name the file in the reason, and only then delete.
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 157: If the write is rejected because the destination file is open in another application, tell Paul plainly and ask him to close it or confirm a different filename — don't force it or silently rename arou
    now: tell Paul and ask him to close it or confirm another name;
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 159: Once saved into the OneDrive folder, it syncs up to SharePoint on its own.
    now: save it into the client's folder by the routes (page 05).
    why: Routes in order with a log; names built by the program; nothing overwritten or deleted without Paul's yes.
- old line 161: ## Step 7 — Correction / Sync mode (after a client meeting)
    now: if w.norm("%s %s" % (oc["first"], oc["surname"])) != w.norm(a.client) or old["mode"] != a.mode:
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 163: Use this mode when client-teams-transcript-skill calls this skill with a list of differences after a follow-up meeting, or when Paul says an application detail has changed.
    now: client-teams-transcript-skill reports differences in WORDS only (it never writes ID or account numbers), so the new values come from Paul's live-completed application, which is the accurate record;
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 163: it never starts from a blank template unless an application for that transaction does not exist yet (then use Steps 1–6).
    now: the program does not read the text it draws" % ("blank form" if mode == "prefill" else "application before the correction") if okap and not pbad else
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 165: the list of corrections (field, new value, which application it came from);
    now: the value of every field of every application, its source, the
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 165: and Paul's carry-across instruction if he gave one.
    now: The inputs are the client, the meeting date, the list of corrections, and Paul's carry-across instruction if he gave one.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 165: Without an instruction, ask (7.4).
    now: a standing instruction from him is followed without asking again.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 167: *7.2 Find every application for the client.
    now: The program prints, for each application:
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: *7.3 Source of truth.
    now: the advisor knows the source of funds"
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: Paul's live-completed application is the accurate record;
    now: A form Paul completed live is never overwritten without a fresh yes.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: the meeting transcript is only a cross-check.
    now: the meeting transcript is only a cross-check (it garbles account numbers, IDs, street names, child names).
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: New values come from that application, not from the garbled transcript (account numbers, IDs, street names, child names).
    now: the meeting transcript is only a cross-check (it garbles account numbers, IDs, street names, child names).
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: When carrying a detail from one application to another, take it ONLY from a current application in a current transaction folder — never from a previous year's application or an older transaction — unl
    now: A correction changes ONLY the planned fields, carries a detail only from a CURRENT application in a CURRENT folder, and stops when two current applications disagree.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: Paul may direct you to the 4.
    now: APPROVAL = "approval.json"              # Paul's yes to the confirmation table
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: FICA & POI folder's Proof of Bank account for banking details;
    now: Text Box 5_4 | ACCOUNT HOLDER (premium-payer's banking details) |
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: if older than 3 months, ask Paul first.
    now: if it is older than 3 months, ask Paul first), fica_address, quote, proposal, policy_schedule.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 169: If two current applications hold different values for the same field, STOP and ask Paul.
    now: If two current applications hold different values for the same detail, the program STOPS:
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 171: *7.4 Build the change plan and ask.
    now: say so plainly, do not claim the render passed, and ask Paul to look in his own viewer.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 171: For each application, list the fields that differ or are blank against the new values (old -> new).
    now: the shipped blank form against the frozen list (path None), or a filled form's fields against it.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 171: Show Paul the plan and ask, per detail, whether to carry it across to all applications, only some, or none.
    now: For a correction, show Paul the change plan (old to new) and ask, per detail, whether to carry it across to all applications, only some, or none;
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 173: Details only carry across where they belong to the same person for that role.
    now: A standing carry-across instruction from Paul is followed without asking again for those details.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 175: *7.5 Apply in place — one copy, overwrite.
    now: lines.append("  corrected in place (one copy);
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 175: Stage the existing file fresh from OneDrive immediately before editing.
    now: Stage each existing file fresh from the folder immediately before editing and note its modified time (receipt stage.<id>.mtime), then register it with run.py current.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 175: Change ONLY the planned fields, leave every other value untouched, and do not touch signature fields.
    now: A correction also proves that only the planned fields changed and the signature fields are untouched.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 175: Save over the same filename in the same Applications folder:
    now: ["names of the files already in the Applications folder"]},
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 175: ONE copy only, nothing deleted.
    now: ONE copy, overwrite, nothing deleted.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 175: Commit with device_commit_files using the expectedMtimeMs from staging so a newer edit by Paul is never overwritten.
    now: probs.append("the file was staged fresh and committed with the same expectedMtimeMs (receipts stage.%s.mtime and commit.%s.expected_mtime, equal) so a newer edit by Paul is never overwritten" % (a.id,
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 175: If the file is locked, tell Paul and ask him to close it.
    now: tell Paul and ask him to close it;
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 177: (a) Field dump before vs after:
    now: a field that was not filled must be empty.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 177: only the planned fields changed;
    now: R.add(okap and not cbad, "Only the planned fields changed in each application;
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 177: (b) visual render of each corrected application (see the Step 5 note on dropdown values);
    now: The insurer is the abbreviation used on the application (BR Brightrock, OM Old Mutual;
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 177: (c) values match the source application.
    now: # ------------------------------------------------------------------ the values of one application
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 179: *7.7 Report back to Paul.
    now: Use correction mode, or record his yes to overwrite (overwrite.paul_said)" % (aid, fn))
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 179: One short block per application:
    now: The hand-back, one short block per application:
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 179: file name, fields changed (old -> new;
    now: the new name must show and the old one must be gone.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 179: mask account and ID numbers to the last 4 digits), fields still blank or needing input, anything skipped and why.
    now: the file name, what was filled (or the fields changed, old to new, with ID and account numbers masked to the last 4), the fields still blank or needing input, any flag, anything skipped and why.
    why: A correction changes only the planned fields; the carry-across rules and the conflict stop are program checks.
- old line 181: ### Field crosswalk (OM form <-> General Short Risk form)
    now: "One filled real application PDF per application (Old Mutual form or General Short Risk form)", "file":
    why: Only the one-to-one pairs are carried between the two forms.
- old line 183: Detail | OM field | General Short Risk field |
    now: General Short Risk Application (General_Short_Risk_Application_Template.pdf)
    why: Only the one-to-one pairs are carried between the two forms.
- old line 185: Title | Title | Text Box 3 |
    now: Text Box 5_3 | CITY |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 186: First names | FullName (split into names/surname) | Text Box 4 (full names) |
    now: Text Box 4 | FULL NAMES |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 187: Surname | FullName | Text Box 4_2 |
    now: Text Box 4_2 | SURNAME |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 188: ID number | IDNumber | Text Box 4_3 |
    now: Text Box 4_3 | ID NUMBER |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 189: Cell | TelCell | Text Box 4_4 |
    now: Text Box 4_4 | CELL |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 190: Work phone | TelW | Text Box 4_5 |
    now: Text Box 4_5 | WORK |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 191: Email | Email | Text Box 5 |
    now: Text Box 4_5 | WORK |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 192: Residential address | ResidentialAddress (one line) | Text Box 4_6 unit, 4_7 complex, 4_8 street no., 4_9 street name, 5_2 suburb, 5_3 city, 4_10 region (split the address;
    now: the OM form's own field name, or the General form's meaning name (street_no, suburb ...)."""
    why: Only the one-to-one pairs are carried between the two forms.
- old line 193: Postal/residential code | ResidentialCode | Text Box 4_11 |
    now: template, the field *names* in this PDF are generic (Text Box 4_7, List
    why: Only the one-to-one pairs are carried between the two forms.
- old line 194: Account holder | AccountHolder | Text Box 5_4 |
    now: ["Text Box 4_4", "Text Box 4_5"]}[form]
    why: Only the one-to-one pairs are carried between the two forms.
- old line 195: Bank | NameOfBank (dropdown) | Text Box 5_9 |
    now: Text Box 4_5 | WORK |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 196: Branch code | BranchCode | Text Box 4_18 |
    now: Text Box 4_18 | BRANCH CODE |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 197: Account type | AccountType (dropdown) | Text Box 4_19 |
    now: template, the field *names* in this PDF are generic (Text Box 4_7, List
    why: Only the one-to-one pairs are carried between the two forms.
- old line 198: Account number | AccountNumber | Text Box 5_10 |
    now: Text Box 5_10 | ACCOUNT NUMBER |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 199: Beneficiary 1 | BenName + BenSurname, BenIDNumber, BenRelationship, BenShare | Text Box 5_15, 5_16, 4_23, 4_24 |
    now: BenName, BenSurname, BenCellNumber, BenIDNumber, BenRelationship, BenShare | text | beneficiary 1 |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 200: Beneficiary 2 | BenName_2 + BenSurname_2, BenIDNumber_2, BenRelationship_2, BenShare_2 | Text Box 5_17, 5_18, 4_25, 4_26 |
    now: BenName, BenSurname, BenCellNumber, BenIDNumber, BenRelationship, BenShare | text | beneficiary 1 |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 202: OM-only (carry OM -> OM only):
    now: "A planned rename (only with Paul's yes, mv -n, never over an existing folder):
    why: Only the one-to-one pairs are carried between the two forms.
- old line 202: TaxNumber, foreign tax fields, MaritalStatus group, occupation/employment fields, HighestQualification, PostalAddress/PostalCode, Tel*, Beneficiary 3, Nationality, CountryOfBirth, source-of-funds fiel
    now: a foreign tax obligation needs the ForeignTaxNumber" % tag)
    why: Only the one-to-one pairs are carried between the two forms.
- old line 202: Risk-only (carry Risk -> Risk only):
    now: only that it is in a document (or Paul's words), that it
    why: Only the one-to-one pairs are carried between the two forms.
- old line 202: doctor name/phone/years, debit date, children, insolvency/debt-review answers, existing-insurance fields, best phone time.
    now: Text Box 5_6 | EXISTING INSURANCE — Policy Number (only if replacing) |
    why: Only the one-to-one pairs are carried between the two forms.
- old line 206: references/field-mappings.md — full field name/type/dropdown-option tables for both bundled templates, plus the General Short Risk field mapping.
    now: assets/forms.json holds the checksum, every field, its type and every dropdown option of both forms, and the program stops if either form differs.
    why: Replaced by the new pointer list.
- old line 207: assets/OM_Application_Template.pdf — the real, blank OM AcroForm.
    now: OM Application Template (OM_Application_Template.pdf)
    why: Replaced by the new pointer list.
- old line 208: assets/General_Short_Risk_Application_Template.pdf — the real, blank WR general short-term/risk AcroForm.
    now: "General_Short_Risk_Application_Template.pdf",
    why: Replaced by the new pointer list.
- old line 209: scripts/fill_om_form.py — fill_om_application(), add_product_option(), dump_filled_values().
    now: the field value — see scripts/fill_om_form.py's add_product_option() for
    why: Replaced by the new pointer list.
- old line 222: Dump a template's fields yourself at any time to confirm names/types/options
    now: shows ONE step at a time, refuses to skip, keeps the run on disk.
    why: Kept; the program checks the blank forms against the frozen field lists.
- old line 227: r = PdfReader("assets/OM_Application_Template.pdf")
    now: "General_Short_Risk_Application_Template.pdf",
    why: Kept; the program checks the blank forms against the frozen field lists.
- old line 228: for k, v in r.get_fields().items():
    now: for k, v in (PdfReader(path).get_fields() or {}).items():
    why: Kept; the program checks the blank forms against the frozen field lists.
- old line 229: print(k, v.get("/FT"), v.get("/Opt"))
    now: "choice" if v.get("/FT") == "/Ch" else "text"}
    why: Kept; the program checks the blank forms against the frozen field lists.
- old line 367: signature date = meeting date) using this mapping, verify visually, and flag
    now: SignatureDate must be the meeting date as DD/MM/YY, never blank" % tag)
    why: Kept; the meaning table is frozen and change-detected.
- old line 368: back if anything about the layout doesn't match this table.
    now: Never tell Paul something is filled, saved or renamed until the program has read it back (the PDF's fields, the saved folder listing).
    why: Kept; the meaning table is frozen and change-detected.


DROPPED (each is covered by a recorded decision):
- ## Index: Replaced by the new short Index (five sections).
- 2 | Last updated + Changelog | Athens-time stamp, last 5 changes, stan: The stamp is set by tools/stamp_skill.py, never typed (S2); the changelog is archived in this history folder and the pointer to the Project file complete-applications-skill-changelog.md is dropped (Paul agreed, 04/11/2026).
- This template hasn't been run through the fill workflow in production : Dropped: the General form is treated as used in production (Step 1 says so twice); Paul agreed, question 1, 04/11/2026.
