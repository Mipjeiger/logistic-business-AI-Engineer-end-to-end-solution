import mlflow
import mlflow.sklearn
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import roc_auc_score

# Import shared data utility
from data_utils import load_and_split_data

# =========================
# CONFIG
# =========================
DATA_PATH = "../../data/tabular_cleaned.csv"
TARGET_COL = "damage_risk"

# =========================
# LOAD + SPLIT DATA
# =========================
X_train, X_val, y_train, y_val = load_and_split_data(
    path=DATA_PATH,
    target_col=TARGET_COL,
    test_size=0.2,
    random_state=42,
    stratify=True
)

# =========================
# TRAINING + MLFLOW
# =========================
mlflow.set_experiment("tabular-decisiontree") # Set the experiment name

with mlflow.start_run():
    model = DecisionTreeClassifier(
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, preds)

    # =========================
    # LOGGING
    # =========================
    mlflow.log_metric("roc_auc", auc)
    mlflow.log_param("max_depth", 5)

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="tabular_decisiontree"
    )