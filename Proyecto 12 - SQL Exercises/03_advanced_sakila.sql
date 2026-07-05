-- =============================================================================
--  PROJECT 12 · SQL EXERCISES — ADVANCED LEVEL
--  Database: Sakila (MySQL sample database)
--  Topics: Multi-table JOINs, GROUP BY + SUM/COUNT, Subqueries, Window Functions
--  Author: Enmanuel Jiménez
-- =============================================================================

USE sakila;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 1 · Total sales and transaction count grouped by amount and date
-- Goal: Practice aggregate functions (SUM, COUNT) with GROUP BY on multiple columns.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    amount,
    DATE(payment_date)      AS payment_day,
    SUM(amount)             AS total_sales,
    COUNT(*)                AS total_transactions
FROM payment
GROUP BY amount, DATE(payment_date)
ORDER BY amount ASC, total_sales DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 2 · Total payments and rentals per store, broken down by film category
-- Goal: Chain 6 tables using JOINs; aggregate across two dimensions (store + category).
--
-- Tables involved:
--   payment → rental → inventory → film_category → category
--                    ↘ store (via inventory.store_id)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    i.store_id                  AS store,
    c.name                      AS film_category,
    SUM(p.amount)               AS total_revenue,
    COUNT(r.rental_id)          AS total_rentals
FROM payment      p
JOIN rental       r  ON p.rental_id      = r.rental_id
JOIN inventory    i  ON r.inventory_id   = i.inventory_id
JOIN film_category fc ON i.film_id       = fc.film_id
JOIN category     c  ON fc.category_id  = c.category_id
GROUP BY i.store_id, c.name
ORDER BY store ASC, total_revenue DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 3 · Film language popularity by customer city
-- Goal: Join 8 tables end-to-end; aggregate revenue and rental count
--       per language–city combination.
--
-- Chain: language → film → inventory → rental → payment
--                                    → customer → address → city
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    l.name                  AS film_language,
    ci.city                 AS customer_city,
    COUNT(r.rental_id)      AS total_rentals,
    SUM(p.amount)           AS total_revenue
FROM language     l
JOIN film         f  ON l.language_id   = f.language_id
JOIN inventory    i  ON f.film_id       = i.film_id
JOIN rental       r  ON i.inventory_id  = r.inventory_id
JOIN payment      p  ON r.rental_id     = p.rental_id
JOIN customer     cu ON r.customer_id   = cu.customer_id
JOIN address      a  ON cu.address_id   = a.address_id
JOIN city         ci ON a.city_id       = ci.city_id
GROUP BY l.name, ci.city
ORDER BY total_revenue DESC
LIMIT 50;


-- ─────────────────────────────────────────────────────────────────────────────
-- BONUS · Top 5 most rented film categories (subquery approach)
-- Goal: Demonstrate an alternative with a subquery to rank categories.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    category_name,
    total_rentals
FROM (
    SELECT
        c.name                  AS category_name,
        COUNT(r.rental_id)      AS total_rentals
    FROM category     c
    JOIN film_category fc ON c.category_id  = fc.category_id
    JOIN inventory     i  ON fc.film_id     = i.film_id
    JOIN rental        r  ON i.inventory_id = r.inventory_id
    GROUP BY c.name
) ranked
ORDER BY total_rentals DESC
LIMIT 5;
