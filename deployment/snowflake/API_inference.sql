-- show snowflake services
SHOW SERVICES;
LIST @logistic_stage; -- verification

LIST @logistic_stage; -- verification

-- create call external API for snowflake network integration egress
CREATE OR REPLACE NETWORK RULE allow_logistic_api
MODE = EGRESS
TYPE = HOST_PORT
VALUE_LIST = ('logistic-api-inference-production.up.railway.app');

SHOW SERVICES;

-- Create External Access Integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION logistic_ext_access
ALLOWED_NETWORK_RULES = (allow_logistic_api)
ENABLED = TRUE;


CREATE OR REPLACE PROCEDURE logistic_predict(text STRING)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.10'
PACKAGES = ('requests')
HANDLER = 'run'
EXTERNAL_ACCESS_INTEGRATIONS = (logistic_ext_access)
AS
$$
import requests

API_URL = "https://logistic-api-inference-production.up.railway.app/predict"
API_KEY = "logistic-prod-123456"

def run(session, text):

    payload = {
        "text": text
    }

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    return response.json()
$$;

-- call usage
CALL logistic_predict("How many cost of shipment to Jakarta-Bandung?")

-- Mengatur Role ke ACCOUNTADMIN
USE ROLE ACCOUNTADMIN;

-- Mengatur Warehouse ke COMPUTE_WH
USE WAREHOUSE COMPUTE_WH;

-- Mengatur Database ke ENGINEERING_PLATFORM
USE DATABASE ENGINEERING_PLATFORM;

-- Mengatur Schema ke PUBLIC
USE SCHEMA PUBLIC;