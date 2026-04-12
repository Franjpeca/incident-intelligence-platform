from fastapi import Request
from fastapi.responses import JSONResponse

# Importancion de los tipos de errores (excepciones) personalizadass
from app.core.exceptions import (
    ModelNotLoadedError,
    ModelLoadError,
    PromptNotFoundError,
    ModelInferenceError,
    InvalidModelOutputError,
    PromptFormattingError,
)

# -- Errores 5XX --
# Modelo no cargado
def model_not_loaded_handler(request: Request, exc: ModelNotLoadedError):
    return JSONResponse(
        status_code=503,
        content={"detail": exc.message}
    )

# Error al cargar el modelo
def model_load_handler(request: Request, exc: ModelLoadError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message}
    )

# Prompt no encontrado
def prompt_not_found_handler(request: Request, exc: PromptNotFoundError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message}
    )

# Error durante la inferencia del modelo (uso del modelo)
def model_inference_handler(request: Request, exc: ModelInferenceError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message}
    )

# Salida del modelo invalida o inesperada
def invalid_model_output_handler(request: Request, exc: InvalidModelOutputError):
    return JSONResponse(
        status_code=502,
        content={"detail": exc.message}
    )

# Error al formatear el prompt o respuesta
def prompt_formatting_handler(request: Request, exc: PromptFormattingError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message}
    )

# -- Manejador generico de error --
# Captura cualquier error no manejado concretamente y devuelve un error 500 generico
def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )