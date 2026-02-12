# =====================================================
# Imports & logging
# =====================================================
import logging
import pickle
from pathlib import Path

import faiss
import os
import mlflow
import mlflow.pyfunc
import numpy as np

from training.common.mlflow_utils import promote_latest_to_prod_alias

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
# Compute FAISS metrics
# =====================================================
def compute_faiss_metrics(index_path, meta_path):
    """
    Compute FAISS index metrics (e.g., index size, number of vectors)
    """
    # Load index
    index = faiss.read_index(str(index_path))
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)

    # Basic metrics
    num_vectors = index.ntotal
    dimension = index.d

    # Index size
    index_size_mb = index_path.stat().st_size / (1024 * 1024)
    meta_size_mb = meta_path.stat().st_size / (1024 * 1024)

    # Performance test (optional - sample search)
    if num_vectors > 0:
        import time
        import random
        # Create random query vector
        query_vector = np.random.randn(1, dimension).astype('float32')

        # Measure search time
        start_time = time.time()
        distances, indices  = index.search(query_vector, k=10)
        search_time_ms = (time.time() - start_time) * 1000
    else:
        search_time_ms = 0

    return {
        "num_vectors": num_vectors,
        "dimension": dimension,
        "index_size_mb": round(index_size_mb, 2),
        "meta_size_mb": round(meta_size_mb, 2),
        "total_size_mb": round(index_size_mb + meta_size_mb, 2),
        "avg_search_time_ms": round(search_time_ms, 2)
    }

# =====================================================
# Resolve artifact paths (LOGGING ONLY)
# =====================================================
def resolve_faiss_paths():
    """
    Resolve local paths for MLflow artifact logging.
    These paths are NOT used during inference.
    """
    project_root = Path(__file__).resolve().parents[3]
    faiss_dir = project_root / "notebooks" / "faiss_container_sop_db"
    return faiss_dir / "index.faiss", faiss_dir / "index.pkl"


# =====================================================
# MLflow logging entrypoint
# =====================================================
def log_faiss_rag_model():
    index_path, meta_path = resolve_faiss_paths()

    # Compute metrics
    metrics = compute_faiss_metrics(index_path=index_path, meta_path=meta_path)

    if not os.getenv("MLFLOW_TRACKING_URI"):
        raise RuntimeError(
            "MLFLOW_TRACKING_URI is not set. // wrong set .env"
        )
    
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    mlflow.set_experiment(EXPERIMENT_NAME) # Set the experiment name

    with mlflow.start_run(run_name="faiss_rag_index"):
        # Log metrics
        mlflow.log_metrics("num_vectors", metrics["num_vectors"])
        mlflow.log_metrics("dimension", metrics["dimension"])
        mlflow.log_metrics("index_size_mb", metrics["index_size_mb"])
        mlflow.log_metrics("meta_size_mb", metrics["meta_size_mb"])
        mlflow.log_metrics("total_size_mb", metrics["total_size_mb"])
        mlflow.log_metrics("avg_search_time_ms", metrics["avg_search_time_ms"])

        # Log parameters
        mlflow.log_params({
            "index_type": "FAISS",
            "model_name": MODEL_NAME,
            "search_k": 10
        })

        # Log model
        mlflow.pyfunc.log_model(
            artifact_path="rag_model",
            python_model=FaissRAG(),
            artifacts={
                "index": str(index_path),
                "meta": str(meta_path),
            },
            registered_model_name=MODEL_NAME,
        )

    # Promote to production alias
    promote_latest_to_prod_alias(model_name=MODEL_NAME, alias="prod")

if __name__ == "__main__":
    log_faiss_rag_model()