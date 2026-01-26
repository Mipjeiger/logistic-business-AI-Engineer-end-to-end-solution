import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variable from .env
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# Create postgresql db connection
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create postgreSQL db URI
DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def extract_business_data():
    """Extract business data from PostgreSQL database and save to parquet."""

    # Create SQLAlchemy engine
    engine = create_engine(DB_URI)

    query = """
    SELECT
        s.shipment_id,
        s.container_id,
        s.inspection_date,
        q.defect_rates,
        q.inspection_results,
        so.revenue_generated,
        so.shipping_costs,
        so.products_sold,
        p.product_type,
        sup.supplier_name
    FROM inspection.quality_inspections q
    JOIN logistics.shipments s ON q.shipment_id = s.shipment_id
    JOIN core.sales_orders so ON so.sales_id = s.sales_id
    JOIN core.products p ON so.product_id = p.product_id
    JOIN core.suppliers sup ON sup.supplier_id = p.supplier_id
    """

    try:
        # Use connection from engine with text() wrapper
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn)

        # Save to parquet
        output_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "business_features.parquet"
        )
        df.to_parquet(output_path, index=False)

        print(f"✅ Business data extracted and saved to {output_path}")
        print(f"Total rows: {len(df)}")
        print("\nPreview:")
        print(df.head())

        return df

    except Exception as e:
        print(f"❌ Error extracting business data: {e}")
        raise
    finally:
        engine.dispose()


# Usage

if __name__ == "__main__":
    extract_business_data()
