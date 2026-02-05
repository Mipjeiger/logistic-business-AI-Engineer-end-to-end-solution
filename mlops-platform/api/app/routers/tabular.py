from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Create a router for tabular model endpoints
router = APIRouter(prefix="/tabular", tags=["tabular ML"])

# Place none variable for being injected from main.py
tabular_model = None

class TabularRequest(BaseModel):
    features: Dict[str, float]

class TabularResponse(BaseModel):
    prediction: int
    probability: float

# Create an endpoint for tabular model

@router.post("/tabular", response_model=TabularResponse)
def predict_tabular(payload: TabularRequest):
    if tabular_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        import pandas as pd

        X = pd.DataFrame([payload.features])
        proba = tabular_model.predict_proba(X)[0][1]
        pred = int(proba >= 0.5)

        return {
            "prediction": pred,
            "probability": round(float(proba), 4)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))