CREATE TABLE core.products (
    product_id UUID PRIMARY KEY,
    product_type VARCHAR(50),
    price NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SCHEMA IF NOT EXISTS core;

DROP TABLE core.products;



-- insert data into products table
INSERT INTO core.products (product_id, product_type, price)
SELECT DISTINCT
    order_id,
    product_type,
    price
FROM staging.stg_supply_chain_data;

SELECT * FROM core.products;