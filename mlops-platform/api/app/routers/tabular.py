from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

import pandas as pd

from app.model_loader import load_model
from app.config import settings

router = APIRouter(prefix="/tabular", tags=["tabular ML"])


class TabularRequest(BaseModel):
    features: Dict[str, float]


class TabularResponse(BaseModel):
    prediction: int
    probability: float


@router.post("/predict", response_model=TabularResponse)
def predict_tabular(payload: TabularRequest):
    try:
        model = load_model(settings.TABULAR_MODEL_NAME)

        X = pd.DataFrame([payload.features])
        proba = float(model.predict_proba(X)[0][1])
        pred = int(proba >= 0.5)

        return {
            "prediction": pred,
            "probability": round(proba, 4),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health_check():
    try:
        _ = load_model(settings.TABULAR_MODEL_NAME)
        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))