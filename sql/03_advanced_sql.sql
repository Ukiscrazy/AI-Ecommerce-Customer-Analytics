-- =====================================================
-- ADVANCED SQL ANALYSIS
-- =====================================================

--------------------------------------------------------
-- 1. Monthly Revenue Trend
--------------------------------------------------------
SELECT
    DATE_TRUNC('month', o.order_date) AS month,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

--------------------------------------------------------
-- 2. Customer Lifetime Value (CLV)
--------------------------------------------------------
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    ROUND(SUM(oi.total_amount),2) AS customer_lifetime_value
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY customer_lifetime_value DESC
LIMIT 20;

--------------------------------------------------------
-- 3. Top 5 Products in Each Category
--------------------------------------------------------
WITH ProductSales AS
(
    SELECT
        p.category,
        p.product_name,
        SUM(oi.quantity) AS quantity_sold,
        RANK() OVER
        (
            PARTITION BY p.category
            ORDER BY SUM(oi.quantity) DESC
        ) AS product_rank
    FROM products p
    JOIN order_items oi
    ON p.product_id = oi.product_id
    GROUP BY
        p.category,
        p.product_name
)
SELECT *
FROM ProductSales
WHERE product_rank <= 5;

--------------------------------------------------------
-- 4. Running Revenue
--------------------------------------------------------
SELECT
    o.order_date,
    SUM(oi.total_amount) AS daily_revenue,
    SUM(SUM(oi.total_amount))
    OVER
    (
        ORDER BY o.order_date
    ) AS running_revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY o.order_date
ORDER BY o.order_date;

--------------------------------------------------------
-- 5. Repeat Customers
--------------------------------------------------------
SELECT
    customer_id,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) > 1
ORDER BY total_orders DESC;