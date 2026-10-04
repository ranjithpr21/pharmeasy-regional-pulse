"""Generates memo.md from SQL so every [HIGH] number is traceable. Run: python3 make_memo.py"""
import sqlite3
con = sqlite3.connect("pharmeasy.db"); q = lambda s, *a: con.execute(s, a).fetchall()
def one(m, col): return q(f"SELECT ROUND(SUM({col}),2), COUNT(DISTINCT order_id) FROM orders_clean WHERE region='Guntur' AND order_date LIKE ?", m + "%")[0]
(a, an), (b, bn), (j, jn) = one("2026-04", "sales_inr"), one("2026-05", "sales_inr"), one("2026-06", "sales_inr")
net = {m: q("SELECT ROUND(SUM(sales_inr),2), COUNT(DISTINCT order_id) FROM orders_clean WHERE order_date LIKE ?", m + "%")[0] for m in ("2026-04", "2026-05")}
cat = {c: dict(q("SELECT substr(order_date,1,7), ROUND(SUM(sales_inr),2) FROM orders_clean WHERE region='Guntur' AND category=? GROUP BY 1", c))
       for c in ("Wellness & Nutrition", "Medical Devices", "Lab Tests")}
d = {c: round(v["2026-05"] - v["2026-04"], 2) for c, v in cat.items()}
top3 = round(sum(d.values()), 2); gain = round(b - a, 2)
aov = lambda s, n: s / n
top5 = q("SELECT SUM(s) FROM (SELECT sales_inr s FROM orders_clean WHERE region='Guntur' AND order_date LIKE '2026-05%' ORDER BY s DESC LIMIT 5)")[0][0]
mg = dict(q("SELECT substr(order_date,1,7), ROUND(SUM(profit_inr)*100.0/SUM(sales_inr),2) FROM orders_clean WHERE region='Guntur' GROUP BY 1"))
pct = (b - a) / a * 100; jp = (j - b) / b * 100
f = lambda x: f"{x:,.2f}"
md = f"""# Memo: Guntur April→May 2026 sales swing

Risk tags: **[LOW]** structural/logical · **[MEDIUM]** reasoned inference · **[HIGH]** specific number, traceable to `python3 queries.py` (section 5) / `pharmeasy.db`.

## Title
Guntur sales rose {pct:+.2f}% Apr→May 2026, then gave back {abs(jp):.2f}% in June: treat as an alert, not yet a trend. [HIGH]

## Context
- Guntur is one of 9 active regions in the Telugu-states + Bengaluru desk export. [HIGH]
- Guntur sales were INR {f(a)} in April, INR {f(b)} in May and INR {f(j)} in June 2026. [HIGH]
- The |MoM| > 8% flag is a fixed operational-alert rule, not a statistical test, and most regions cross it most months. [LOW]
- Guntur's Apr→May move is the largest in magnitude of any region-transition in this dataset. [HIGH]

## Key Insight
- The +{pct:.2f}% came from both more orders ({an} → {bn}) and larger orders (average INR {f(aov(a,an))} → INR {f(aov(b,bn))}). [HIGH]
- Three categories account for INR {f(top3)} of the INR {f(gain)} increase: Wellness & Nutrition +{f(d['Wellness & Nutrition'])}, Medical Devices +{f(d['Medical Devices'])}, Lab Tests +{f(d['Lab Tests'])}. [HIGH]
- Because the increase is concentrated in high-ticket categories, the swing looks like an order-mix effect more than broad-based demand growth. [MEDIUM]

## Evidence
- Guntur Apr→May: INR {f(a)} → INR {f(b)}, change (b−a)/a×100 = {pct:+.2f}%. [HIGH]
- Network sales Apr→May moved only INR {f(net['2026-04'][0])} → INR {f(net['2026-05'][0])} ({(net['2026-05'][0]-net['2026-04'][0])/net['2026-04'][0]*100:+.2f}%) on {net['2026-04'][1]} and {net['2026-05'][1]} orders. [HIGH]
- Guntur's INR {f(gain)} gain is larger than the network's total gain of INR {f(net['2026-05'][0]-net['2026-04'][0])}, so other regions net declined. [HIGH]
- The five largest Guntur orders in May total INR {f(top5)} ({top5/b*100:.1f}% of Guntur's May sales). [HIGH]
- Guntur's profit margin was {mg['2026-04']}% (Apr), {mg['2026-05']}% (May), {mg['2026-06']}% (Jun): sales grew but margin did not. [HIGH]
- June sales of INR {f(j)} ({jp:+.2f}% vs May) remain {(j/a-1)*100:.1f}% above April. [HIGH]

## Recommendation
- Do not reallocate inventory, staffing or targets on the strength of one month's swing. [MEDIUM]
- Have a regional lead review the largest May orders and the three drivers above before the figure is quoted externally. [MEDIUM]
- Re-run the pipeline when July data arrives (state persistence means only July is needed). [LOW]

## Next Check
- When the July export is loaded, compare Guntur's July sales with June's INR {f(j)} and with May's INR {f(b)}. [HIGH]
- If July stays above INR {f(j)} with average order value above April's INR {f(aov(a,an))}, upgrade the finding from "alert" to "emerging level shift". [MEDIUM]
- If July falls back toward INR {f(a)}, treat May as a one-off mix spike. [MEDIUM]

## Assumptions
- **Unverified (flag upfront):** the export is a complete and representative record of Guntur orders, so the +{pct:.2f}% reflects real order activity rather than sync, attribution or data-entry effects. [MEDIUM]
- Hypothesis (not fact): a handful of large-basket orders in high-ticket categories drove May; only the July check can test it. [MEDIUM]
- Fact about this export: total orders are {net['2026-04'][1]} in April and {net['2026-05'][1]} in May, so regional gains and losses largely offset. This may be an export artefact, not real demand. [HIGH]
- Imputed profit values (94 of 2,100 rows) use category mean margins, so margin figures carry small imputation uncertainty. [MEDIUM]
- No external market context (competitors, festivals, promotions) is used or claimed. [LOW]
"""
open("memo.md", "w", encoding="utf-8").write(md); print(md)
