import os
import mlflow
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv

# Load .env variables from api/app/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../api/app/.env'))

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
def promote_latest_to_production(model_name: str):
    client = MlflowClient()

    versions = client.get_latest_versions(name=model_name)
    if not versions:
        raise RuntimeError(f"No versions found for model '{model_name}'")
    
    # Iterate through versions to find the latest 'Staging' version
    for v in versions:
        client.transition_model_version_stage(
            name=model_name,
            version=v.version,
            stage="Production",
            archive_existing_versions=True
        )