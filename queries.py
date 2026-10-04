"""Part 2.2 - JOIN validation + region x month SQL. Run: python3 queries.py"""
import sqlite3
con = sqlite3.connect("pharmeasy.db")
q = lambda s: con.execute(s).fetchall()

left = q("SELECT COUNT(*) FROM regions_master r LEFT JOIN orders_clean o ON r.region=o.region")[0][0]
inner = q("SELECT COUNT(*) FROM regions_master r INNER JOIN orders_clean o ON r.region=o.region")[0][0]
print(f"1. LEFT JOIN rows={left} | INNER JOIN rows={inner} | delta={left-inner}")

dups = q("SELECT order_id, COUNT(*) FROM orders_clean GROUP BY order_id HAVING COUNT(*)>1")
print(f"2. duplicate order_ids: {len(dups)} rows returned {dups}")

print("3. COUNT(*) vs COUNT(o.order_id) under LEFT JOIN")
print(f"   {'region':14s}{'COUNT(*)':>9s}{'COUNT(order_id)':>16s}")
for r, a, b in q("""SELECT r.region, COUNT(*), COUNT(o.order_id) FROM regions_master r
                    LEFT JOIN orders_clean o ON r.region=o.region GROUP BY r.region ORDER BY r.region"""):
    print(f"   {r:14s}{a:9d}{b:16d}" + ("   <-- DISAGREE (COUNT(*) is wrong)" if a != b else ""))

print("4. Per-region order counts (LEFT JOIN, ascending)")
for r, n in q("""SELECT r.region, COUNT(o.order_id) n FROM regions_master r
                 LEFT JOIN orders_clean o ON r.region=o.region GROUP BY r.region ORDER BY n ASC, r.region"""):
    print(f"   {r:14s}{n:5d}")

print("5. Sales by region x month (INR) and MoM %")
rows = q("""SELECT region, substr(order_date,1,7), ROUND(SUM(sales_inr),2), COUNT(DISTINCT order_id)
            FROM orders_clean GROUP BY 1,2 ORDER BY 1,2""")
d = {}
for r, m, s, n in rows: d.setdefault(r, {})[m] = (s, n)
for r, v in d.items():
    a, b, c = v["2026-04"][0], v["2026-05"][0], v["2026-06"][0]
    print(f"   {r:14s} Apr {a:>10,.2f} May {b:>10,.2f} Jun {c:>10,.2f} | Apr->May {(b-a)/a*100:+7.2f}% May->Jun {(c-b)/b*100:+7.2f}% | orders {v['2026-04'][1]}/{v['2026-05'][1]}/{v['2026-06'][1]}")
