import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
MODEL_PATH  = os.getenv("MODEL_PATH", "artifacts/model.joblib")
MODEL_METADATA_PATH = os.getenv("MODEL_METADATA_PATH","artifacts/model_metadata.json")