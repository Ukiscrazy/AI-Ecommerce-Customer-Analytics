-- ============================================
-- AI E-Commerce Customer Analytics
-- Basic SQL Analysis
-- ============================================

-- 1. Total Customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- 2. Total Products
SELECT COUNT(*) AS total_products
FROM products;

-- 3. Total Orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- 4. Total Order Items
SELECT COUNT(*) AS total_order_items
FROM order_items;

-- 5. Total Revenue
SELECT ROUND(SUM(total_amount),2) AS total_revenue
FROM order_items;

-- 6. Average Order Value
SELECT ROUND(AVG(total_amount),2) AS average_order_value
FROM order_items;

-- 7. Top 10 Selling Products
SELECT
    p.product_name,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sold DESC
LIMIT 10;

-- 8. Top 10 Revenue Generating Products
SELECT
    p.product_name,
    ROUND(SUM(oi.total_amount),2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;