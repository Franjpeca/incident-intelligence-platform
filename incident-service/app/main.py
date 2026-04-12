from fastapi import FastAPI
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.infrastructure.db.models.incident_model import Incident
from app.api.v1.routers.incident_router import router as incident_router

from app.core.exceptions import (
    IncidentNotFoundError,
    AnalysisNotFoundError,
    LLMServiceUnavailableError,
    InvalidLLMResponseError,
    DatabaseOperationError,
)

from app.core.error_handlers import (
    incident_not_found_handler,
    analysis_not_found_handler,
    llm_service_unavailable_handler,
    invalid_llm_response_handler,
    database_operation_handler,
    generic_exception_handler,
)

app = FastAPI()

# Registro de los manejadores de errores propios
# Se registra el tipo de error y el manejador (funcion) que se encarga de procesar ese error
app.add_exception_handler(IncidentNotFoundError, incident_not_found_handler)
app.add_exception_handler(AnalysisNotFoundError, analysis_not_found_handler)
app.add_exception_handler(LLMServiceUnavailableError, llm_service_unavailable_handler)
app.add_exception_handler(InvalidLLMResponseError, invalid_llm_response_handler)
app.add_exception_handler(DatabaseOperationError, database_operation_handler)
app.add_exception_handler(Exception, generic_exception_handler)

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

