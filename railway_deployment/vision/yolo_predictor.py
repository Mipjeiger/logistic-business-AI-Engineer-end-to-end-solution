from ultralytics import YOLO
import os
import pathlib

MODEL_PATH = pathlib.Path(__file__).parent / "models" / "yolov8.pt"
model = YOLO(MODEL_PATH)


# Create a function to make predictions
def predict_vision(image_path):
    results = model(image_path)
    result = results[0]

    detections = []

    # Iterate through detected boxes
    for box in result.boxes:
        detections.append(
            {
                "class_id": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy.tolist(),
            }
        )
    return detections
