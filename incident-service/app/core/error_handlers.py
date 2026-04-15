from fastapi import Request
from fastapi.responses import JSONResponse
# Tipos de errores registrados
from app.core.exceptions import (
    IncidentNotFoundError,
    AnalysisNotFoundError,
    LLMServiceUnavailableError,
    InvalidLLMResponseError,
    DatabaseOperationError,
    FieldError,
)

## -- Errores 4XX (cliente) --

# Incidencia no encontrada
def incident_not_found_handler(request: Request, exc: IncidentNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )

# Analisis no encontrado
def analysis_not_found_handler(request: Request, exc: AnalysisNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )

async def field_error_handler(request: Request, exc: FieldError):
    return JSONResponse(
        status_code=400, # Bad Request porque el error es de los datos enviados
        content={
            "error": "campos_invalidos",
            "message": exc.message
        }
    )

## -- Errores 5XX (servidor) --

# Fallo al conectar con el servicio de LLM
def llm_service_unavailable_handler(request: Request, exc: LLMServiceUnavailableError):
    return JSONResponse(
        status_code=503,
        content={"detail": exc.message}
    )

# Respuesta del LLM incorrecta
def invalid_llm_response_handler(request: Request, exc: InvalidLLMResponseError):
    return JSONResponse(
        status_code=502,
        content={"detail": exc.message}
    )

# Fallo en la base de datos
def database_operation_handler(request: Request, exc: DatabaseOperationError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message}
    )


# -- Manejador generico de error --
# Captura algun otro error posible para no dejar al cliente sin respuesta o con un error no manejado
def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )