"""Rebuilds, from the run folder, everything the program is responsible for: the value of every field of every application, its source, the
names, the flags, the table Paul says yes to. run.py uses it to build, verify.py REBUILDS and compares, so a file edited by hand cannot pass.
"""
import os

import apps as A
import docread
import wrlib as w


def p(run, name):
    return os.path.join(run, name)


def load_docs(run):
    docs = w.load_opt(p(run, w.DOCS), {"docs": {}, "currents": {}})
    docs.setdefault("docs", {})
    docs.setdefault("currents", {})
    evid = {}
    for role, d in docs["docs"].items():
        try:
            evid[role] = docread.Evidence(w.load_json(p(run, d["text_file"])))
        except Exception:
            pass
    return docs, evid


def route_order_problems(log):
    """The routes are tried in order, separately for each purpose: [route names used too early]."""
    bad, failed = [], {}
    for e in log:
        pur = e.get("purpose", "docs")
        f = failed.setdefault(pur, set())
        i = w.ROUTES.index(e["route"])
        if any(r not in f for r in w.ROUTES[:i]):
            bad.append("%s (%s)" % (e["route"], pur))
        if e["result"] == "failed":
            f.add(e["route"])
    return bad


def current_apps(docs):
    """{id: {"form", "values", "name", "file"}} of the registered current applications."""
    return {i: {"form": c["form"], "values": c["values"], "name": c["name"], "file": c["file"]} for i, c in docs["currents"].items()}


def compute(run):
    rj = w.load_json(p(run, w.RUN))
    today = w.parse_date(rj["today"])
    plan = w.load_opt(p(run, w.PLAN), None)
    out = {"rj": rj, "today": today, "plan": plan, "client": None, "apps": [], "problems": [], "flags": [], "rows": []}
    if plan is None:
        return out
    docs, evid = load_docs(run)
    out["docs"], out["evid"] = docs, evid
    client = {"first": rj["client"]["first"], "surname": rj["client"]["surname"]}
    out["client"] = client
    P = out["problems"]
    items = plan.get("apps") or []
    if plan.get("mode") != rj["mode"]:
        P.append("the plan's mode '%s' is not the run's mode '%s'" % (plan.get("mode"), rj["mode"]))
    if not items:
        P.append("the plan holds no application")
    seen = set()
    currents = current_apps(docs)
    listing = [x.lower() for x in ((plan.get("listing") or {}).get("applications") or [])]
    for app in items:
        aid = app.get("id")
        if not aid or aid in seen:
            P.append("every application needs its own id")
            continue
        seen.add(aid)
        row = {"app": app, "id": aid}
        if rj["mode"] == "prefill":
            if app.get("form") not in A.FORMS:
                P.append("%s: form must be 'om' or 'general'" % aid)
                continue
            R = A.build_values(app, client, evid, set(docs["docs"]), today)
            row.update(form=app["form"], values=R["values"], old={}, sources=R["sources"], changes=[], problems=R["problems"], flags=R["flags"], new_option=R["new_option"], base=A.template_path(app["form"]))
            fn, fo = A.file_name(app, client), A.folder_name(app, client)
            row.update(file_name=fn, folder_name=fo)
            if fn is None:
                P.append("%s: the file name cannot be built (insurer abbreviation, product short name or type, amount and meeting date; a new insurer or product needs Paul's words)" % aid)
            if fo is None:
                P.append("%s: the transaction folder name cannot be built" % aid)
            if fn and fn.lower() in listing and len(((app.get("overwrite") or {}).get("paul_said") or "").strip()) < 5:
                P.append("%s: a file called '%s' already exists in the Applications folder (Paul may have completed it live). Use correction mode, or record his yes to overwrite (overwrite.paul_said)" % (aid, fn))
            row["superseded"] = [x for x in ((plan.get("listing") or {}).get("applications") or []) if "application" in x.lower() and x.lower() != (fn or "").lower()
                                 and A.abbr_of(app) and x.lower().startswith((A.abbr_of(app) or "").lower() + " - ") and (A.product_type(app) or "").lower() in x.lower()]
            tf = app.get("txn_folder") or {}
            if tf.get("root") not in A.settings()["roots"] or not tf.get("current_name") or tf.get("is_current_transaction") is not True:
                P.append("%s: txn_folder needs root (%s), current_name and is_current_transaction: true (the current transaction folder, not the older unnamed one)" % (aid, " or ".join(A.settings()["roots"])))
            elif len(tf.get("candidates") or []) > 1 and len((tf.get("paul_said") or "").strip()) < 5:
                P.append("%s: more than one transaction folder could be current; Paul says which (txn_folder.paul_said)" % aid)
            row["rename"] = bool(fo and tf.get("current_name") and tf["current_name"] != fo)
        else:
            cur = currents.get(app.get("current_id"))
            if cur is None:
                P.append("%s: current_id '%s' is not a registered current application (run.py current)" % (aid, app.get("current_id")))
                continue
            R = A.correction_values(app, cur, currents, evid, set(docs["docs"]), today)
            srcs = {n: s for n, _o, _nw, s in R["changes"]}
            row.update(form=cur["form"], values=R["values"], old=R["old"], sources=srcs, changes=R["changes"], problems=R["problems"], flags=R["flags"], new_option=None,
                       base=os.path.join(run, cur["file"]), file_name=cur["name"], folder_name=None, rename=False, superseded=[])
        for pr in row["problems"]:
            P.append(pr)
        out["flags"] += row["flags"]
        row["blanks"] = [A.label(row["form"], n) for n in A.blanks(row["form"], row["values"])]
        out["apps"].append(row)
    out["rows"] = table_rows(out) if not P else []
    return out


