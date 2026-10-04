"""Part 3.1 - CII insight generator. Every number comes from Part 2 metrics."""
from metrics_engine import (MONTHS, monthly_sales, mom_changes, flag_significant_regions_v1)

T1, T2 = f"{MONTHS[0]}->{MONTHS[1]}", f"{MONTHS[1]}->{MONTHS[2]}"
inr = lambda x: f"INR {x:,.2f}"

def build_metrics(db="pharmeasy.db"):
    sales = monthly_sales(db)
    changes = {T1: mom_changes(sales, MONTHS[0], MONTHS[1]),
               T2: mom_changes(sales, MONTHS[1], MONTHS[2])}
    flagged = {T1: flag_significant_regions_v1(changes[T1]),
               T2: flag_significant_regions_v1(changes[T2])}
    return flagged, {"sales": sales, "changes": changes}

def draft_report_v1(flagged_regions, metrics, run_id="run-2026-06"):
    """flagged_regions: {transition: [regions]}. One deduped CII block per unique region."""
    by_region = {}
    for t, regs in flagged_regions.items():
        for r in regs:
            by_region.setdefault(r, []).append(t)
    blocks = []
    for r in sorted(by_region):
        s, ts = metrics["sales"][r], by_region[r]
        ch = {t: metrics["changes"][t][r] for t in ts}
        context = (f"{r} sales were {inr(s[MONTHS[0]])} in Apr, {inr(s[MONTHS[1]])} in May and "
                   f"{inr(s[MONTHS[2]])} in Jun 2026. Flagged (|MoM| > 8%) for: "
                   + "; ".join(f"{t} ({ch[t]:+.2f}%)" for t in ts) + ".")
        big = max(ch.items(), key=lambda kv: abs(kv[1]))
        insight = (f"Largest move: {big[0]} at {big[1]:+.2f}%. "
                   + ("Both transitions moved in opposite directions, so the level is not steadily trending."
                      if len(ts) == 2 and ch[T1] * ch[T2] < 0 else
                      "Only one transition crossed the threshold." if len(ts) == 1 else
                      "Both transitions moved the same way."))
        implication = ("Fixed-threshold alert only, not a significance test: review the underlying order mix "
                       "before acting, and confirm against the next month's data.")
        blocks.append({"run_id": run_id, "region": r, "transitions": ts, "changes_pct": ch,
                       "context": context, "insight": insight, "implication": implication,
                       "status": "draft", "decision": None, "external_use_allowed": False})
    return blocks

if __name__ == "__main__":
    fl, m = build_metrics()
    blocks = draft_report_v1(fl, m)
    print(f"{len(blocks)} unique flagged regions\n")
    for b in blocks:
        print(f"[{b['region']}]\n  Context: {b['context']}\n  Insight: {b['insight']}\n  Implication: {b['implication']}\n")
