-- =============================================================================
--  PROJECT 12 · SQL EXERCISES — WORLD DATABASE EXPLORATION
--  Database: World (MySQL sample database)
--  Topics: SELECT, WHERE, ORDER BY, Multiple filters on countrylanguage table
--  Author: Enmanuel Jiménez
-- =============================================================================

USE world;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 1 · Countries where Portuguese is spoken
-- Goal: Basic filter on a language column.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT CountryCode
FROM countrylanguage
WHERE language = 'Portuguese'
ORDER BY CountryCode ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 2 · Countries where Spanish is spoken by at least 30% of the population
-- Goal: Combine a string filter (language) with a numeric filter (Percentage).
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    CountryCode,
    Percentage
FROM countrylanguage
WHERE language  = 'Spanish'
  AND Percentage >= 30
ORDER BY Percentage DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 3 · All languages ordered by official status, then by percentage
-- Goal: ORDER BY two columns — a boolean-like column first, then a numeric one.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    CountryCode,
    language,
    IsOfficial,
    Percentage
FROM countrylanguage
ORDER BY IsOfficial DESC, Percentage DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 4 · Languages spoken in Venezuela (VEN)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    CountryCode,
    language,
    IsOfficial,
    Percentage
FROM countrylanguage
WHERE CountryCode = 'VEN'
ORDER BY Percentage DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 5 · Languages spoken in Portugal (PRT)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    CountryCode,
    language,
    IsOfficial,
    Percentage
FROM countrylanguage
WHERE CountryCode = 'PRT'
ORDER BY Percentage DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- EXERCISE 6 · Languages spoken in the United States (USA)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    CountryCode,
    language,
    IsOfficial,
    Percentage
FROM countrylanguage
WHERE CountryCode = 'USA'
ORDER BY Percentage DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- BONUS · Compare all three countries side by side
-- Goal: Use IN() to filter multiple country codes in a single query.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    CountryCode,
    language,
    IsOfficial,
    ROUND(Percentage, 1) AS percentage_spoken
FROM countrylanguage
WHERE CountryCode IN ('VEN', 'PRT', 'USA')
ORDER BY CountryCode ASC, Percentage DESC;
