import streamlit as st
import pandas as pd
import plotly.express as px
from src.etl import run_pipeline, DB
from src.analytics import query, kpis, monthly, by_category, by_region, by_customer

st.set_page_config(page_title="Retail Sales Analytics",page_icon="📊",layout="wide")
st.title("Retail Sales Analytics Dashboard")
st.caption("Python • Pandas • SQL • SQLite • Streamlit | Synthetic portfolio dataset")

if not DB.exists():
    run_pipeline()

bounds=query("SELECT MIN(order_date) lo, MAX(order_date) hi FROM sales").iloc[0]
st.sidebar.header("Filters")
date_range=st.sidebar.date_input("Order date range",(pd.to_datetime(bounds.lo).date(),pd.to_datetime(bounds.hi).date()))
regions=query("SELECT DISTINCT region FROM sales ORDER BY region").region.tolist()
cats=query("SELECT DISTINCT category FROM sales ORDER BY category").category.tolist()
r=st.sidebar.multiselect("Region",regions,default=regions)
c=st.sidebar.multiselect("Category",cats,default=cats)
if isinstance(date_range,tuple) and len(date_range)==2: start,end=date_range
else: start,end=pd.to_datetime(bounds.lo).date(),pd.to_datetime(bounds.hi).date()
clauses=["order_date BETWEEN ? AND ?"]; params=[str(start),str(end)]
if r: clauses.append("region IN ("+",".join("?" for _ in r)+")"); params+=r
else: clauses.append("1=0")
if c: clauses.append("category IN ("+",".join("?" for _ in c)+")"); params+=c
else: clauses.append("1=0")
where="WHERE "+" AND ".join(clauses); params=tuple(params)
k=kpis(where,params)
a,b,d,e=st.columns(4)
a.metric("Net revenue",f"₹{(k['revenue'] or 0):,.0f}")
b.metric("Orders",f"{int(k['orders'] or 0):,}")
d.metric("Avg. revenue / order",f"₹{(k['avg_order_revenue'] or 0):,.0f}")
e.metric("Units sold",f"{int(k['units'] or 0):,}")
x,y=st.columns(2)
m=monthly(where,params); cat=by_category(where,params)
with x:
    st.subheader("Monthly revenue")
    if not m.empty: st.plotly_chart(px.line(m,x="order_month",y="revenue",markers=True),use_container_width=True)
with y:
    st.subheader("Revenue by category")
    if not cat.empty: st.plotly_chart(px.bar(cat,x="category",y="revenue"),use_container_width=True)
x,y=st.columns(2)
reg=by_region(where,params); cust=by_customer(where,params)
with x:
    st.subheader("Revenue by region")
    if not reg.empty: st.plotly_chart(px.bar(reg,x="region",y="revenue"),use_container_width=True)
with y:
    st.subheader("New vs returning customers")
    if not cust.empty: st.plotly_chart(px.pie(cust,names="customer_type",values="revenue",hole=.4),use_container_width=True)
st.subheader("Filtered transactions")
detail=query(f"SELECT order_id,order_date,region,category,product,quantity,unit_price,discount,net_revenue FROM sales {where} ORDER BY order_date DESC",params)
st.dataframe(detail,use_container_width=True,hide_index=True)
st.download_button("Download cleaned transactions",detail.to_csv(index=False).encode(), "filtered_sales.csv","text/csv")
with st.expander("Dataset and metric definitions"):
    st.write("The included data is synthetic and created only for this portfolio project.")
    st.write("Net revenue = quantity × unit price × (1 − discount). Average revenue/order = net revenue ÷ unique orders.")
