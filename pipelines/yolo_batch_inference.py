import pandas as pd
import os
import glob
from PIL import Image

IMAGE_DIR = "../data/IMG_VALID"


# Load images path using glob
def load_image_paths(img_dir=IMAGE_DIR, num_images=None):
    image_paths = glob.glob(os.path.join(img_dir, "*.jpg"))
    print(f"Total Images: {len(image_paths)}")
    return image_paths[:num_images]


# Running YOLO batch for each images are recorded
def run_yolo_batch():

    records = []

    for img in os.listdir(IMAGE_DIR):

        container_id = img.split(".")[0]

        # MOCK RESULT(replace with YOLO output: Similar as JSON types)
        records.append(
            {
                "container_id": container_id,
                "damage_type": "dent",
                "severity_score": 3.2,
                "confidence": 0.91,
            }
        )

    try:
        df = pd.DataFrame(records)
        df.to_parquet("data/yolo_events.parquet")
        print(f"Total yolo comes are: {len(df)}")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error extracting YOLO: {e}")
