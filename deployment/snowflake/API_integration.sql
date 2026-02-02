-- create API Integration for snowflake
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION logistic_ext_access
ALLOWED_NETWORK_RULES = (allow_logistic_api)
ENABLED = TRUE;