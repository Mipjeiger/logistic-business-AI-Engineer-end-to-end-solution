LIST @logistic_stage; -- verification

-- create call external API for snowflake network integration
CREATE OR REPLACE NETWORK RULE model_api_rule
MODE = EGRESS
TYPE = HOST_PORT
VALUE_LIST = 

SHOW SERVICES;