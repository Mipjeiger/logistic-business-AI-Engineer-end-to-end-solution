"""Generate Container Mapping from CV Inspection Results and Save to DB: (mapping image → shipment RANDOM / RULE BASED)"""

import pandas as pd
import os
import uuid
import glob
import random
from datetime import datetime

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Load shipment ids from SQL export CSV
shipments_path = os.path.join(DATA_DIR, "shipments.csv")
shipments = pd.read_csv(shipments_path)
shipments_ids = shipments["shipment_id"].astype(str).tolist()  # Fix from int to str

# Load images YOLO
images_dir = os.path.join(DATA_DIR, "IMG_VALID", "*.jpg")
images = glob.glob(images_dir)

rows = []

for img in images:
    image_name = img.split("/")[-1]

    shipment_id = random.choice(shipments_ids)
    container_id = f"CNT-{uuid.uuid4()}"

    # appending data to rows list
    rows.append(
        {
            "container_id": container_id,
            "shipment_id": shipment_id,
            "image_name": image_name,
            "captured_at": datetime.now(),
        }
    )

# Create DataFrame
df = pd.DataFrame(rows)
output_path = os.path.join(DATA_DIR, "container_registry.csv")
df.to_csv(output_path, index=False)

print(f"✅ Generated container registry with {len(df)} records.")
print(f"📁 Saved to: {output_path}")
