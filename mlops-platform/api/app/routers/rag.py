"""FAISS-based SOP RAG Router Module."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Create a router for RAG model endpoints
router = APIRouter(prefix="/rag", tags=["RAG"])

# Injected from main.py
rag_model = None

class RAGRequest(BaseModel):
    query: str

class RAGResponse(BaseModel):
    answer: str

# Create an endpoint for RAG model
@router.post("/query", response_model=RAGResponse)
async def query_rag(payload: RAGRequest):
    if rag_model is None:
        raise HTTPException(status_code=500, detail="RAG Model not loaded")
    
    try:
        result = rag_model.predict(payload.query)
        return {
            "answer": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))