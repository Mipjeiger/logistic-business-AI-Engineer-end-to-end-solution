from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Central configuration for MLOps Platform API."""
    # =========================
    # Environment
    # =========================
    ENV: str = Field("local", description="Environment: local, dev, staging, prod")

    # =========================
    # MLflow
    # =========================
    MLFLOW_TRACKING_URI: str = Field(
        "http://localhost:5015",
        description="MLflow Tracking URI"
    )

    MLFLOW_MODEL_STAGE: str = Field(
        "Production",
        description="MLflow Model Stage to load"
    )

    # =========================
    # Registered Model Names
    # =========================
    TABULAR_MODEL_NAME: str = Field(
        "tabular_decisiontree",
        "tabular_lightgbm",
        "tabular_xgboost",
        "tabular_logistic",
        description="Registered name of the tabular multi class models in MLflow"
    )

    RAG_MODEL_NAME: str = Field(
        "container_sop_rag",
        description="Registered MLflow model for FAISS RAG"
    )

    YOLO_MODEL_NAME: str = Field(
        "container_damage_classifier",
        description="Registered MLflow YOLOv8 model"
    )

    # =========================
    # Performance
    # =========================
    MODEL_LOAD_TIMEOUT: int = Field(
        120,
        description="Timeout in seconds for model loading"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"