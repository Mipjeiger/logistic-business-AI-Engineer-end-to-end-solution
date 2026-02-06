from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict
import tempfile
import shutil
import os

from app.model_loader import load_model
from app.config import settings

router = APIRouter(prefix="/detect", tags=["YOLOv8"])


@router.post("/yolo")
async def detect_yolo(file: UploadFile = File(...)) -> List[Dict]:
    try:
        yolo_model = load_model(settings.YOLO_MODEL_NAME)

        suffix = os.path.splitext(file.filename)[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        results = yolo_model.predict(tmp_path)

        detections = []
        for box in results[0].boxes:
            detections.append({
                "class_id": int(box.cls),
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist(),
            })

        return detections

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)