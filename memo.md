# Memo: Guntur April→May 2026 sales swing

Risk tags: **[LOW]** structural/logical · **[MEDIUM]** reasoned inference · **[HIGH]** specific number, traceable to `python3 queries.py` (section 5) / `pharmeasy.db`.

## Title
Guntur sales rose +122.19% Apr→May 2026, then gave back 28.11% in June: treat as an alert, not yet a trend. [HIGH]

## Context
- Guntur is one of 9 active regions in the Telugu-states + Bengaluru desk export. [HIGH]
- Guntur sales were INR 62,442.27 in April, INR 138,738.93 in May and INR 99,745.18 in June 2026. [HIGH]
- The |MoM| > 8% flag is a fixed operational-alert rule, not a statistical test, and most regions cross it most months. [LOW]
- Guntur's Apr→May move is the largest in magnitude of any region-transition in this dataset. [HIGH]

## Key Insight
- The +122.19% came from both more orders (51 → 77) and larger orders (average INR 1,224.36 → INR 1,801.80). [HIGH]
- Three categories account for INR 68,075.50 of the INR 76,296.66 increase: Wellness & Nutrition +33,787.42, Medical Devices +23,276.06, Lab Tests +11,012.02. [HIGH]
- Because the increase is concentrated in high-ticket categories, the swing looks like an order-mix effect more than broad-based demand growth. [MEDIUM]

## Evidence
- Guntur Apr→May: INR 62,442.27 → INR 138,738.93, change (b−a)/a×100 = +122.19%. [HIGH]
- Network sales Apr→May moved only INR 1,072,207.16 → INR 1,103,140.73 (+2.89%) on 700 and 700 orders. [HIGH]
- Guntur's INR 76,296.66 gain is larger than the network's total gain of INR 30,933.57, so other regions net declined. [HIGH]
- The five largest Guntur orders in May total INR 38,091.04 (27.5% of Guntur's May sales). [HIGH]
- Guntur's profit margin was 15.72% (Apr), 14.18% (May), 15.58% (Jun): sales grew but margin did not. [HIGH]
- June sales of INR 99,745.18 (-28.11% vs May) remain 59.7% above April. [HIGH]

## Recommendation
- Do not reallocate inventory, staffing or targets on the strength of one month's swing. [MEDIUM]
- Have a regional lead review the largest May orders and the three drivers above before the figure is quoted externally. [MEDIUM]
- Re-run the pipeline when July data arrives (state persistence means only July is needed). [LOW]

## Next Check
- When the July export is loaded, compare Guntur's July sales with June's INR 99,745.18 and with May's INR 138,738.93. [HIGH]
- If July stays above INR 99,745.18 with average order value above April's INR 1,224.36, upgrade the finding from "alert" to "emerging level shift". [MEDIUM]
- If July falls back toward INR 62,442.27, treat May as a one-off mix spike. [MEDIUM]

## Assumptions
- **Unverified (flag upfront):** the export is a complete and representative record of Guntur orders, so the +122.19% reflects real order activity rather than sync, attribution or data-entry effects. [MEDIUM]
- Hypothesis (not fact): a handful of large-basket orders in high-ticket categories drove May; only the July check can test it. [MEDIUM]
- Fact about this export: total orders are 700 in April and 700 in May, so regional gains and losses largely offset. This may be an export artefact, not real demand. [HIGH]
- Imputed profit values (94 of 2,100 rows) use category mean margins, so margin figures carry small imputation uncertainty. [MEDIUM]
- No external market context (competitors, festivals, promotions) is used or claimed. [LOW]
