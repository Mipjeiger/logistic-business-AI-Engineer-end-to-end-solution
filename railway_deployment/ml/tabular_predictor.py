import joblib
import os
import pathlib

MODEL_PATH = pathlib.Path(__file__).parent / "models" / "severity_model.joblib"
model = joblib.load(MODEL_PATH)


# Create a function to make predictions
def predict_tabular(payload: dict):
    features = list(payload.values())
    prediction = model.predict([features])
    return prediction[0]
