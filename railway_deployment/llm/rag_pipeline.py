import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, "..", "..", ".env")
load_dotenv(env_path)

# HuggingFace key environment variable
HF_TOKEN = os.getenv("HUGGING_API_KEY")
API_URL = (
    "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
)
headers = {"Authorization": f"Bearer {HF_TOKEN}"}


# Create a function to query the LLM RAG pipeline
def query_llm(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
