FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

COPY app ./app

ENV MLFLOW_TRACKING_URI=http://mlflow:5015

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]