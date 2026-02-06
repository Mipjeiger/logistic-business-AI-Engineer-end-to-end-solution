import mlflow
from functools import lru_cache
from mlflow.exceptions import MlflowException

from app.config import settings

# =========================
# MLflow setup (ONCE)
# =========================
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)


# =========================
# Safe, cached model loader
# =========================
@lru_cache(maxsize=8)
def load_model(model_name: str):
    """
    Load MLflow model safely with caching.
    
    Args:
        model_name (str): Registered MLflow model name.
        
    Returns:
        Loaded MLflow Pyfunc model.
    """
    model_uri = f"models:/{model_name}/{settings.MLFLOW_MODEL_STAGE}"

    try:
        return mlflow.pyfunc.load_model(model_uri=model_uri)
    except MlflowException as e:
        raise RuntimeError(
            f"Failed to load MLflow model: {model_uri}. "
            f"Check registry, stage, and MLflow connectivity."
        ) from e