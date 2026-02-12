import os
import mlflow
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv

# =========================
# .Env Configuration
# =========================
BASE_DIR = os.path.dirname(__file__)
ENV_PATH = os.path.join(BASE_DIR, "..", "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

# =========================
# MLflow Configuration
# =========================
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
if MLFLOW_TRACKING_URI:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    print(f"MLflow Tracking URI is exists set to: {MLFLOW_TRACKING_URI}")
else:
    raise RuntimeError("MLFLOW_TRACKING_URI is not set in environment variables.")

# =========================
# MLflow bootstrap
# =========================
def setup_mlflow(experiment_name: str):
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name=experiment_name)

# =========================
# Auto promote to Production
# =========================
def promote_latest_to_prod_alias(model_name: str, alias: str = "prod"):
    client = MlflowClient()

    versions = client.get_latest_versions(model_name)
    if not versions:
        raise RuntimeError(f"No versions found for model {model_name}")
    
    latest = max(versions, key=lambda v: int(v.version))

    # Iterate through versions to find the latest 'Staging' version
    client.transition_model_version_stage(
        name=model_name,
        version=latest.version,
        stage="Production",
        archive_existing_versions=True # Concern to avoid multiple prod versions
    )
