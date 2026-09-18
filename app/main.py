from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.config import MODEL_PATH, MODEL_METADATA_PATH
from app.ml import ModelWrapper
from app.database import Base, engine
import app.models
from app.routes import router

@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    app.state.model=ModelWrapper(MODEL_PATH, MODEL_METADATA_PATH)
    yield


app= FastAPI(title="Loss Predictor", version="0.1.0", lifespan=lifespan)
app.include_router(router)