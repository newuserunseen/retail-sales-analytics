from pathlib import Path
import pandas as pd
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_raw.csv"
OUT = ROOT / "output"
DB = OUT / "retail_sales.db"

def run_pipeline():
    raw = pd.read_csv(DATA)
    required = ["order_id","order_date","region","category","product","quantity","unit_price","discount","customer_type"]
    missing = set(required) - set(raw.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    df = raw[required].copy()
    input_rows = len(df)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for col in ["quantity","unit_price","discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["region","category","product","customer_type"]:
        df[col] = df[col].astype("string").str.strip()
    df = df.drop_duplicates(subset=["order_id"])
    df = df.dropna(subset=required)
    df = df[(df.quantity > 0) & (df.unit_price > 0) & df.discount.between(0,1)].copy()
    df["gross_sales"] = df.quantity * df.unit_price
    df["net_revenue"] = df.gross_sales * (1-df.discount)
    df["order_month"] = df.order_date.dt.to_period("M").astype(str)
    df["order_date"] = df.order_date.dt.strftime("%Y-%m-%d")
    OUT.mkdir(exist_ok=True)
    df.to_csv(OUT/"sales_cleaned.csv",index=False)
    with sqlite3.connect(DB) as con:
        df.to_sql("sales",con,if_exists="replace",index=False)
        con.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region)")
    report = {"input_rows":input_rows,"clean_rows":len(df),"removed_rows":input_rows-len(df)}
    (OUT/"data_quality_report.txt").write_text("\\n".join(f"{k}: {v}" for k,v in report.items()))
    return df, report

if __name__ == "__main__":
    data, report = run_pipeline()
    print("ETL completed:", report)