def table_rows(c):
    rows = []
    for a in c["apps"]:
        form = a["form"]
        head = "%s (%s)" % (a["file_name"], A.FORM_NAMES[form])
        if c["rj"]["mode"] == "prefill":
            rows.append(("Application %s: NEW file" % a["id"], head, "program: file name built from fixed lists"))
            ex = (a["app"].get("txn_folder") or {})
            rows.append(("Saved into", "%s%s\\%s\\Applications" % (A.settings()["root_path"], ex.get("root"), ex.get("current_name")), "the client's folder"))
            if a["rename"]:
                rows.append(("Transaction folder rename (mv -n, your yes covers it)", "%s  ->  %s" % (ex.get("current_name"), a["folder_name"]), "your 08/10 rule, name built by the program"))
            if (a["app"].get("overwrite") or {}).get("paul_said"):
                rows.append(("OVERWRITES an existing file", a["file_name"], "Paul: %s" % a["app"]["overwrite"]["paul_said"]))
            for n, v in a["values"].items():
                rows.append(("  %s" % A.label(form, n), A.mask_text(v), A.mask_text(a["sources"].get(n, ""))))
            for s_ in a["superseded"]:
                rows.append(("Possible older draft (listed only, never deleted)", s_, "the Applications folder listing"))
        else:
            rows.append(("Application %s: CORRECTION in place" % a["id"], head, "one copy, same file name"))
            for n, old, new, src in a["changes"]:
                rows.append(("  %s" % A.label(form, n), "%s  ->  %s" % (A.mask_text(old) or "(blank)", A.mask_text(new) or "(blank)"), A.mask_text(src)))
        rows.append(("  Still blank (listed in the hand-back)", ", ".join(a["blanks"]) or "none", "the form"))
        for fl in a["flags"]:
            rows.append(("  FLAG (not a refusal)", fl, "program check"))
    return rows


def confirm_sha(c):
    plan = c["plan"]
    return w.content_hash({"plan": plan, "rows": c["rows"], "names": [(a["id"], a["file_name"], a["folder_name"]) for a in c["apps"]]})


def handback(c, receipts):
    """One short block per application (Paul's rule 7.7): file, what was done, what is still blank, flags. ID and account numbers masked."""
    out = []
    for a in c["apps"]:
        mode = c["rj"]["mode"]
        lines = ["%s" % a["file_name"]]
        if mode == "prefill":
            filled = len([v for v in a["values"].values() if (v or "").strip()])
            lines.append("  new %s, %d field(s) filled; saved in %s\\%s\\Applications" % (A.FORM_NAMES[a["form"]], filled, (a["app"].get("txn_folder") or {}).get("root"), (a["folder_name"] if a["rename"] else (a["app"].get("txn_folder") or {}).get("current_name"))))
            if a["rename"]:
                lines.append("  transaction folder renamed to: %s" % a["folder_name"])
        else:
            lines.append("  corrected in place (one copy); %d field(s) changed:" % len(a["changes"]))
            for n, old, new, _s in a["changes"]:
                lines.append("    %s: %s -> %s" % (A.label(a["form"], n), A.mask_text(old) or "(blank)", A.mask_text(new) or "(blank)"))
        lines.append("  still blank or needing input: %s" % (", ".join(a["blanks"]) or "none"))
        for fl in a["flags"]:
            lines.append("  flag: " + fl)
        for s_ in a["superseded"]:
            lines.append("  possible older draft, NOT deleted (Paul decides): %s" % s_)
        out.append("\n".join(lines))
    return "\n\n".join(out)
