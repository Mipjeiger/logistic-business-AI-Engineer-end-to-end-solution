from fastapi import FastAPI
from app.model_loader import load_model
from app.routers import tabular, yolo, rag
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models at startup
    tabular.tabular_model = {model: load_model(model) for model in ["tabular_lightgbm", "tabular_xgboost", "tabular_decisiontree", "tabular_logistic"]}
    rag.rag_model = load_model("container_sop_faiss_rag_model")
    yolo.yolo_model = load_model("container_yolov8_multi_task_model")

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(tabular.router)
app.include_router(rag.router)
app.include_router(yolo.router)