import mlflow
import mlflow.sklearn
import lightgbm as lgb
import os
from pathlib import Path

from sklearn.metrics import roc_auc_score

# Import shared data utility
from training.tabular.data_utils import load_and_split_data
from training.common.mlflow_utils import promote_latest_to_prod_alias

# =========================
# CONFIG
# =========================
MODEL_NAME = "tabular_lightgbm"
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
if not os.getenv("MLFLOW_TRACKING_URI"):
    raise RuntimeError(
        "MLFLOW_TRACKING_URI is not set. "
        "Refusing to log to local mlruns."
    )

mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
mlflow.set_experiment(EXPERIMENT_NAME) # Set the experiment name

with mlflow.start_run(run_name="lightgbm"):
    model = lgb.LGBMClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5
    )

    model.fit(X_train, y_train)

    preds = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, preds)

    # =========================
    # LOGGING
    # =========================
    mlflow.log_metric("roc_auc", auc)
    mlflow.log_params({
        "n_estimators": 200,
        "learning_rate": 0.1,
        "max_depth": 5
    })

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=MODEL_NAME
    )

# Auto injected models
promote_latest_to_prod_alias(model_name=MODEL_NAME, alias="prod")