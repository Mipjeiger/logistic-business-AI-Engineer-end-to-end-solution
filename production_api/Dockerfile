FROM python:3.11-slim

# ----- System dependencies -----
RUN apt-get update && apt-get install -y \
    libgl1 \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ----- Set up working directory -----
WORKDIR /app

# ----- Copy requirements -----
COPY requirements.txt .

# ----- Install Python dependencies -----
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ----- Copy application code -----
COPY . .

# ----- Create Runtime Directory -----
RUN mkdir -p uploads outputs

# ----- Expose port -----
EXPOSE 8000

# ----- Start the application -----
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]