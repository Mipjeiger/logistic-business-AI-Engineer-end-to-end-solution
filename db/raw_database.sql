CREATE TABLE raw.supply_chain_data (
    order_id UUID PRIMARY KEY,
    availability INT,
    costs NUMERIC(12,4),
    customer_demographics TEXT,
    defect_rates FLOAT,
    inspection_results TEXT,
    lead_time INT,
    lead_times INT,
    location TEXT,
    manufacturing_costs NUMERIC(12,4),
    manufacturing_lead_time INT,
    number_of_products_sold INT,
    order_quantities INT,
    price NUMERIC(10,4),
    product_type TEXT,
    production_volumes INT,
    revenue_generated NUMERIC(14,4),
    routes TEXT,
    shipping_carriers TEXT,
    shipping_costs NUMERIC(10,4),
    shipping_times INT,
    stock_levels INT,
    supplier_name TEXT,
    transportation_modes TEXT
);

DROP TABLE raw.supply_chain_data;

-- load csv data into raw.supply_chain_data table
-- Gunakan file yang sudah dimodifikasi dengan UUID valid
COPY raw.supply_chain_data
FROM '/Users/miftahhadiyannoor/Documents/logistics-rag/data/supply_chain_data_expanded.csv'
DELIMITER ','
CSV HEADER;

-- Create staging table for supply chain data
CREATE TABLE staging.stg_supply_chain_data AS
SELECT
    order_id,
    availability,
    costs,
    customer_demographics,
    defect_rates,
    inspection_results,
    lead_time,
    lead_times,
    location,
    manufacturing_costs,
    manufacturing_lead_time,
    number_of_products_sold,
    order_quantities,
    price,
    product_type,
    production_volumes,
    revenue_generated,
    routes,
    shipping_carriers,
    shipping_costs,
    shipping_times,
    stock_levels,
    supplier_name,
    transportation_modes
FROM raw.supply_chain_data;

DROP TABLE staging.stg_supply_chain_data;

--validate data in staging table
SELECT * FROM staging.stg_supply_chain_data;
