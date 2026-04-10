from fastapi import FastAPI
from app.api.v1.routers.analysis_router import router as analysis_router
from app.core.config import LOAD_MODEL_ON_STARTUP
from app.core.model_loader import load_model, is_model_loaded

app = FastAPI()

@app.on_event("startup")
def on_startup():
    if LOAD_MODEL_ON_STARTUP:
        print("Cargando modelo...")
        load_model()
        print("Modelo cargado")

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": is_model_loaded()}

app.include_router(analysis_router)