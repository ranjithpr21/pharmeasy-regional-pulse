# Data-Quality Report (Part 1)

Source: `pharmeasy_orders_raw.csv` (2,159 rows) → `orders_clean.csv` (2,100 rows). Produced by `clean_data.py`; all counts below are its printed output.

| # | Fix (in pipeline order) | Problem found | Dimension addressed |

| 1 | Drop exact duplicates (all 8 columns) | 59 duplicate rows from copy-paste of source sheets | **Uniqueness** (also protects **Accuracy**: sales/order counts were overstated) |
| 2 | Strip + title-case `region` | 16 raw spellings (e.g. `" hyderabad"`, `"VIJAYAWADA"`) → 9 canonical names | **Consistency** (also **Validity**: every value now matches `regions_master.csv`) |
| 3 | Impute `category` from product→category lookup | 48 blank categories; lookup is exact (each product maps to exactly one category, asserted in code) | **Completeness** |
| 4 | Impute `profit_inr` = sales × category mean margin | 94 blank profits (nightly-sync loss); mean margins are ~14.8–15.3% per category | **Completeness** (with an **Accuracy** trade-off: imputed values are estimates) |
| 5 | `validate_schema()` gate | Blocks the pipeline if a required column is missing | **Validity** |

## All 7 dimensions

- **Accuracy** – duplicates removed; imputed profit is an estimate, flagged as an assumption in `memo.md`.
- **Completeness** – 0 missing `category` and 0 missing `profit_inr` remain.
- **Consistency** – one canonical spelling per region.
- **Timeliness** – *not fixed here.* The export covers Apr–Jun 2026 only; the dataset has no load timestamps, so freshness cannot be measured. State persistence (`metrics_engine.py`) lets a new month be added without recomputing history.
- **Validity** – region names checked against `regions_master.csv`; required columns checked by `validate_schema`.
- **Uniqueness** – `order_id` is unique after dedup (SQL check in `queries.py`).
- **Relevance** – *not fixed here.* All 8 columns are used downstream; Kurnool has no orders and is retained in the master table on purpose (LEFT JOIN test).

## Validation results
`validate_schema(clean)` → `{'status': 'validated', 'row_count': 2100, 'missing_columns': []}`
`validate_schema(clean minus profit_inr)` → `{'status': 'blocked_schema', 'row_count': 2100, 'missing_columns': ['profit_inr']}`
