import os
import requests
import logging

from app.core.exceptions import (
    LLMServiceUnavailableError,
    InvalidLLMResponseError,
)

logger = logging.getLogger("incident-service")

LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL")


# Funcion cliente que se comunica con el microservicio del LLM
def analyze_text_with_llm(text: str, analysis_type: str):

    logger.info(f"Enviando solicitud al servicio LLM en {LLM_SERVICE_URL} para analizar el texto con el tipo de analisis: {analysis_type}")
    try:
        response = requests.post(
            f"{LLM_SERVICE_URL}/api/v1/analysis/text",
            json={
                "text": text,
                "analysis_type": analysis_type
            },
            timeout=120
        )
    except requests.exceptions.Timeout:
        raise LLMServiceUnavailableError("Tiempo de espera agotado para el servicio de LLM")
    except requests.exceptions.ConnectionError:
        raise LLMServiceUnavailableError("Error de conexion con el servicio de LLM")
    except requests.exceptions.RequestException:
        raise LLMServiceUnavailableError("Error de solicitud al servicio de LLM")

    if response.status_code >= 500:
        raise LLMServiceUnavailableError("Error de servidor en el servicio LLM")


    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise LLMServiceUnavailableError("El servicio LLM devolvio un error HTTP")


    try:
        logger.info(f"Respuesta recibida del servicio LLM para el analisis del texto, comprobando formato de la respuesta")
        data = response.json()
    except ValueError:
        logger.warning(f"Respuesta del servicio LLM no es un JSON valido")
        raise InvalidLLMResponseError("La respuesta del servicio LLM no es un JSON valido")

    if not isinstance(data, dict):
        logger.warning(f"Respuesta del servicio LLM no es un objeto JSON valido")
        raise InvalidLLMResponseError("La respuesta del servicio LLM no es un objeto valido")

    logger.info(f"Respuesta del servicio LLM recibida y validada correctamente")
    return data