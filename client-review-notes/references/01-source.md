The raw notes are the notes of the client's Outlook contact. **Paul gives them to you**: pasted into the chat or attached. Write them to a text file exactly as given (never tidied, shortened or re-ordered) and register them with `run.py notes --route pasted`. If Paul instead asks you to fetch them, try the routes in order (1 the computer, 2 the Microsoft 365 connector, 3 Zapier, for example its "find a contact" tool, which is unproven for notes) and log every try with `run.py access --purpose notes`, failures too; never say "I cannot access your files" without a log of all three. Paul is asked last, with proof of what was searched.

The program splits the notes into dated entries (a line that starts with a date such as 14/02/2022, 2022-02-14, 14 Feb 2022 or MARCH 2024, a time after it is allowed). Text before the first dated line is entry 0. When it cannot find at least two dated entries it treats the whole note as ONE entry, says so, and the audit shows that the coverage check was weaker.

Earlier Client Records of the same client (Markdown files made by this skill) are registered with `run.py earlier`; they are used only for the duplicate check (page 03).

If the notes appear lost or clearly incomplete, flag it with ⚠️ in the Notes and tell Paul; the program cannot know.
