from fastapi import FastAPI, UploadFile, File
import shutil
import os
from ml.tabular_predictor import predict_tabular
from vision.yolo_predictor import predict_vision
from llm.rag_pipeline import query_llm

app = FastAPI(title="Mutli Model Inference API")

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


# ---------------- TABULAR ML ----------------
@app.post("/predict/vision")
async def vision_predict(file: UploadFile = File(...)):
    path = f"{TEMP_DIR}/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_vision(path)
    os.remove(path)

    return {"status": "success", "model": "yolov8", "predictions": result}


# ---------------- LLM RAG ----------------
@app.post("/predict/llm")
async def llm_predict(prompt: str):
    response = query_llm(prompt)
    return {"status": "success", "model": "RAG-LLM", "response": response}


# Railway needs this
@app.get("/")
def health():
    return {"status": "API is running"}
