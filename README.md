# Retail Sales Analytics & ETL Pipeline

An end-to-end data analytics portfolio project using **Python, Pandas, SQL, SQLite, and Streamlit**.

> **Dataset transparency:** The included 1,200-row retail dataset is synthetic sample data generated for this project. It is not real company/customer data. Do not present its results as actual business performance.

## What it demonstrates
- Extract raw transaction data from CSV.
- Clean and validate missing or invalid records with Pandas.
- Transform transactions and calculate gross sales and net revenue.
- Load cleaned records into SQLite.
- Analyse KPIs with SQL aggregations and window functions.
- Explore revenue trends using an interactive Streamlit dashboard.
- Filter by date, region, and category; inspect and export filtered data.

## Structure
```text
retail-sales-analytics/
├── app.py
├── run_pipeline.py
├── requirements.txt
├── README.md
├── data/sales_raw.csv
├── sql/analysis_queries.sql
└── src/
    ├── __init__.py
    ├── etl.py
    └── analytics.py
```

## Run locally
Requires Python 3.10+.

```bash
git clone https://github.com/YOUR-USERNAME/retail-sales-analytics.git
cd retail-sales-analytics
python -m venv .venv
```

Windows activation:
```bash
.venv\Scripts\activate
```

macOS/Linux activation:
```bash
source .venv/bin/activate
```

Install and run:
```bash
pip install -r requirements.txt
python run_pipeline.py
streamlit run app.py
```

Open the local URL printed by Streamlit (normally `http://localhost:8501`).

## Key calculations
- Gross sales = quantity × unit price
- Net revenue = quantity × unit price × (1 − discount)
- Orders = count of unique order IDs
- Average revenue per order = net revenue ÷ unique orders

## SQL topics
See `sql/analysis_queries.sql` for `GROUP BY`, aggregations, monthly trends, category and region comparisons, customer segmentation, and `DENSE_RANK()`.

## Resume description (use after running and understanding it)
**Retail Sales Analytics & ETL Pipeline | Python, Pandas, SQL, SQLite, Streamlit**
- Built a Python ETL workflow to clean, validate, transform, and load retail transaction data into SQLite.
- Wrote SQL queries to analyse revenue by month, region, product category, and customer type.
- Developed an interactive Streamlit dashboard with sales KPIs, trend charts, filters, and data export.

Only report dataset counts or other metrics after verifying them by running the pipeline.

## GitHub
Create a public repository named `retail-sales-analytics` and upload the contents of this folder. Do not upload `.venv/`, credentials, or generated database files.
