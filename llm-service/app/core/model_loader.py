# Importamos las librerias necesarias para cargar el modelo y tokenizer de Hugging Face
from transformers import AutoModelForCausalLM, AutoTokenizer
 # Nombre del modelo a cargar
from app.core.config import MODEL_ID
# Import de la excepcion propia de error al cargar el modelo
from app.core.exceptions import ModelLoadError

import logging
import threading

logger = logging.getLogger(__name__)

# Variables que almacenaran el modelo y tokenizer cargados
# Se busca evitar cargarlo cada vez que se haga una peticion
_tokenizer = None
_model = None
# Para evitar problemas de rendimiento al acceder al modelo
# Se indica fuera para evitar problemas de condiciones de carrera
_inference_lock = threading.Lock()

# Funcion para obtener el modelo, lo carga si no esta ya cargado
def get_model():
    # Tomamos las variables gloables, y si no esta cargado el modelo y tokenizer, los cargamos
    logging.info("Comenzando la carga del modelo")
    global _tokenizer, _model, _inference_lock

    # Probamos a realizar la carga de las dos variables
    try:
        if _tokenizer is None:
            logging.info("Tokenizer no cargado, cargandolo")
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

        if _model is None:
            logging.info("Modelo no cargado, cargandolo")
            _model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID,
                device_map="auto",  # Indicamos que se cargue en GPU, si no se puede, se cargara en CPU
                torch_dtype="auto",# Ajusta automaticamente a float16 si hay GPU, mas eficiente
                low_cpu_mem_usage=True # Mejora la carga del modelo
            )
    # Si no funciona, entonces lanzamos error de carga del modelo
    except Exception:
        logging.error("Error al cargar el modelo")
        raise ModelLoadError("Error al cargar el modelo")

    logging.info("Modelo y tokenizer cargados con exito")
    return _tokenizer, _model, _inference_lock



def is_model_loaded(): # Funcion para verificar si el modelo y tokenizer estan cargados, para el health check
    return _tokenizer is not None and _model is not None