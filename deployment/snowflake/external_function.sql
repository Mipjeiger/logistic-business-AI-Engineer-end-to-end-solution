-- Create External Function wrapper
CREATE OR REPLACE EXTERNAL FUNCTION logistic_rag_api(features ARRAY, question STRING)
RETURNS VARIANT
API_INTEGRATION = model_api_integration
AS '';


-- Call external function from snowflake
SELECT logistic_rag_api(
    ARRAY_CONSTRUCT(45,2,12000,3).
    'Why shipment is delayed?'
)