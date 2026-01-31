import joblib
import os
import pathlib

# Create a base directory path
BASE_DIR = pathlib.Path(__file__).parent.parent
MODEL_PATH = os.path.join(BASE_DIR, "deployment", "models", "severity_model.joblib")

_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


print(f"Model is ready and ready to deploy from: {MODEL_PATH}")
