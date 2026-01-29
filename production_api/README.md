# Container Damage Detection API

Production-ready FastAPI service untuk deteksi kerusakan container menggunakan YOLOv8 + RAG System.

## 🚀 Features

- **YOLOv8 Object Detection** - Deteksi 4 tipe kerusakan (dent, rust, broken_door, leak)
- **Risk Engine** - Kalkulasi severity dan risk level
- **RAG System** - Rekomendasi SOP menggunakan FAISS + LangChain
- **Video Processing** - Support untuk image & video input
- **Auto Device Detection** - CUDA / MPS / CPU

## 📋 Prerequisites

- Python 3.11
- Docker (optional)
- Model YOLOv8 (`model/best.pt`)
- FAISS Database (`rag/sop_db/`)

## 🛠️ Installation

### Option 1: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Docker

```bash
# Build image
docker build -t container-damage-api .

# Run container
docker run -p 8000:8000 container-damage-api
```

## 📦 Dependencies

### Core Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `ultralytics` - YOLOv8 model
- `torch` - Deep learning framework

### LangChain & RAG
- `langchain` - Main framework
- `langchain-community` - **REQUIRED** for FAISS integration
- `langchain-core` - Core components
- `sentence-transformers` - Text embeddings
- `faiss-cpu` - Vector database

### Computer Vision
- `opencv-python-headless` - Image/video processing
- `pillow` - Image handling

## 🔧 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'langchain_community'`

**Solusi:**
Pastikan `langchain-community` terinstall di `requirements.txt`:

```txt
langchain-community==1.2.7
```

Ini adalah package terpisah dari `langchain` dan **WAJIB** untuk menggunakan:
- `langchain_community.vectorstores.FAISS`
- `langchain_community.embeddings.HuggingFaceEmbeddings`

### Error: Docker build gagal

**Solusi:**
1. Pastikan semua dependencies ada di `requirements.txt`
2. Gunakan `opencv-python-headless` untuk Docker (bukan `opencv-python`)
3. Rebuild dengan `--no-cache`:
   ```bash
   docker build --no-cache -t container-damage-api .
   ```

## 📡 API Endpoints

### Health Check
```bash
GET /healthcheck
```

### Image Inspection (JSON Response)
```bash
POST /inspect-image
Content-Type: multipart/form-data

file: <image_file>
```

### Image Inspection (Annotated Image)
```bash
POST /inspect-image-visual
Content-Type: multipart/form-data

file: <image_file>
```

### Video Processing
```bash
POST /inspect-video
Content-Type: multipart/form-data

file: <video_file>
```

## 📊 Response Format

```json
{
  "damage_count": {
    "dent": 3,
    "rust": 2,
    "broken_door": 0,
    "leak": 0
  },
  "severity_score": 7,
  "risk_level": "MEDIUM",
  "sop_recommendation": "..."
}
```

## 🐳 Docker Configuration

File `Dockerfile` sudah dikonfigurasi dengan:
- Python 3.11-slim base image
- System dependencies (libgl1, ffmpeg)
- Auto-create upload/output directories
- Expose port 8000

## 📝 Notes

- Model path: `model/best.pt` (copy dari `notebooks/runs/detect/train4/weights/best.pt`)
- RAG database: `rag/sop_db/` (copy dari notebook FAISS folder)
- Default confidence threshold: 0.4
- Default image size: 640x640

## 🔐 Environment Variables

Tidak ada environment variables yang required untuk saat ini. Semua konfigurasi hardcoded di `app.py`.

## 📚 References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
