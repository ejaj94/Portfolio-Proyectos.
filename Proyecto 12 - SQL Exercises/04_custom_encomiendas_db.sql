-- =============================================================================
--  PROJECT 12 · SQL EXERCISES — FIRST ORIGINAL TABLE (DDL + DML)
--  Database: encomiendas (custom database — package deliveries)
--  Topics: CREATE DATABASE, CREATE TABLE, INSERT, SELECT
--  Author: Enmanuel Jiménez
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- SETUP · Create the database and select it
-- ─────────────────────────────────────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS encomiendas;
USE encomiendas;


-- ─────────────────────────────────────────────────────────────────────────────
-- DDL · Create the clients table
-- This table stores courier clients with the products they ship.
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cliente (
    numero   INT          AUTO_INCREMENT PRIMARY KEY  COMMENT 'Unique client number',
    nombre   VARCHAR(100) NOT NULL                    COMMENT 'Company or client name',
    producto VARCHAR(100) NOT NULL                    COMMENT 'Type of product shipped'
);


-- ─────────────────────────────────────────────────────────────────────────────
-- DML · Seed data — 16 real-world inspired clients
-- ─────────────────────────────────────────────────────────────────────────────
INSERT INTO cliente (nombre, producto) VALUES
    ('Zara',          'clothing'),
    ('Zara Home',     'home goods'),
    ('Auto Doc',      'car parts'),
    ('GLS Francia',   'miscellaneous'),
    ('Big Bazar',     'home articles'),
    ('Pull & Bear',   'clothing'),
    ('Temu',          'miscellaneous'),
    ('Shein',         'miscellaneous'),
    ('AliExpress',    'miscellaneous'),
    ('Oysho',         'clothing'),
    ('Rituals',       'home goods'),
    ('Amazon',        'miscellaneous'),
    ('Skulm',         'home goods'),
    ('Vidaxl',        'home goods'),
    ('Worten',        'electronics'),
    ('Vapor',         'vapes');


-- ─────────────────────────────────────────────────────────────────────────────
-- QUERIES · Practice retrieval on our own data
-- ─────────────────────────────────────────────────────────────────────────────

-- View all clients
SELECT * FROM cliente;

-- Count clients per product category
SELECT
    producto            AS product_category,
    COUNT(*)            AS total_clients
FROM cliente
GROUP BY producto
ORDER BY total_clients DESC;

-- Find all clients that ship clothing
SELECT numero, nombre
FROM cliente
WHERE producto = 'clothing'
ORDER BY nombre ASC;
