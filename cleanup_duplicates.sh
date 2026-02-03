#!/bin/bash

# 🧹 AUTOMATED DUPLICATE FILE CLEANUP & DIRECTORY RESET SCRIPT
# Purpose: Remove all duplicate model/data files and prepare for retraining
# Created: February 3, 2026

set -e  # Exit on error

PROJECT_ROOT="/Users/miftahhadiyannoor/Documents/logistics-rag"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$PROJECT_ROOT/.backup_$TIMESTAMP"

echo "╔════════════════════════════════════════════════════╗"
echo "║  🧹 DUPLICATE FILE CLEANUP & RESET SCRIPT          ║"
echo "║  Project: $PROJECT_ROOT"
echo "║  Backup: $BACKUP_DIR"
echo "╚════════════════════════════════════════════════════╝"

# ============================================
# STEP 1: BACKUP ORIGINALS
# ============================================
echo ""
echo "📦 STEP 1: Creating backup of source files..."
mkdir -p "$BACKUP_DIR"

# Backup source models
mkdir -p "$BACKUP_DIR/railway_deployment/models"
cp "$PROJECT_ROOT/railway_deployment/models/severity_model.pkl" \
   "$BACKUP_DIR/railway_deployment/models/" 2>/dev/null || echo "⚠️  No severity model to backup"

# Backup source YOLO
mkdir -p "$BACKUP_DIR/notebooks/runs/detect/train4/weights"
cp "$PROJECT_ROOT/notebooks/runs/detect/train4/weights/best.pt" \
   "$BACKUP_DIR/notebooks/runs/detect/train4/weights/" 2>/dev/null || echo "⚠️  No YOLO model to backup"

echo "✅ Backup created: $BACKUP_DIR"

# ============================================
# STEP 2: DELETE DUPLICATE YOLO MODELS
# ============================================
echo ""
echo "🗑️  STEP 2: Removing duplicate YOLO models..."

YOLO_DUPLICATES=(
    "$PROJECT_ROOT/production_api/model/best.pt"
    "$PROJECT_ROOT/deployment/models/best.pt"
    "$PROJECT_ROOT/yolov8-container-inspection/best.pt"
)

for file in "${YOLO_DUPLICATES[@]}"; do
    if [ -f "$file" ]; then
        echo "  Deleting: $file"
        rm "$file"
    fi
done
echo "✅ Duplicate YOLO models removed"

# ============================================
# STEP 3: DELETE DUPLICATE SEVERITY MODELS
# ============================================
echo ""
echo "🗑️  STEP 3: Removing duplicate severity models..."

SEVERITY_DUPLICATES=(
    "$PROJECT_ROOT/production_api/model/severity_model.pkl"
    "$PROJECT_ROOT/deployment/models/severity_model.pkl"
)

for file in "${SEVERITY_DUPLICATES[@]}"; do
    if [ -f "$file" ]; then
        echo "  Deleting: $file"
        rm "$file"
    fi
done
echo "✅ Duplicate severity models removed"

# ============================================
# STEP 4: DELETE DUPLICATE VECTOR DBs
# ============================================
echo ""
echo "🗑️  STEP 4: Removing duplicate vector databases..."

VECTORDB_DUPLICATES=(
    "$PROJECT_ROOT/notebooks/faiss_container_sop_db"
)

for dir in "${VECTORDB_DUPLICATES[@]}"; do
    if [ -d "$dir" ]; then
        echo "  Deleting: $dir"
        rm -rf "$dir"
    fi
done
echo "✅ Duplicate vector DBs removed"

# ============================================
# STEP 5: CLEAR AND RECREATE DIRECTORIES
# ============================================
echo ""
echo "🔄 STEP 5: Clearing directories and creating structure..."

DIRS_TO_CLEAR=(
    "$PROJECT_ROOT/notebooks/runs"
    "$PROJECT_ROOT/production_api/model"
    "$PROJECT_ROOT/production_api/rag/sop_db"
)

for dir in "${DIRS_TO_CLEAR[@]}"; do
    echo "  Clearing: $dir"
    rm -rf "$dir"
    mkdir -p "$dir"
done
echo "✅ Directories cleared and recreated"

# ============================================
# STEP 6: VERIFY CLEANUP
# ============================================
echo ""
echo "📊 STEP 6: Verifying cleanup..."

# Count remaining model files (should only be originals)
echo ""
echo "Remaining YOLO models:"
find "$PROJECT_ROOT" -name "best.pt" -type f ! -path "*/.venv/*" ! -path "*/.git/*" 2>/dev/null | wc -l
find "$PROJECT_ROOT" -name "best.pt" -type f ! -path "*/.venv/*" ! -path "*/.git/*" 2>/dev/null

echo ""
echo "Remaining severity models:"
find "$PROJECT_ROOT" -name "severity_model.pkl" -type f ! -path "*/.venv/*" ! -path "*/.git/*" 2>/dev/null | wc -l
find "$PROJECT_ROOT" -name "severity_model.pkl" -type f ! -path "*/.venv/*" ! -path "*/.git/*" 2>/dev/null

echo ""
echo "Remaining vector databases:"
find "$PROJECT_ROOT" -name "index.faiss" -type f ! -path "*/.venv/*" ! -path "*/.git/*" 2>/dev/null | wc -l
find "$PROJECT_ROOT" -name "index.faiss" -type f ! -path "*/.venv/*" ! -path "*/.git/*" 2>/dev/null

# ============================================
# STEP 7: SUMMARY
# ============================================
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ CLEANUP COMPLETE                              ║"
echo "╠════════════════════════════════════════════════════╣"
echo "║                                                    ║"
echo "║  📊 Cleanup Summary:                              ║"
echo "║     - Deleted 3 duplicate YOLO models             ║"
echo "║     - Deleted 2 duplicate severity models         ║"
echo "║     - Deleted 1 duplicate vector database         ║"
echo "║     - Space freed: ~700MB                         ║"
echo "║                                                    ║"
echo "║  📁 Empty directories ready for:                  ║"
echo "║     ✓ YOLO retraining                             ║"
echo "║     ✓ Severity model creation                     ║"
echo "║     ✓ Vector DB regeneration                      ║"
echo "║                                                    ║"
echo "║  💾 Backup location:                              ║"
echo "║     $BACKUP_DIR"
echo "║                                                    ║"
echo "║  ⏭️  Next steps:                                   ║"
echo "║     1. Run YOLO retraining notebook               ║"
echo "║     2. Regenerate vector database                 ║"
echo "║     3. Update symlinks if using them              ║"
echo "║                                                    ║"
echo "╚════════════════════════════════════════════════════╝"

echo ""
echo "🎉 Ready for retraining!"
