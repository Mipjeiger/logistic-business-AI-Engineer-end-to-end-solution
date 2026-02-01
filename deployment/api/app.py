from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import shutil
import os
import torch
import cv2
import numpy as np
import joblib


from ultralytics import YOLO

# RAG + HuggingFace
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Slack notifier
from slack.thresholds import classify_alert, apply_class_weight
from slack.notifier import send_alert

# ------------------- CONFIG -------------------- #

MODEL_PATH = "model/best.pt"
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
RAG_PATH = "rag/sop_db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

CLASS_MAP = {0: "dent", 1: "rust", 2: "broken_door", 3: "leak"}


# ------------------- DEVICE AUTO DETECT -------------------- #

if torch.cuda.is_available():
    DEVICE = "cuda"
elif torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"
print("Running on device:", DEVICE)


# ------------------- LOAD YOLO MODEL -------------------- #

print("Loading YOLOv8 Model...")
model = YOLO(MODEL_PATH)
model.to(DEVICE)
model.fuse()  # Performance optimization

# ------------------- LOAD MACHINE LEARNING MODEL -------------------- #

print("Loading Severity Model...")
severity_model = joblib.load("model/severity_model.joblib")

# ------------------- LOAD RAG -------------------- #

print("Loading High-quality Embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("Loading SOP RAG FAISS Database...")
sop_db = FAISS.load_local(
    RAG_PATH,
    embeddings=embeddings,
    allow_dangerous_deserialization=True,
)

print("Setup Complete.")


# ------------------- FASTAPI SETUP -------------------- #

app = FastAPI(
    title="Container Damage Detection API",
    description="YOLOv8 + Risk Engine + SOP RAG System API",
    version="1.0.0",
)


# ------------------- UTILS -------------------- #


def extract_features(result):

    counts = {
        "dent": 0,
        "rust": 0,
        "broken_door": 0,
        "leak": 0,
    }

    if result.boxes is None:
        return counts, 0

    for cls in result.boxes.cls:
        name = CLASS_MAP[int(cls)]
        counts[name] += 1

    severity = (
        counts["dent"] * 1
        + counts["rust"] * 2
        + counts["broken_door"] * 3
        + counts["leak"] * 4
    )

    return counts, severity


def calculate_risk_level(severity):

    if severity >= 5:
        return "HIGH"
    elif severity >= 2:
        return "MEDIUM"
    else:
        return "LOW"


def get_sop_recommendation(risk, count):

    query = f"""
    Container damage inspection SOP.
    Risk Level: {risk}
    Damage summary count: {count}
    What is recommendation action for provide this case?
    """

    docs = sop_db.similarity_search(query, k=2)
    sop_text = "\n".join([d.page_content for d in docs])

    return sop_text


# Create slack notification function
def process_slack_alert(result, image_name, img_shape):
    """YOLO → Feature extraction → Severity model → Threshold → Slack"""

    if result.boxes is None:
        return

    h, w = img_shape[:2]
    img_area = h * w

    # -----------------------------
    # Aggregate image-level feature
    # -----------------------------

    total_boxes = len(result.boxes)
    confidences = []
    area_ratios = []
    class_names = []

    for box in result.boxes:

        cls_id = int(box.cls[0])
        label = CLASS_MAP[cls_id]

        confidence = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0]
        box_area = float(
            (x2 - x1) * (y2 - y1)
        )  # Gradient calculation for bounding box area
        bbox_area_ratio = box_area / img_area

        confidences.append(confidence)
        area_ratios.append(bbox_area_ratio)
        class_names.append(label)

    # -----------------------------
    # Build severity features
    # SAME FORMAT AS TRAINING
    # -----------------------------

    avg_confidence = sum(confidences) / len(confidences)
    total_damage_area = sum(area_ratios)
    detection_count = total_boxes

    # Create feature array
    features = np.array([[avg_confidence, total_damage_area, detection_count]])

    # -----------------------------
    # Severity model inference
    # -----------------------------

    base_score = severity_model.predict(features)[0]

    # -----------------------------
    # Class weight application
    # -----------------------------

    dominant_class = max(set(class_names), key=class_names.count)
    final_score = apply_class_weight(
        base_score,
        dominant_class,
    )

    # -----------------------------
    # Threshold decision
    # -----------------------------

    alert_level = classify_alert(final_score)

    # -----------------------------
    # Slack trigger
    # -----------------------------

    if alert_level:
        send_alert(
            shipment_id=image_name,
            severity_score=final_score,
            alert_level=alert_level,
            class_name=dominant_class,
        )


