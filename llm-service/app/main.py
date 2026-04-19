from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from app.api.v1.routers.analysis_router import router as analysis_router
from app.core.config import LOAD_MODEL_ON_STARTUP
from app.core.model_loader import get_model, is_model_loaded

from fastapi.middleware.cors import CORSMiddleware

import logging
from app.core.logging_config import setup_logging

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

setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando microservicio LLM...")
    # En base a una variable configurable, se establece cuando cargar el modelo
    if LOAD_MODEL_ON_STARTUP:
        logger.info("Se procede a realizar la carga del modelo ...")
        get_model()
        if is_model_loaded():
            logger.info("Modelo cargado correctamente en memoria")
        else:
            logger.error("El modelo no se pudo cargar")
            
    yield
    logger.info("Apagando microservicio LLM...")

app = FastAPI(
    title="LLM Service",
    lifespan=lifespan
)

# Permitimos conexiones, en este caso, desde nuestra web
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de manejadores de errores personalizados
app.add_exception_handler(ModelNotLoadedError, model_not_loaded_handler)
app.add_exception_handler(ModelLoadError, model_load_handler)
app.add_exception_handler(PromptNotFoundError, prompt_not_found_handler)
app.add_exception_handler(ModelInferenceError, model_inference_handler)
app.add_exception_handler(InvalidModelOutputError, invalid_model_output_handler)
app.add_exception_handler(PromptFormattingError, prompt_formatting_handler)
app.add_exception_handler(Exception, generic_exception_handler)



# Endpoint para comprobar el estado del microservicio y si el modelo esta cargado o no
@app.get("/health")
def health():
    if is_model_loaded():
        return {"status": "ok", "model_loaded": True}

    raise HTTPException(status_code=503, detail="Model not loaded yet")

# Registro de routers de la API (endpoints)
app.include_router(analysis_router)
