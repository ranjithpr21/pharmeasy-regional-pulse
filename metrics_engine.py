"""Part 2.3/2.4 - monthly metrics, significance flagging, state persistence."""
import json, sqlite3

MONTHS = ["2026-04", "2026-05", "2026-06"]

def monthly_sales(db="pharmeasy.db"):
    """{region: {month: total_sales}} via SQL GROUP BY."""
    con = sqlite3.connect(db)
    rows = con.execute("""SELECT region, substr(order_date,1,7) AS m, ROUND(SUM(sales_inr),2)
                          FROM orders_clean GROUP BY region, m""").fetchall()
    con.close()
    out = {}
    for r, m, s in rows:
        out.setdefault(r, {})[m] = s
    return out

def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0
    return (current - previous) / previous * 100

def flag_significant_regions_v1(changes, threshold=8):
    """Fixed-percentage operational alert (NOT a statistical test)."""
    return [r for r, c in changes.items() if abs(c) > threshold]

def save_state_v1(month_summary, path):
    with open(path, "w") as f:
        json.dump(month_summary, f, indent=2, sort_keys=True)

def load_previous_state_v1(path):
    with open(path) as f:
        return json.load(f)

def mom_changes(sales, prev_m, cur_m):
    return {r: round(compute_percentage_change_v1(v[cur_m], v[prev_m]), 2) for r, v in sales.items()}

if __name__ == "__main__":
    sales = monthly_sales()
    for p, c in [(MONTHS[0], MONTHS[1]), (MONTHS[1], MONTHS[2])]:
        ch = mom_changes(sales, p, c)
        print(f"\n{p} -> {c}")
        for r, v in sorted(ch.items(), key=lambda x: -abs(x[1])):
            print(f"  {r:14s}{v:+9.2f}%")
        print("  flagged:", sorted(flag_significant_regions_v1(ch)))
    # state persistence demo: save April, reload, recompute Apr->May from state + May only
    save_state_v1({r: v[MONTHS[0]] for r, v in sales.items()}, "state_2026-04.json")
    prev = load_previous_state_v1("state_2026-04.json")
    assert prev == {r: v[MONTHS[0]] for r, v in sales.items()}
    print("\nstate round-trip OK")
