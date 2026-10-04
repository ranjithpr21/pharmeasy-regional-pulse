"""Part 3.4 - human review gate + audit log + test harness."""
import copy, json, datetime, os

ALLOWED = ("approve", "edit", "reject")
LOG = "audit_log.jsonl"

def _log(report, decision, note, valid=True):
    entry = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
             "run_id": report.get("run_id"), "region": report.get("region"),
             "decision": decision, "reviewer_note": note}
    if not valid:
        entry["valid"] = False
    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def review_gate_v1(report, decision, reviewer_note=""):
    if decision not in ALLOWED:
        _log(report, decision, reviewer_note, valid=False)   # failed attempts are audited too
        raise ValueError(f"decision must be one of {ALLOWED}, got {decision!r}")
    out = copy.deepcopy(report)
    out["decision"] = decision
    out["reviewer_note"] = reviewer_note
    out["status"] = {"approve": "approved", "edit": "needs_edit", "reject": "rejected"}[decision]
    out["external_use_allowed"] = decision == "approve"      # edit must be re-reviewed; reject blocks
    _log(report, decision, reviewer_note)
    return out

if __name__ == "__main__":
    from draft_report import build_metrics, draft_report_v1
    if os.path.exists(LOG):
        os.remove(LOG)
    fl, m = build_metrics()
    blocks = {b["region"]: b for b in draft_report_v1(fl, m)}
    cases = [("Guntur", "approve", "Numbers tie to queries.py section 5."),
             ("Tirupati", "edit", "Add note that Tirupati reversed -17.07% in June."),
             ("Karimnagar", "reject", "Only 22-38 orders/month; too thin to publish.")]
    for region, dec, note in cases:
        after = review_gate_v1(blocks[region], dec, note)
        print(f"{region}: BEFORE status={blocks[region]['status']} external={blocks[region]['external_use_allowed']}"
              f" -> AFTER status={after['status']} external={after['external_use_allowed']}")
    try:
        review_gate_v1(blocks["Guntur"], "maybe")
    except ValueError as e:
        print("invalid decision rejected:", e)
    print(f"\n{LOG}:"); print(open(LOG).read())
