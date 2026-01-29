#!/bin/bash

# Script untuk verify dependencies dan troubleshoot common issues

echo "🔍 Checking Python version..."
python --version

echo ""
echo "📦 Checking installed packages..."
echo "================================"

# Critical packages
packages=(
    "fastapi"
    "uvicorn"
    "ultralytics"
    "opencv-python-headless"
    "langchain"
    "langchain-community"
    "langchain-core"
    "sentence-transformers"
    "faiss-cpu"
    "torch"
)

for package in "${packages[@]}"
do
    if python -c "import ${package//-/_}" 2>/dev/null; then
        echo "✅ $package - OK"
    else
        echo "❌ $package - MISSING"
    fi
done

echo ""
echo "🔍 Checking required files..."
echo "================================"

# Check model
if [ -f "model/best.pt" ]; then
    echo "✅ Model file exists: model/best.pt"
else
    echo "❌ Model file NOT FOUND: model/best.pt"
    echo "   Copy from: ../notebooks/runs/detect/train4/weights/best.pt"
fi

# Check RAG database
if [ -d "rag/sop_db" ]; then
    echo "✅ RAG database exists: rag/sop_db/"
else
    echo "❌ RAG database NOT FOUND: rag/sop_db/"
    echo "   Copy from notebook FAISS folder"
fi

echo ""
echo "🚀 Ready to start server!"
echo "Run: uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
