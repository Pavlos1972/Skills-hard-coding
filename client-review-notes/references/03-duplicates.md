Before formatting a record, the program checks the earlier Client Records you registered: the same name as Paul gave, or an ID number that appears in the raw notes. If one matches, FLAG it first: show Paul both and ask whether to merge or keep them separate; record his words with `run.py duplicate`. Never merge silently.

If he says merge: produce ONE merged record combining all the unique information of both versions, and enter `merge_notes` saying which version contributed which additional details. The program then proves that nothing from either version is lost (every date, amount, number, code, name of the earlier record is in the merged one, or listed in `left_out` with a reason). If he says separate, nothing is merged.

The old rule only looked at records formatted "in the current session"; this one looks at every earlier record you are given, so give it the earlier `.md` files of the client.
