-- ===========================================
-- BUSINESS ANALYSIS
-- ===========================================

-- 1. Revenue by Category
SELECT
    p.category,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

------------------------------------------------

-- 2. Revenue by Brand
SELECT
    p.brand,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.brand
ORDER BY revenue DESC
LIMIT 10;

------------------------------------------------

-- 3. Top 10 Customers by Spending
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    ROUND(SUM(oi.total_amount),2) AS total_spent
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY total_spent DESC
LIMIT 10;

------------------------------------------------

-- 4. Orders by State
SELECT
    c.state,
    COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.state
ORDER BY total_orders DESC;

------------------------------------------------

-- 5. Average Spending per Customer
SELECT
ROUND(AVG(customer_total),2) AS avg_customer_spending
FROM
(
SELECT
customer_id,
SUM(total_amount) AS customer_total
FROM orders o
JOIN order_items oi
ON o.order_id=oi.order_id
GROUP BY customer_id
)t;