# ------------------- VIDEO PROCESSOR -------------------- #


def process_video(video_path, output_path):

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_counts = {
        "dent": 0,
        "rust": 0,
        "broken_door": 0,
        "leak": 0,
    }

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        results = model.predict(
            source=frame,
            conf=0.4,
            imgsz=640,
            device=DEVICE,
            verbose=False,
        )

        result = results[0]

        annotated_frame = result.plot()
        out.write(annotated_frame)

        if result.boxes is not None:
            for cls in result.boxes.cls:
                name = CLASS_MAP[int(cls)]
                total_counts[name] += 1

    cap.release()
    out.release()

    severity = (
        total_counts["dent"] * 1
        + total_counts["rust"] * 2
        + total_counts["broken_door"] * 3
        + total_counts["leak"] * 4
    )

    return total_counts, severity, frame_count


# ------------------- API ENDPOINTS -------------------- #


@app.get("/health")
async def healthcheck():
    return JSONResponse(content={"status": "ok"}, status_code=200)


# ------------------- IMAGE JSON RESULT -------------------- #


@app.post("/inspect-image")
async def inspect_image(
    file: UploadFile = File(...), background_tasks: BackgroundTasks = None
):

    # ---------- VALIDATION ---------- #
    if file is None:
        raise HTTPException(
            status_code=400,
            detail="File is required. Use multipart/form-data with field name 'file'.",
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only image files allowed.",
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- SAFE IMAGE LOAD ---------- #

    image = cv2.imread(file_path)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="OpenCV failed to read image. Possibly corrupted file.",
        )

    results = model.predict(
        source=image,
        conf=0.4,
        imgsz=640,
        device=DEVICE,
        verbose=False,
    )
    result = results[0]

    # ---------- RISK ENGINE ---------- #

    counts, severity = extract_features(result)
    risk = calculate_risk_level(severity)
    sop_recommendation = get_sop_recommendation(risk, counts)

    # ---------- REGISTER BACKGROUND TASK FOR SLACK ALERT ---------- #
    if background_tasks:
        background_tasks.add_task(
            process_slack_alert,
            result=result,
            image_name=file.filename,
            img_shape=image.shape,
        )

    # ---------- RESPONSE ---------- #
    # User will get immediate response while Slack alert is processed in background
    return {
        "filename": file.filename,
        "damage_counts": counts,
        "severity_score": severity,
        "risk_level": risk,
        "sop_recommendation": sop_recommendation,
    }


# ------------------- IMAGE VISUAL -------------------- #


@app.post("/inspect-image-visual")
async def inspect_image_visual(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model.predict(
        source=file_path,
        conf=0.4,
        imgsz=640,
        device=DEVICE,
    )

    result = results[0]  # ingesting result from results are modeled as list
    image = cv2.imread(file_path)

    # Create slack alert
    process_slack_alert(
        result=result,
        image_name=file.filename,
        img_shape=image.shape,
    )

    annotated_path = f"{OUTPUT_DIR}/annotated_{file.filename}"
    result.save(filename=annotated_path)

    return FileResponse(annotated_path, media_type="image/jpeg")


# ------------------- VIDEO INSPECTION -------------------- #


@app.post("/inspect-video")
async def inspect_video(file: UploadFile = File(...)):

    input_path = f"{UPLOAD_DIR}/{file.filename}"
    output_path = f"{OUTPUT_DIR}/result_{file.filename}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    counts, severity, frames = process_video(input_path, output_path)

    if severity >= 5:
        send_alert(
            image_name=file.filename,
            label="Video Inspection Alert Summary",
            confidence=1.0,
            bbox_area_ratio=severity / 10,
        )

    risk = calculate_risk_level(severity)
    sop_recommendation = get_sop_recommendation(risk, counts)

    return {
        "filename": file.filename,
        "frames_processed": frames,
        "damage_summary": counts,
        "severity_score": severity,
        "risk_level": risk,
        "sop_recommendation": sop_recommendation,
        "annotated_video_path": output_path,
    }


# ------------------- DOWNLOAD VIDEO -------------------- #


@app.get("/download-video/{video_name}")
def download_video(video_name: str):

    video_path = f"{OUTPUT_DIR}/{video_name}"

    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=video_name,
    )


# ------------------- RUN APP -------------------- #

if __name__ == "__main__":

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
