"""Create SQL pipeline to train severity dataset for production deployment ready logistic regression model"""

import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# ======================== CONFIGURATION ========================
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(env_path)

# Retrieve database connection parameters from environment variables
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
DB_NAME = os.getenv("DB_NAME")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Create Snowflake connection string
connection_string = f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/{DB_NAME}/{SNOWFLAKE_SCHEMA}"
engine = create_engine(connection_string)

# Create model path configuration
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "production_api", "model", "severity_model.joblib"
)

# ======================== DATA RETRIEVAL ========================
# SQL query to retrieve training data
query = """
SELECT
    m.defect_"""
