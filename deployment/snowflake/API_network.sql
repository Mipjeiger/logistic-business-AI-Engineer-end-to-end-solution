LIST @logistic_stage; -- verification

-- create call external API for snowflake network integration
CREATE OR REPLACE NETWORK RULE allow_logistic_api
MODE = EGRESS
TYPE = HOST_PORT
VALUE_LIST = ('logistic-api-inference-production.up.railway.app');

SHOW SERVICES;

-- Create External Access Integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION model_api_integration
ALLOWED_NETWORK_RULES = (model_api_rule)
ENABLED = TRUE;