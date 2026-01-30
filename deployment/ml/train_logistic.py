import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

# Get base_dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data from CSV file
dataset = os.path.join(BASE_DIR, "..", "data", "logistic_data_cleaned.csv")

# Load dataset
try:
    df = pd.read_csv(dataset)
    print(df.head())
    print("Dataset loaded successfully.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

# Split dataset into features and target
X = df.drop("is_high_risk", axis=1)
y = df["is_high_risk"]

# Define model
model = LogisticRegression(
    max_iter=3500,
    random_state=42,
    solver="saga",
    verbose=1,
    n_jobs=-1,
    penalty="elasticnet",
    l1_ratio=0.5,
)
model.fit(X, y)

# Save model using joblib
joblib.dump(model, os.path.join(BASE_DIR, "..", "models", "logistic_model.pkl"))
print("Model trained and saved successfully.")
