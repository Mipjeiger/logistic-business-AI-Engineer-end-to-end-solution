from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os
import pathlib
import logging
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = pathlib.Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Initialize FastAPI app ---

app = FastAPI()
model = joblib.load(
    os.path.join(BASE_DIR, "models", "severity_model.joblib")
)  # Load the model at startup


# Define the input data model
class InputData(BaseModel):
    features: list
    question: str


# --- Define API endpoints ---
@app.post("/predict")
async def predict(data: InputData):
    try:
        X = np.array(data.features).reshape(1, -1)
        score = float(model.predict_proba(X)[0][1])  # Assuming binary classification

        # Simulation RAG + LLM response
        response = {
            "risk_score": score,
            "llm_answer": f"Shipment risk score is {score:.2f} for the question: {data.question}",
        }

        return response
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return {"error": "Prediction failed."}


@app.get("/health")
async def health():
    return {"status": "ok"}
