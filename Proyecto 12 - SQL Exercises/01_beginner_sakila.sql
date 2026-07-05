-- =============================================================================
--  PROJECT 12 · SQL EXERCISES — BEGINNER LEVEL
--  Database: Sakila (MySQL sample database)
--  Topics: SELECT, WHERE, ORDER BY, BETWEEN, LIKE
--  Author: Enmanuel Jiménez
-- =============================================================================

USE sakila;

-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 0 · Explore the actors table
-- Goal: See all columns and rows before filtering.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT * FROM actor;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 1 · Actors ordered by last name
-- Goal: Retrieve only the name columns and sort alphabetically.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    first_name  AS first_name,
    last_name   AS last_name
FROM actor
ORDER BY last_name ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 2 · Actors named "Scarlett"
-- Goal: Filter rows with an exact match on first_name.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    actor_id,
    first_name,
    last_name
FROM actor
WHERE first_name = 'Scarlett';


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 3 · Films with duration between 80 and 100 minutes
-- Goal: Use BETWEEN for a range filter on a numeric column.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    title,
    length AS duration_minutes
FROM film
WHERE length BETWEEN 80 AND 100
ORDER BY length ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 4 · Customers whose last name starts with "S" and first name ends with "N"
-- Goal: Combine two LIKE patterns with AND.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    first_name,
    last_name,
    email
FROM customer
WHERE last_name  LIKE 'S%'
  AND first_name LIKE '%N';


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 5 · Films rated "PG"
-- Goal: Filter on an ENUM column and project only relevant fields.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    film_id,
    title,
    rating,
    length AS duration_minutes,
    rental_rate
FROM film
WHERE rating = 'PG'
ORDER BY title ASC;
