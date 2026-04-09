from fastapi import FastAPI
from app.api.v1.routers.analysis_router import router as analysis_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(analysis_router)