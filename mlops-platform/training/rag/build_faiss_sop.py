# =====================================================
# Imports & logging
# =====================================================
import logging
import pickle
from pathlib import Path

import faiss
import mlflow
import mlflow.pyfunc

from mlflow_utils import setup_mlflow, promote_latest_to_production

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_NAME = "container_sop_faiss_rag_model"
EXPERIMENT_NAME = "rag-models"

# =====================================================
# MLflow PyFunc Model
# =====================================================
class FaissRAG(mlflow.pyfunc.PythonModel):
    """
    FAISS-based RAG model (index + metadata)
    """

    def load_context(self, context):
        """
        Load FAISS index and metadata from MLflow artifacts
        """
        logger.info("Loading FAISS artifacts from MLflow context")

        self.index = faiss.read_index(context.artifacts["index"])
        with open(context.artifacts["meta"], "rb") as f:
            self.meta = pickle.load(f)

        logger.info("FAISS index and metadata loaded successfully")

    def predict(self, context, query):
        """
        query: str | list[str]
        (Embedding + FAISS search logic goes here)
        """
        raise NotImplementedError("Embedding + FAISS search not implemented yet")


# =====================================================
# Resolve artifact paths (LOGGING ONLY)
# =====================================================
def resolve_faiss_paths():
    """
    Resolve local paths for MLflow artifact logging.
    These paths are NOT used during inference.
    """
    project_root = Path(__file__).resolve().parents[2]
    faiss_dir = project_root / "notebooks" / "faiss_container_sop_db"
    return faiss_dir / "index.faiss", faiss_dir / "index.pkl"


# =====================================================
# MLflow logging entrypoint
# =====================================================
def log_faiss_rag_model():
    
    setup_mlflow(EXPERIMENT_NAME) # Setup MLflow experiment

    index_path, meta_path = resolve_faiss_paths()

    with mlflow.start_run(run_name="faiss-rag"):
        mlflow.pyfunc.log_model(
            artifact_path="rag_model",
            python_model=FaissRAG(),
            artifacts={
                "index": str(index_path),
                "meta": str(meta_path),
            },
            registered_model_name=MODEL_NAME,
        )

        logger.info("FAISS RAG model logged to MLflow successfully")

    # Promote latest model to Production
    promote_latest_to_production(MODEL_NAME)
    logger.info(f"Latest model for '{MODEL_NAME}' promoted to Production")