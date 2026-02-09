#!/bin/bash
set -e

python3 training/tabular/train_logistic.py
python3 training/tabular/train_xgboost.py
python3 training/yolo/train_yolov8.py
python3 training/rag/build_faiss_sop.py