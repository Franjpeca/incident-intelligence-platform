from app.core.config import DO_SAMPLE, MAX_NEW_TOKENS, TEMPERATURE, TOP_P
from app.core.model_loader import get_model
from app.core.output_parser import parse_and_validate_response
from app.core.prompt_manager import get_input_text
from app.schemas.analysis_response import AnalysisResponse
# Importaciones de excepciones propias
from app.core.exceptions import ModelInferenceError

import threading

import logging

logger = logging.getLogger(__name__)


# Funcion "privada" auxiliar, incorpora el control de errores para dejar limpia la funcion que la llama
def _tokenize_input(input_text: str, tokenizer, device) -> dict:
    try:
        logging.info("Tokenizando el input del modelo")
        return tokenizer(input_text, return_tensors="pt").to(device)
    except Exception as exc:
        logging.error(f"Error en fase de tokenización: {exc}")
        raise ModelInferenceError("Error al preparar los tensores para el modelo") from exc


# Funcion "privada" auxiliar para dejar mas limpio el servicio
# Realiza la llamada al modelo
def _generate_response(model, inputs) -> list:

    try:
        logging.info("Iniciando inferencia en el modelo")
        # Aqui se introducen al modelo la entrada que ya ha sido cargada y se pide generar una respuesta
        # Se le indican parametros del mismo, como la temperatura
        return model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=DO_SAMPLE
        )
    except Exception as exc:
        logging.error(f"Error en la generación del modelo: {exc}")
        raise ModelInferenceError("Error durante la inferencia del modelo") from exc


# Funcion principal del servicios de analisis
# Recibe el texto del cliente a analizar
# Devuelve un objeto con el resumen, categoria, prioridad y confianza
def analyze_text(text: str, analysis_type: str = None) -> AnalysisResponse:
    logging.info("Iniciando analisis de texto usando LLM")
    # Cargamos el modelo y el tokenizer
    # El modelo se carga una sola vez y se reutiliza en cada llamada a la funcion
    tokenizer, model, lock = get_model()

    input_text = get_input_text(tokenizer, analysis_type, text)
    # Transformamos este texto a tokens que entendera el modelo y los movemos a memoria
    # Es cargar la entrada
    inputs = _tokenize_input(input_text, tokenizer, model.device)
    # Generamos la respuesta del modelo
    with lock:
        logging.info("Entrando al lock de inferencia. Iniciando uso del modelo...")
        outputs = _generate_response(model, inputs)

    # La respuesta viene mezclada con la entrada, por lo que hay que separar la parte de la respuesta que nos interesa
    return parse_and_validate_response(outputs, inputs, tokenizer)