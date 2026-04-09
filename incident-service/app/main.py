from fastapi import FastAPI
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine

# Permite importar el modelo para las tablas
from app.infrastructure.db.models.incident_model import Incident

app = FastAPI()

# Ejecucion al iniciar el microservicio
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}