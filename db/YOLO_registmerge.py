import pandas as pd
from pathlib import Path
import os
import glob
import random
import numpy as np

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Load labels YOLO
labels_dir = os.path.join(DATA_DIR, "IMG_VALID", "*.txt")
labels = glob.glob(labels_dir)

# Load container registry CSV
registry_path = os.path.join(DATA_DIR, "container_registry.csv")
registry = pd.read_csv(registry_path)
registry_map = registry.set_index("image_name").to_dict(orient="index")

# Merging YOLO labels with container registry
rows = []

for label_file in labels:
    # Get filename without extension using os.path
    image_name = os.path.basename(label_file).replace(".txt", ".jpg")

    if image_name not in registry_map:
        continue

    meta = registry_map[image_name]

    with open(label_file) as f:
        for line in f:
            # YOLO format: class_id x_center y_center width height
            parts = line.strip().split()

            if len(parts) == 5:
                # Standard YOLO format (no confidence)
                cls, x, y, w, h = map(float, parts)
                # Generate random confidence between 0.75 - 0.99
                conf = round(random.uniform(0.75, 0.99), 3)
            elif len(parts) == 6:
                # YOLO format with confidence
                cls, x, y, w, h, conf = map(float, parts)
            else:
                print(f"⚠️ Skipping invalid line in {label_file}: {line.strip()}")
                continue

            area = w * h

            # appending data to rows list
            rows.append(
                {
                    "detection_id": None,
                    "image_name": image_name,
                    "shipment_id": meta["shipment_id"],
                    "container_id": meta["container_id"],
                    "class_id": int(cls),
                    "confidence": conf,
                    "bbox_x": x,
                    "bbox_y": y,
                    "bbox_w": w,
                    "bbox_h": h,
                    "bbox_area": area,
                    "detected_at": pd.Timestamp.now(),
                    "model_version": "yolo_v8",
                }
            )

df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA_DIR, "image_metadata.csv"), index=False)
print(f"✅ Merged YOLO labels with container registry. Total records: {len(df)}")
