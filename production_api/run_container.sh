#!/bin/bash

# Script untuk menjalankan production_api container

echo "🚀 Starting production_api container..."

# Stop dan remove container lama jika ada
docker stop production_api-production 2>/dev/null
docker rm production_api-production 2>/dev/null

# Run container dengan volumes
docker run -d \
  --name production_api-production \
  -p 8000:8000 \
  -v "$(pwd)/uploads:/app/uploads" \
  -v "$(pwd)/outputs:/app/outputs" \
  -v "$(pwd)/model:/app/model" \
  -v "$(pwd)/rag:/app/rag" \
  --restart unless-stopped \
  production_api-production:latest

echo ""
echo "✅ Container started!"
echo "📡 API running on: http://localhost:8000"
echo "📄 Health check: http://localhost:8000/healthcheck"
echo ""
echo "📊 View logs with: docker logs -f production_api-production"
echo "🛑 Stop with: docker stop production_api-production"
