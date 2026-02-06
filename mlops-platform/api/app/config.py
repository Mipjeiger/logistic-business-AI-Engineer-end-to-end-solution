from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    """Central configuration for MLOps Platform API."""
    # =========================
    # Environment
    # =========================
    ENV: Literal["local", "dev", "staging", "prod"] = Field(
        "local",
        description="Runtime environment"
    )

    # =========================
    # MLflow
    # =========================
    MLFLOW_TRACKING_URI: str = Field(
        "http://host.docker.internal:5015",
        description="MLflow Tracking URI"
    )

    MLFLOW_MODEL_STAGE: Literal["Production", "Staging", "None"] = Field(
        "Production",
        description="MLflow model stage to load"
    )

    # =========================
    # Registered Model Names
    # =========================
    TABULAR_MODEL_NAME: Literal[
        "tabular_decisiontree",
        "tabular_logistic",
        "tabular_lightgbm",
        "tabular_xgboost",
    ] = Field(
        "tabular_lightgbm",
        description="Active tabular model name"
    )

    RAG_MODEL_NAME: str = Field(
        "container_sop_faiss_rag_model",
        description="Registered FAISS RAG model name"
    )

    YOLO_MODEL_NAME: str = Field(
        "container_yolov8_multi_task_model",
        description="Registered YOLOv8 model name"
    )

    # =========================
    # Performance
    # =========================
    MODEL_LOAD_TIMEOUT: int = Field(
        120,
        description="Timeout (seconds) for MLflow model loading"
    )

    # pydantic v2 style setting source (code changed in v2)
    model_config = {
        "env_file": "api/app/.env",
        "env_file_encoding": "utf-8",
    }

# Singleton setting object
settings = Settings()