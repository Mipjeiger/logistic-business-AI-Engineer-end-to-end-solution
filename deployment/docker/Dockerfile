FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pastikan struktur folder tetap terjaga
COPY api/ ./api/
COPY models/severity_model.joblib ./models/severity_model.joblib

EXPOSE 8000

# Jika kamu menggunakan FastAPI/Uvicorn
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]