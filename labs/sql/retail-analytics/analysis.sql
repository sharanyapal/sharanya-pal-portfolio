-- 1. Monthly net revenue; refunded orders excluded.
SELECT substr(o.ordered_at,1,7) AS month, ROUND(SUM(i.quantity*p.unit_price),2) AS revenue
FROM orders o JOIN order_items i ON i.order_id=o.order_id JOIN products p ON p.product_id=i.product_id
WHERE o.status='paid' GROUP BY month ORDER BY month;

-- 2. Product category contribution.
SELECT p.category, COUNT(DISTINCT o.order_id) AS order_count, SUM(i.quantity*p.unit_price) AS revenue
FROM products p JOIN order_items i ON i.product_id=p.product_id JOIN orders o ON o.order_id=i.order_id
WHERE o.status='paid' GROUP BY p.category ORDER BY revenue DESC;

-- 3. Customer lifetime value and ranking using window functions.
WITH sales AS (
 SELECT c.customer_id,c.name,c.region,COALESCE(SUM(CASE WHEN o.status='paid' THEN i.quantity*p.unit_price ELSE 0 END),0) AS spend
 FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id
 LEFT JOIN order_items i ON i.order_id=o.order_id LEFT JOIN products p ON p.product_id=i.product_id
 GROUP BY c.customer_id,c.name,c.region
)
SELECT name,region,spend,DENSE_RANK() OVER (ORDER BY spend DESC) AS spending_rank FROM sales ORDER BY spending_rank;

-- 4. Rolling monthly revenue (window function).
WITH monthly AS (
 SELECT substr(o.ordered_at,1,7) AS month,SUM(i.quantity*p.unit_price) AS revenue
 FROM orders o JOIN order_items i ON o.order_id=i.order_id JOIN products p ON p.product_id=i.product_id
 WHERE o.status='paid' GROUP BY month
)
SELECT month,revenue,SUM(revenue) OVER (ORDER BY month ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS two_month_revenue FROM monthly;
