# Presentation Storyline: Guntur April→May 2026 (+122.19%)

All figures: `pharmeasy.db` via `queries.py` / `memo.md`.

## A. For an executive: Situation → Complication → Resolution

**Situation:  Network sales are steady: INR 1,072,207.16 in April, INR 1,103,140.73 in May (+2.89%), on 700 orders each month. Beneath that, Guntur went from INR 62,442.27 to INR 138,738.93 (+122.19%), the largest regional move in the quarter.

**Complication: The jump did not hold. Guntur fell 28.11% in June to INR 99,745.18. It came mainly from a few high-ticket categories, and profit margin slipped from 15.72% to 14.18%. Because network volume is fixed at 700 orders, Guntur's INR 76,296.66 gain exceeded the network's whole gain of INR 30,933.57, so other regions lost share. Acting on it as a trend risks moving stock and targets on a one-month mix effect.

**Resolution:  Hold reallocation. Have a regional lead review the largest May orders now. When July data loads, call it an emerging level shift only if Guntur stays above INR 99,745.18 with average order value above INR 1,224.36. Otherwise treat May as a one-off.

## B. For a regional manager: Overview → Category → Detail

**Overview - Guntur sales +122.19% Apr→May (INR 62,442.27 → INR 138,738.93); orders 51 → 77; average order INR 1,224.36 → INR 1,801.80.

**Category - Three categories explain INR 68,075.50 of the INR 76,296.66 rise: Wellness & Nutrition +INR 33,787.42, Medical Devices +INR 23,276.06, Lab Tests +INR 11,012.02. OTC Medicines (the most frequent category) added only INR 2,056.42.

**Detail - The five largest May orders (Lipid Profile, Nebulizer, Vitamin D Test, Fish Oil Capsules, Whey Protein 1kg) sum to INR 38,091.04 (27.5% of May). Method: sales summed by region and month in SQLite on the deduplicated, normalised 2,100-row table; MoM = (current − previous) / previous × 100; flag rule |MoM| > 8% is an operational alert, not a significance test. June: INR 99,745.18, still 59.7% above April.

## C. Anticipated pushback (Direct Acknowledgement Pattern)

**Q1. "Why should I believe this number?"**
1. Acknowledge: Fair, since 94 profit values and 48 categories were imputed and 59 duplicates removed before this was computed.
2. Verified / not verified: Verified: sales come from `sales_inr`, which was never imputed; order ids are unique (SQL check returns zero duplicate rows); the figure reproduces from `queries.py`. Not verified: that the export is a complete record of Guntur orders.
3. Resolve: Reconcile Guntur's May order count (77) and sales against the source system's own May report; a regional data owner can do this before the July load.

**Q2. "What if something other than demand is driving it?"**
1. Acknowledge: Yes: a handful of large orders can produce this on their own, and the June reversal points that way.
2. Verified / not verified: Verified: orders and order value both rose, and the top 5 orders are 27.5% of May. Not verified: why those orders happened, or any promotion, festival or competitor effect. This dataset can't show it.
3. Resolve: Compare July against June's INR 99,745.18 once July data is loaded; a lead can review the five largest May orders for one-offs before then.

**Q3. "What would change your recommendation?"**
1. Acknowledge: The recommendation to hold is conditional, not permanent.
2. Verified / not verified: Verified: June already gave back 28.11%. Not verified: whether July stays elevated.
3. Resolve: If July Guntur sales stay above INR 99,745.18 with average order value above INR 1,224.36, I would move to "emerging shift" and revisit inventory and targets.
