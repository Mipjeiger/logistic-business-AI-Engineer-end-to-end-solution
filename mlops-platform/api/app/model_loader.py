import mlflow

mlflow.set_tracking_uri("http://localhost:5015")

# Create function to load the model
def load_model(model_name: str):
    return mlflow.pyfunc.load_model(
        f"models:/{model_name}/Production"
    )