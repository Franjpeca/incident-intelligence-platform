from fastapi import FastAPI
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.infrastructure.db.models.incident_model import Incident
from app.api.v1.routers.incident_router import router as incident_router

app = FastAPI()

# Ejecucion al iniciar el microservicio
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Endopint para probar que el microservicio esta activo
@app.get("/health")
def health():
    return {"status": "ok"}

# Permite incluir el router de incidencias y con ello sus endpoints
app.include_router(incident_router)