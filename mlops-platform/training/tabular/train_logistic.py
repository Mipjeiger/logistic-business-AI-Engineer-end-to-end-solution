import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
import os
from pathlib import Path

from sklearn.metrics import roc_auc_score, log_loss

# Import shared data utility
from training.tabular.data_utils import load_and_split_data
from training.common.mlflow_utils import promote_latest_to_prod_alias

# =========================
# CONFIG
# =========================
MODEL_NAME = "tabular_logistic"
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

with mlflow.start_run(run_name="logistic_regression"):
    model = LogisticRegression(
        max_iter=800,
        solver='lbfgs',
        n_jobs=-1,
        class_weight='balanced'
    )

    model.fit(X_train, y_train)

    # metrics training calculation
    val_probs = model.predict_proba(X_val)
    auc = roc_auc_score(y_val, val_probs[:, 1])
    val_logloss = log_loss(y_val, val_probs)
    train_logloss = log_loss(y_train, model.predict_proba(X_train))

    # =========================
    # LOGGING
    # =========================
    mlflow.log_metric("roc_auc", auc)
    mlflow.log_metric("validation_logloss", val_logloss)
    mlflow.log_metric("training_logloss", train_logloss)
    mlflow.log_params({
        "max_iter": 800,
        "solver": 'lbfgs',
        "n_jobs": -1,
        "l1_ratio": None,
        "class_weight": 'balanced'
    })

    # Log the correct code for mlflow.sklearn.log_model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=MODEL_NAME
    )

# Promote the latest model to Production stage
promote_latest_to_prod_alias(model_name=MODEL_NAME, alias="prod")