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

-- Create computer vision inspection feature mart
CREATE TABLE inspection.cv_detections (
    detection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    image_name TEXT,
    shipment_id TEXT,
    container_id TEXT,
    class_id TEXT,
    confidence FLOAT CHECK (confidence BETWEEN 0 AND 1),
    bbox_x_center FLOAT,
    bbox_y_center FLOAT,
    bbox_width FLOAT,
    bbox_height FLOAT,
    bbox_area FLOAT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_version TEXT DEFAULT 'yolo-v8'
);

-- insert data into cv_detections table
INSERT INTO inspection.cv_detections (
    image_name,
    shipment_id,
    container_id,
    class_id,
    confidence,
    bbox_x_center,
    bbox_y_center,
    bbox_width,
    bbox_height,
    bbox_area
)
VALUES (
    '10_20210526T020642376Z.jpg',
    'SHP001',
    'CNT001',
    'dent',
    0.82,
    0.51,
    0.63,
    0.12,
    0.18,
    0.0216
);

SELECT * FROM inspection.cv_detections;

-- create synthetic container registry table
CREATE TABLE logistics.container_registry (
    container_id TEXT PRIMARY KEY,
    shipment_id UUID REFERENCES logistics.shipments(shipment_id),
    image_name TEXT,
    captured_at TIMESTAMP
);

-- import registry container_registry data from CSV into SQL
COPY logistics.container_registry
FROM '/Users/miftahhadiyannoor/Documents/logistics-rag/data/container_registry.csv'
DELIMITER ','
CSV HEADER;

-- trunctable
TRUNCATE TABLE inspection.cv_detections;

-- Bulk insert data into container_registry table
COPY inspection.cv_detections(
    image_name,
    shipment_id,    
    container_id,
    class_id,
    confidence,
    bbox_x_center,
    bbox_y_center,
    bbox_width,
    bbox_height,
    bbox_area,
    detected_at,
    model_version
)
FROM '/Users/miftahhadiyannoor/Documents/logistics-rag/data/image_metadata_cleaned.csv'
DELIMITER ','
CSV HEADER;

-- validate data
SELECT shipment_id, COUNT(*)
FROM inspection.cv_detections
GROUP BY shipment_id
LIMIT 10;

-- create inspection feature mart
CREATE TABLE inspection.feature_mart AS
SELECT
  shipment_id,

  COUNT(*) AS total_detections,

  AVG(confidence) AS avg_confidence,

  SUM(bbox_area) AS total_damage_area,

  SUM(CASE WHEN class_id = 'dent' THEN 1 ELSE 0 END) AS dent_count

FROM inspection.cv_detections
GROUP BY shipment_id;


-- feature mart join
SELECT
    s.shipment_id,
    p.product_type,
    sup.supplier_name,

    f.total_damage_area,
    f.total_detections,
    f.avg_confidence,

    q.defect_rate

FROM inspection.feature_mart f

JOIN logistics.shipments s
  ON f.shipment_id = s.shipment_id

JOIN core.products p
  ON s.product_id = p.product_id

JOIN core.suppliers sup
  ON s.supplier_id = sup.supplier_id

JOIN inspection.quality_inspections q
  ON p.product_id = q.product_id;

SELECT COUNT(*) FROM inspection.cv_detections;
SELECT COUNT(*) FROM inspection.feature_mart;

-- Create Machine Learning Engineer dataset

-- create ml_engineer schema
CREATE SCHEMA IF NOT EXISTS ml;

-- create ml_engineer dataset view
CREATE OR REPLACE VIEW ml.inspection_training AS
SELECT
    s.shipment_id,

    f.total_detections,
    f.avg_confidence,
    f.total_damage_area,
    f.dent_count,

    q.defect_rate,

    CASE
      WHEN q.defect_rate > 0.23 THEN 1
      ELSE 0
    END AS is_high_risk

FROM inspection.feature_mart f
JOIN logistics.shipments s ON f.shipment_id = s.shipment_id
JOIN inspection.quality_inspections q ON s.product_id = q.product_id;

-- validate ml view
SELECT * FROM ml.inspection_training LIMIT 10;

-- list of queries to select data from all tables
SELECT * FROM core.products;
SELECT * FROM core.suppliers;
SELECT * FROM core.inventory_status;
SELECT * FROM core.sales_orders;
SELECT * FROM core.production_metrics;
SELECT * FROM logistics.shipments;
SELECT * FROM inspection.quality_inspections;
SELECT * FROM logistics.container_registry;
SELECT * FROM inspection.feature_mart;
SELECT * FROM inspection.cv_detections;
SELECT * FROM ml.inspection_training;