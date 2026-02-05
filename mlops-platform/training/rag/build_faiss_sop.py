# =====================================================
# Imports & logging
# =====================================================
import logging
import pickle
from pathlib import Path

import faiss
import mlflow
import mlflow.pyfunc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parents[2]

    faiss_dir = project_root / "notebooks" / "faiss_container_sop_db"

    index_path = faiss_dir / "index.faiss"
    meta_path = faiss_dir / "index.pkl"

    logger.info(f"FAISS index path: {index_path}")
    logger.info(f"FAISS meta path: {meta_path}")

    return index_path, meta_path


# =====================================================
# MLflow logging entrypoint
# =====================================================
def log_faiss_rag_model():
    index_path, meta_path = resolve_faiss_paths()

    with mlflow.start_run():
        mlflow.pyfunc.log_model(
            artifact_path="rag_model",
            python_model=FaissRAG(),
            artifacts={
                "index": str(index_path),
                "meta": str(meta_path),
            },
            registered_model_name="container_sop_faiss_rag_model",
        )

        logger.info("FAISS RAG model logged to MLflow successfully")