# Librerias de carga del modelo y tokenizer de Hugging Face
from transformers import AutoModelForCausalLM, AutoTokenizer
# Nombre del modelo a cargar
from app.core.config import MODEL_ID

from app.core.exceptions import ModelLoadError

import logging
import threading

logger = logging.getLogger(__name__)


_tokenizer = None
_model = None
# Lock global para evitar problemas de condiciones de carrera
_inference_lock = threading.Lock()

# Funcion para obtener el modelo, lo carga si no esta ya cargado
def get_model():

    logger.info("Comenzando la carga del modelo")
    global _tokenizer, _model, _inference_lock

    try:
        if _tokenizer is None:
            logger.info("Tokenizer no cargado, cargandolo")
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

        if _model is None:
            logger.info("Modelo no cargado, cargandolo")
            _model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID,
                device_map="auto",  # Indicamos que se cargue en GPU, si no se puede, se cargara en CPU
                torch_dtype="auto", # Ajusta automaticamente a float16 si hay GPU, mas eficiente
                low_cpu_mem_usage=True  # Mejora la carga del modelo
            )

    except Exception:
        logger.error("Error al cargar el modelo")
        raise ModelLoadError("Error al cargar el modelo")

    logger.info("Modelo y tokenizer cargados con exito")
    return _tokenizer, _model, _inference_lock


# Funcion para verificar si el modelo y tokenizer estan cargados
def is_model_loaded():
    return _tokenizer is not None and _model is not None