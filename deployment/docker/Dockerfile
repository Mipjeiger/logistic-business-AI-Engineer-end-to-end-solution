FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
ARG PIP_DEFAULT_TIMEOUT=300
RUN pip install --default-timeout=${PIP_DEFAULT_TIMEOUT} --no-cache-dir -r requirements.txt

# Ensure the models directory exists
COPY deployment/api/ ./api/
COPY deployment/models/severity_model.joblib /app/models/severity_model.joblib

EXPOSE 8000

# Jika kamu menggunakan FastAPI/Uvicorn
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]