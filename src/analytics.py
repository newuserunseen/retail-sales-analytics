from pathlib import Path
import sqlite3
import pandas as pd

DB = Path(__file__).resolve().parents[1] / "output" / "retail_sales.db"

def query(sql, params=()):
    if not DB.exists():
        raise FileNotFoundError("Run `python run_pipeline.py` first.")
    with sqlite3.connect(DB) as con:
        return pd.read_sql_query(sql,con,params=params)

def kpis(where, params):
    return query(f"""SELECT SUM(net_revenue) revenue,
        COUNT(DISTINCT order_id) orders,
        AVG(net_revenue) avg_order_revenue,
        SUM(quantity) units FROM sales {where}""",params).iloc[0]

def monthly(where,params):
    return query(f"""SELECT order_month, ROUND(SUM(net_revenue),2) revenue
        FROM sales {where} GROUP BY order_month ORDER BY order_month""",params)

def by_category(where,params):
    return query(f"""SELECT category, ROUND(SUM(net_revenue),2) revenue
        FROM sales {where} GROUP BY category ORDER BY revenue DESC""",params)

def by_region(where,params):
    return query(f"""SELECT region, ROUND(SUM(net_revenue),2) revenue
        FROM sales {where} GROUP BY region ORDER BY revenue DESC""",params)

def by_customer(where,params):
    return query(f"""SELECT customer_type, ROUND(SUM(net_revenue),2) revenue,
        COUNT(DISTINCT order_id) orders FROM sales {where}
        GROUP BY customer_type""",params)
