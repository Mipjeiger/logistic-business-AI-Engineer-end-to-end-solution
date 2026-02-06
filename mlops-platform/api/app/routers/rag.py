"""FAISS-based SOP RAG Router Module."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.model_loader import load_model
from app.config import settings

# Create a router for RAG model endpoints
router = APIRouter(prefix="/rag", tags=["RAG"])

class RAGRequest(BaseModel):
    query: str


class RAGResponse(BaseModel):
    answer: str


@router.post("/query", response_model=RAGResponse)
def query_rag(payload: RAGRequest):
    try:
        rag_model = load_model(settings.RAG_MODEL_NAME)
        result = rag_model.predict(payload.query)

        return {"answer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))