import mlflow
import mlflow.sklearn
from sklearn.tree import DecisionTreeClassifier
import os
from pathlib import Path

from sklearn.metrics import roc_auc_score

# Import shared data utility
from data_utils import load_and_split_data
from mlflow_utils import setup_mlflow, promote_latest_to_production

# =========================
# CONFIG
# =========================
MODEL_NAME = "tabular_decisiontree"
EXPERIMENT_NAME = "tabular-models"

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "tabular_cleaned.csv"
TARGET_COL = "damage_risk"

# =========================
# LOAD + SPLIT DATA
# =========================
X_train, X_val, y_train, y_val = load_and_split_data(
    path=DATA_PATH,
    target_column=TARGET_COL,
    test_size=0.2,
    random_state=42,
    stratify=True
)

# =========================
# TRAINING + MLFLOW
# =========================
setup_mlflow(EXPERIMENT_NAME)

with mlflow.start_run(run_name="decisiontree"):
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, preds)

    # =========================
    # LOGGING
    # =========================
    mlflow.log_metric("roc_auc", auc)
    mlflow.log_params({
        "max_depth": 5,
        "min_samples_leaf": 10
    })

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=MODEL_NAME
    )

# Promote the latest model to production
promote_latest_to_production(MODEL_NAME)