from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import shutil
import pandas as pd
import numpy as np
import joblib
import os

# -----------------------------
# App
# -----------------------------
app = FastAPI(title="Container Risk Inspection API")

# -----------------------------
# Image folder setup
# -----------------------------
IMAGE_FOLDER = "uploaded_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# -----------------------------
# Load artifacts at startup
# -----------------------------
df_features = pd.read_parquet("df_features.parquet")
df_images = pd.read_parquet("df_images.parquet")

FEATURES = [
    "total_detections",
    "avg_confidence",
    "total_damage_area",
    "dent_count",
    "defect_rate"
]

# Load all models from models/ directory
models = {}
for filename in os.listdir("models"):
    if filename.endswith(".pkl"):
        name = filename.replace(".pkl", "")
        models[name] = joblib.load(f"models/{filename}")

print(f"Loaded models: {list(models.keys())}")

# -----------------------------
# Request schema
# -----------------------------
class PredictionRequest(BaseModel):
    image_name: str

# -----------------------------
# Helper: YOLO (mock for now)
# -----------------------------
def run_yolo_stub(row):
    return {
        "damage_detected": True,
        "confidence": 0.9,
        "bbox_count": int(row.total_detections),
        "classes": ["dent"] if row.dent_count > 0 else []
    }

# -----------------------------
# Helper: RAG reasoning (safe)
# -----------------------------
def generate_rag_reasoning(avg_risk, yolo_conf):
    if avg_risk >= 0.7 and yolo_conf >= 0.7:
        return (
            "Based on multiple model predictions and high-confidence visual damage detection, "
            "the container is likely compromised and should not proceed with shipping "
            "until further inspection or repair."
        )
    elif avg_risk < 0.5 and yolo_conf < 0.5:
        return (
            "Model predictions and visual inspection indicate low risk. "
            "The container may proceed with shipping under standard monitoring."
        )
    else:
        return (
            "The assessment shows mixed indicators. Further manual inspection "
            "is recommended before making a shipping decision."
        )
    

# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/predict")
def predict(request: PredictionRequest):
    image_name = request.image_name

    # 1. Resolve shipment_id
    match = df_images[df_images["image_name"] == image_name]
    if match.empty:
        raise HTTPException(status_code=500, detail="Image not found")
    
    shipment_id = match.iloc[0]["shipment_id"]

    # 2. Get shipment features
    row = df_features[df_features["shipment_id"] == shipment_id]
    if row.empty:
        raise HTTPException(status_code=500, detail="Shipment features not found")
    
    row = row.iloc[0]
    X = row[FEATURES].values.reshape(1, -1)

    # 3. Run all models
    model_results = {}
    probs = []

    for name, model in models.items():
        prob = float(model.predict_proba(X)[0, 1])
        probs.append(prob)

        model_results[name] = {
            "risk_probability": round(prob, 3),
            "decision": "HIGH_RISK" if prob >= 0.5 else "LOW_RISK"
        }

    avg_risk = float(np.mean(probs))

    # 4. YOLO evidence
    yolo_result = run_yolo_stub(row)

    # 5. RAG reasoning
    rag_text = generate_rag_reasoning(
        avg_risk=avg_risk,
        yolo_conf=yolo_result["confidence"]
    )

    # 6. Final JSON
    return {
        "image": image_name,
        "shipment_id": shipment_id,

        "models": model_results,

        "model_consesus": {
            "average_risk_probability": round(avg_risk, 3),
            "final_decision": "HIGH_RISK" if avg_risk >= 0.5 else "LOW_RISK"
        },

        "detection_yolo": yolo_result,

        "rag_assesment": {
            "summary": rag_text,
            "recommendation": "DO NOT SHIP" if avg_risk >= 0.5 else "SAFE TO SHIP"
        }
    }

# ------------------------------
# Predicting image upload endpoint
# ------------------------------
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):

    # 1. Save uploaded file
    image_name = file.filename
    image_path = os.path.join(IMAGE_FOLDER, image_name)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Resolve shipment_id
    match = df_images[df_images["image_name"] == image_name]
    if match.empty:
        raise HTTPException(status_code=500, detail="Image not found")
    
    shipment_id = match.iloc[0]["shipment_id"]

    # 3. Load shipment features
    row = df_features[df_features["shipment_id"] == shipment_id]
    if row.empty:
        raise HTTPException(status_code=500, detail="Shipment features not found")
    
    row = row.iloc[0]
    X = row[FEATURES].values.reshape(1, -1)

    # 4. Run all models
    model_results = {}
    probs = []

    for name, model in models.items():
        prob = float(model.predict_proba(X)[0, 1])
        probs.append(prob)

        model_results[name] = {
            "risk_probability": round(prob, 3),
            "decision": "HIGH_RISK" if prob >= 0.5 else "LOW_RISK"
        }

    avg_risk = float(np.mean(probs))

    # 5. YOLO evidence
    yolo_result = run_yolo_stub(row)

    # 6. RAG reasoning
    rag_text = generate_rag_reasoning(
        avg_risk=avg_risk,
        yolo_conf=yolo_result["confidence"]
    )

    # 7. Cleanup uploaded file
    os.remove(image_path)

    # 8. Final JSON
    return {
        "image": image_name,
        "shipment_id": shipment_id,

        "models": model_results,

        "model_consensus": {
            "average_risk_probability": round(avg_risk, 3),
            "final_decision": "HIGH_RISK" if avg_risk >= 0.5 else "LOW_RISK"
        },

        "detection_yolo": yolo_result,

        "rag_assessment": {
            "summary": rag_text,
            "recommendation": (
                "DO NOT SHIP" if avg_risk >= 0.5 else "SAFE TO SHIP"
            )
        }
    }



# -----------------------------
# Health check endpoint
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}