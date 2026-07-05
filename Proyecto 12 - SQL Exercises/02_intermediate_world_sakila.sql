-- =============================================================================
--  PROJECT 12 · SQL EXERCISES — INTERMEDIATE LEVEL
--  Databases: World, Sakila (MySQL sample databases)
--  Topics: INNER JOIN, multi-table JOIN, GROUP BY, HAVING, LIMIT, Aliases
--  Author: Enmanuel Jiménez
-- =============================================================================


-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION A — World Database
-- ─────────────────────────────────────────────────────────────────────────────
USE world;

-- Quick exploration
SELECT * FROM city    LIMIT 10;
SELECT * FROM country LIMIT 10;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 1 · Cities and their countries
-- Goal: JOIN city ↔ country using the CountryCode foreign key.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    city.name    AS city,
    country.name AS country
FROM city
INNER JOIN country ON city.CountryCode = country.Code
ORDER BY country.name ASC, city.name ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION B — Sakila Database
-- ─────────────────────────────────────────────────────────────────────────────
USE sakila;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 2 · Films and the actors who starred in them
-- Goal: JOIN film ↔ film_actor ↔ actor (many-to-many resolved via bridge table).
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    f.title                                         AS film_title,
    CONCAT(a.first_name, ' ', a.last_name)          AS actor_name
FROM film f
INNER JOIN film_actor fa ON f.film_id   = fa.film_id
INNER JOIN actor      a  ON fa.actor_id = a.actor_id
ORDER BY f.title ASC, a.last_name ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 3 · Films and their category
-- Goal: JOIN film ↔ film_category ↔ category (correct bridge table usage).
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    f.title         AS film_title,
    c.name          AS category
FROM film f
INNER JOIN film_category fc ON f.film_id      = fc.film_id
INNER JOIN category      c  ON fc.category_id = c.category_id
ORDER BY c.name ASC, f.title ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 4 · Staff full address (country → city → address)
-- Goal: Chain four JOINs to traverse a hierarchy of related tables.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    s.first_name AS first_name,
    s.last_name  AS last_name,
    ctry.country AS country,
    ci.city      AS city,
    a.address    AS address
FROM staff       s
JOIN address     a    ON s.address_id  = a.address_id
JOIN city        ci   ON a.city_id     = ci.city_id
JOIN country     ctry ON ci.country_id = ctry.country_id
ORDER BY s.last_name ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 5 · Top 10 customers by number of rentals
-- Goal: Use GROUP BY + COUNT(*) + ORDER BY + LIMIT to find the most active customers.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    COUNT(r.rental_id) AS total_rentals
FROM customer c
JOIN rental   r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_rentals DESC
LIMIT 10;
