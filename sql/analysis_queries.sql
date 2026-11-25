-- Run after: python run_pipeline.py
-- SQLite database: output/retail_sales.db

-- Overall KPIs
SELECT COUNT(DISTINCT order_id) AS orders,
       SUM(quantity) AS units,
       ROUND(SUM(net_revenue),2) AS net_revenue
FROM sales;

-- Monthly revenue trend
SELECT order_month, ROUND(SUM(net_revenue),2) AS revenue
FROM sales GROUP BY order_month ORDER BY order_month;

-- Regional performance
SELECT region, ROUND(SUM(net_revenue),2) AS revenue
FROM sales GROUP BY region ORDER BY revenue DESC;

-- Category performance
SELECT category, SUM(quantity) AS units,
       ROUND(SUM(net_revenue),2) AS revenue
FROM sales GROUP BY category ORDER BY revenue DESC;

-- New vs returning customers
SELECT customer_type, COUNT(*) AS orders,
       ROUND(SUM(net_revenue),2) AS revenue
FROM sales GROUP BY customer_type;

-- Rank categories by revenue (window function)
SELECT category, SUM(net_revenue) AS revenue,
       DENSE_RANK() OVER (ORDER BY SUM(net_revenue) DESC) AS revenue_rank
FROM sales GROUP BY category;
