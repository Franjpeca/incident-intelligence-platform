from app.core.config import DO_SAMPLE, MAX_NEW_TOKENS, TEMPERATURE, TOP_P
from app.core.model_loader import get_model
from app.core.output_parser import parse_and_validate_response
from app.core.prompt_manager import get_input_text
from app.schemas.analysis_response import AnalysisResponse

from app.core.exceptions import ModelInferenceError

import logging

logger = logging.getLogger(__name__)


# Funcion privada auxiliar para tokenizar la entrada
def _tokenize_input(input_text: str, tokenizer, device) -> dict:
    try:
        logger.info("Tokenizando el input del modelo")
        return tokenizer(input_text, return_tensors="pt").to(device)
    except Exception as exc:
        logger.error(f"Error en fase de tokenizacion: {exc}")
        raise ModelInferenceError("Error al preparar los tensores para el modelo") from exc


# Funcion privada auxiliar que realiza la llamada al modelo
def _generate_response(model, inputs) -> list:

    try:
        logger.info("Iniciando inferencia en el modelo")
        # Llamada al modelo 
        return model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=DO_SAMPLE
        )
    except Exception as exc:
        logger.error(f"Error en la generacion del modelo: {exc}")
        raise ModelInferenceError("Error durante la inferencia del modelo") from exc


# Funcion principal que trata y analiza un texto usando un LLM
def analyze_text(text: str, analysis_type: str = None) -> AnalysisResponse:
    logger.info("Iniciando analisis de texto usando LLM")

    tokenizer, model, lock = get_model()

    input_text = get_input_text(tokenizer, analysis_type, text)

    inputs = _tokenize_input(input_text, tokenizer, model.device)

    with lock:
        logger.info("Entrando al lock de inferencia. Iniciando uso del modelo...")
        outputs = _generate_response(model, inputs)

    # La respuesta viene mezclada con la entrada, por lo que hay que separar la parte de la respuesta que nos interesa
    return parse_and_validate_response(outputs, inputs, tokenizer)