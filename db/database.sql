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

-- Query for suppliers
CREATE TABLE core.suppliers (
    supplier_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_name VARCHAR(100),
    location TEXT
);

-- insert data into suppliers table
INSERT INTO core.suppliers (supplier_name, location)
SELECT DISTINCT
    supplier_name,
    location
FROM staging.stg_supply_chain_data;

SELECT * FROM core.suppliers;

-- query for invetory status
CREATE TABLE core.inventory_status (
    inventory_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES core.products(product_id),
    stock_levels INT,
    availability INT,
    recorded_at DATE DEFAULT CURRENT_DATE
);

-- insert data into inventory_status table
INSERT INTO core.inventory_status (product_id, stock_levels, availability)
SELECT
    order_id,
    stock_levels,
    availability
FROM staging.stg_supply_chain_data;
SELECT * FROM core.inventory_status;

-- query for sales order
CREATE TABLE core.sales_orders (
    sales_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES core.products(product_id),
    products_sold INT,
    revenue_generated NUMERIC(12,2),
    order_date DATE DEFAULT CURRENT_DATE
);

-- insert data into sales_orders table
INSERT INTO core.sales_orders (product_id, products_sold, revenue_generated)
SELECT
    order_id,
    number_of_products_sold,
    revenue_generated
FROM staging.stg_supply_chain_data;

SELECT * FROM core.sales_orders;

-- query for production metrics
CREATE TABLE core.production_metrics (
    production_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES core.products(product_id),
    production_volumes INT,
    manufacturing_cost NUMERIC(12,2),
    manufacturing_lead_time INT,
    recorded_at DATE DEFAULT CURRENT_DATE
);

-- insert data into production_metrics table
INSERT INTO core.production_metrics
(product_id, production_volumes, manufacturing_cost, manufacturing_lead_time)
SELECT
    order_id,
    production_volumes,
    manufacturing_costs,
    manufacturing_lead_time
FROM staging.stg_supply_chain_data;

-- query for shipments
CREATE TABLE logistics.shipments (
    shipment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES core.products(product_id),
    supplier_id UUID REFERENCES core.suppliers(supplier_id),
    shipping_carrier TEXT,
    transportation_mode TEXT,
    route TEXT,
    shipping_cost NUMERIC(10,2),
    total_cost NUMERIC(12,2),
    shipping_time INT,
    shipped_at DATE DEFAULT CURRENT_DATE
);

-- insert data into shipments table
INSERT INTO logistics.shipments
(product_id, supplier_id, shipping_carrier, transportation_mode,
 route, shipping_cost, total_cost, shipping_time)
SELECT
    r.order_id,
    s.supplier_id,
    r.shipping_carriers,
    r.transportation_modes,
    r.routes,
    r.shipping_costs,
    r.costs,
    r.shipping_times
FROM staging.stg_supply_chain_data r
JOIN core.suppliers s
ON r.supplier_name = s.supplier_name;
SELECT * FROM logistics.shipments;

-- query for quality inspection
CREATE TABLE inspection.quality_inspections (
    inspection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES core.products(product_id),
    inspection_result TEXT,
    defect_rate FLOAT,
    lead_time INT,
    inspected_at DATE DEFAULT CURRENT_DATE
);

-- insert data into quality_inspections table
INSERT INTO inspection.quality_inspections (product_id, inspection_result, defect_rate, lead_time)
SELECT
    order_id,
    inspection_results,
    defect_rates,
    lead_time
FROM staging.stg_supply_chain_data;

SELECT * FROM inspection.quality_inspections;


-- list of queries to select data from all tables
SELECT * FROM core.products;
SELECT * FROM core.suppliers;
SELECT * FROM core.inventory_status;
SELECT * FROM core.sales_orders;
SELECT * FROM core.production_metrics;
SELECT * FROM logistics.shipments;
SELECT * FROM inspection.quality_inspections;