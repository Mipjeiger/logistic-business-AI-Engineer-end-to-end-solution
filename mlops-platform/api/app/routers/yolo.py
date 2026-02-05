from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict
import tempfile
import shutil
import os

router=APIRouter(prefix="/detect", tags=["YOLOv8"])

# Injected from main.py
yolo_model = None

@router.post("/yolo")
async def detect_yolo(file: UploadFile = File(...)) -> List[Dict]:
    if yolo_model is None:
        raise HTTPException(status_code=500, detail="YOLO Model not loaded")

    suffix = os.path.splitext(file.filename)[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        results = yolo_model.predict(
            source=tmp_path,
            conf=0.10,
            imgsz=640,
            verbose=False
        )

        detections = []

        for box in results[0].boxes:
            detections.append({
                "class_id": int(box.cls),
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist()
            })

        return detections
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        os.remove(tmp_path)