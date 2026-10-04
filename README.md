# PharmEasy Regional Pulse

PharmEasy Regional Pulse is a deterministic regional-performance intelligence pipeline for cleaning monthly order data, validating data quality, computing SQL-verified regional metrics, flagging significant month-on-month movements, generating a reviewable narrative, and presenting the results through a local Streamlit dashboard.

## Headline Finding

Guntur recorded the largest flagged movement in the generated dataset, with April-to-May sales increasing by **122.19%**, making it the primary case for human review and operational follow-up.

## Four-Artifact Cover Note

- **Streamlit dashboard — `app.py`**: Provides live local exploration of verified sales, profit, order counts, category performance, regional trends, and detailed monthly results.
- **CII narrative — embedded in the dashboard**: Explains the verified regional movements using Context, Insight, and Implication without inventing external causes.
- **One-page memo — `memo.md`**: Provides the recommendation for the Guntur April-to-May movement using only verified dataset evidence.
- **Presentation storyline — `presentation_storyline.md`**: Shows how the same Guntur finding can be explained to an executive and a regional manager and includes anticipated stakeholder questions.

### Recommended Reviewer Order

1. Open `app.py` using Streamlit and review the dashboard.
2. Read the embedded CII executive narrative.
3. Read `memo.md` for the recommendation.
4. Read `presentation_storyline.md` for the stakeholder presentation and Q&A.
5. Review the supporting Python pipeline and SQL validation files.

### Single Unverified Assumption

The data verifies that Guntur sales increased by 122.19% from April to May, but the dataset does not verify the operational cause of that movement; therefore, any proposed cause must be treated as a hypothesis until additional evidence is checked.

## Pipeline

```text
Raw Dataset
    ↓
Dataset Generation
    ↓
Data Cleaning & Validation
    ↓
SQLite Database
    ↓
SQL Verification
    ↓
Monthly Metrics
    ↓
8% Operational Flagging Rule
    ↓
CII Narrative
    ↓
Human Review Gate
    ↓
Audit Log
    ↓
Streamlit Dashboard
```

This is a conventional Python and SQL analytics workflow. It does not require an AI model, API key, paid service, or network connection.

## Repository Structure

```text
pharmeasy-regional-pulse/
│
├── README.md
├── generate_dataset.py
├── clean_data.py
├── data_quality_report.md
│
├── build_db.py
├── queries.py
├── metrics_engine.py
│
├── draft_report.py
├── memo.md
├── review_gate.py
├── audit_log.jsonl
├── reliability_checklist.md
│
├── app.py
└── presentation_storyline.md
```

Generated runtime files include:

```text
pharmeasy_orders_raw.csv
regions_master.csv
orders_clean.csv
pharmeasy.db
```

## Requirements

- Python 3.10 or later
- pandas
- Streamlit
- Plotly

SQLite is provided by Python's standard library.

No API key or paid service is required.

## Installation

Clone the repository and enter the project directory:

```bash
git clone <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>
cd pharmeasy-regional-pulse
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Pipeline

Generate the deterministic dataset:

```bash
python3 generate_dataset.py
```

Clean and validate the data:

```bash
python3 clean_data.py
```

Build the SQLite database:

```bash
python3 build_db.py
```

Run SQL validation and metrics:

```bash
python3 queries.py
```

Generate the CII report:

```bash
python3 draft_report.py
```

Run the human review-gate test harness:

```bash
python3 review_gate.py
```

Start the dashboard:

```bash
streamlit run app.py
```

## Expected Acceptance Checks

The deterministic dataset is expected to produce:

| Check | Expected Result |
|---|---:|
| Raw rows | 2,159 |
| Master regions | 10 |
| Exact duplicates removed | 59 |
| Clean rows | 2,100 |
| Missing categories before imputation | 48 |
| Missing profits before imputation | 94 |
| LEFT JOIN rows | 2,101 |
| INNER JOIN rows | 2,100 |
| Duplicate order IDs | 0 |
| Zero-order region | Kurnool |
| April → May flagged regions | 7 |
| May → June flagged regions | 7 |
| Guntur April → May movement | +122.19% |

The 8% threshold is an operational alert rule. A flag means the number deserves human review; it does not establish statistical significance or prove a cause.

## Non-AI Design

The project intentionally uses a conventional deterministic analytics workflow:

- Python for data processing
- pandas for cleaning and transformation
- SQLite for SQL verification
- predefined percentage-change rules for alerting
- deterministic templates for CII reporting
- a human review gate for approval
- JSON Lines for the audit trail
- Streamlit and Plotly for visualization

No generative AI, LLM, external API, API key, paid service, or network connection is required.

## Human Review

The review gate supports three decisions:

```text
approve
edit
reject
```

Every review action is written to:

```text
audit_log.jsonl
```

The audit record contains:

```text
timestamp
run_id
region
decision
reviewer_note
```

## Dashboard

The dashboard provides:

1. Overview KPIs
2. Category-level analysis
3. Region/month detail
4. Interactive region filtering
5. Monthly regional sales trend
6. Regional sales comparison
7. Category sales share

The order-count KPI uses a distinct `order_id` count.

## Data Quality

The cleaning stage addresses data-quality dimensions including:

- Accuracy
- Completeness
- Consistency
- Timeliness
- Validity
- Uniqueness
- Relevance

Detailed checks are documented in `data_quality_report.md`.

## Project Disclaimer

The generated dataset is synthetic and deterministic for assessment purposes. The Guntur movement is a property of this generated dataset and should not be interpreted as a real PharmEasy business result.
