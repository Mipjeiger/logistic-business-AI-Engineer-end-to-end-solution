import mlflow
import mlflow.pyfunc
from ultralytics import YOLO
import pickle
import logging
from pathlib import Path

# ====================================================
# Setup logging
# ====================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====================================================
# MLflow PyFunc Model Wrapper
# =====================================================
class YOLOv8ModelWrapper(mlflow.pyfunc.PythonModel):
    """
    Multi-task YOLOv8 model:
    - Container detection
    - Damage detection
    """

    def load_context(self, context):
        """
        Load YOLOv8 models from MLflow artifacts.
        """
        logger.info("Loading YOLOv8 models from artifacts...")

        self.detector = YOLO(context.artifacts["detection_model"])
        self.damage = YOLO(context.artifacts["damage_model"])

        with open(context.artifacts["class_mapping"], "rb") as f:
            self.class_mapping  = pickle.load(f)

        logger.info("YOLOV8 models loaded successfully.")

    def predict(self, context, model_input):
        """
        model_input:
            - image path (str / Path)
            - numpy array

        return:
            dict with detection & damage results
        """
        logger.info("Running YOLOV8 inference...")

        detection_results = self.detector(
            source=model_input,
            conf=0.10,
            verbose=False
        )

        damage_results = self.damage(
            source=model_input,
            conf=0.10,
            verbose=False
        )

        return {
            "container_detections": detection_results,
            "damage_detections": damage_results,
            "class_mapping": self.class_mapping
        }
    
# =====================================================
# Artifact path resolution (LOGGING ONLY)
# =====================================================
def resolve_artifact_paths():
    """
    Resolve and log artifact paths for YOLOv8 models.
    """
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parents[2]

    detection_path = (
        project_root /
        "notebooks" /
        "datasets_container" /
        "models" /
        "container_yolov8.pt"
    )

    damage_path = (
        project_root /
        "notebooks" /
        "yolov8_damage_models" /
        "yolov8_container_damage.pt"
    )
    logger.info(f"Detection model path: {detection_path}")
    logger.info(f"Damage model path: {damage_path}")

    return detection_path, damage_path

# =====================================================
# MLflow logging entrypoint
# =====================================================
def log_model_to_mlflow():
    """
    Log the YOLOv8 multi-task model to MLflow."""
    detection_path, damage_path = resolve_artifact_paths()

    with mlflow.start_run():
        mlflow.pyfunc.log_model(
            artifact_path="YOLOv8_model",
            python_model=YOLOv8ModelWrapper(),
            artifacts={
                "detection_model": str(detection_path),
                "damage_model": str(damage_path),
            },
            register_model_name="container_yolov8_multi_task_model"
        )

        logger.info("YOLOv8 multi-task model logged to MLflow successfully.")