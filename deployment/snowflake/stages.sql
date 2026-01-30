-- create snowflake stage storage for logistic data
CREATE OR REPLACE STAGE logistic_stage;
LIST @logistic_stage;


USE DATABASE supply_chain;