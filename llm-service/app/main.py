from fastapi import FastAPI
from app.api.v1.routers.analysis_router import router as analysis_router
from app.core.config import LOAD_MODEL_ON_STARTUP
from app.core.model_loader import load_model, is_model_loaded

# Importancion de los tipos de errores (excepciones personalizadas)
from app.core.exceptions import (
    ModelNotLoadedError,
    ModelLoadError,
    PromptNotFoundError,
    ModelInferenceError,
    InvalidModelOutputError,
    PromptFormattingError,
)

# Importancion de los manejadores de errores propios (funciones)
from app.core.error_handlers import (
    model_not_loaded_handler,
    model_load_handler,
    prompt_not_found_handler,
    model_inference_handler,
    invalid_model_output_handler,
    prompt_formatting_handler,
    generic_exception_handler,
)

app = FastAPI()

# Registro de manejadores de errores personalizados
app.add_exception_handler(ModelNotLoadedError, model_not_loaded_handler)
app.add_exception_handler(ModelLoadError, model_load_handler)
app.add_exception_handler(PromptNotFoundError, prompt_not_found_handler)
app.add_exception_handler(ModelInferenceError, model_inference_handler)
app.add_exception_handler(InvalidModelOutputError, invalid_model_output_handler)
app.add_exception_handler(PromptFormattingError, prompt_formatting_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Evento al levantar el microservicio
@app.on_event("startup")
def on_startup():
    # Se realiza un tipo de carga u otra dependiendo del parametro
    if LOAD_MODEL_ON_STARTUP:
        load_model()

# Endpoint para comprobar el estado del microservicio y si el modelo esta cargado o no
@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": is_model_loaded()}

# Registro de routers de la API (endpoints)
app.include_router(analysis_router)
