import os
import requests
import logging

from app.core.exceptions import (
    LLMServiceUnavailableError,
    InvalidLLMResponseError,
)

logger = logging.getLogger("incident-service")

LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL")

# Funcion que se comunica con el microservicio del LLM
# Se encuentra en la capa de infraestructura ya que no es parte de la propia API
# Es un cliente que se comunica con otro servicio externo
def analyze_text_with_llm(text: str, analysis_type: str):
    # Realizamos la solicitud al servicio de LLM usando la libreria requests
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
    except requests.exceptions.Timeout: # Comprobamos errores posibles que hayan sucedido
        raise LLMServiceUnavailableError("Tiempo de espera agotado para el servicio de LLM")
    except requests.exceptions.ConnectionError:
        raise LLMServiceUnavailableError("Error de conexion con el servicio de LLM")
    except requests.exceptions.RequestException:
        raise LLMServiceUnavailableError("Error de solicitud al servicio de LLM")

    # Comprobamos si el error devuelto es 500, es decir, un error de lservidor
    if response.status_code >= 500:
        raise LLMServiceUnavailableError("Error de servidor en el servicio LLM")

    # Buscamos con raise_for_status comprobar si ha devuelto algun codigo de error HTTP 4XX o 5XX
    # Es para controlar otros posibles errores de forma generica
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise LLMServiceUnavailableError("El servicio LLM devolvio un error HTTP")

    # Ahora comprobamos que los datos que nos ha devuelto el LLM es un JSON y con formato correcto
    try:
        logger.info(f"Respuesta recibida del servicio LLM para el analisis del texto, comprobando formato de la respuesta")
        data = response.json()
    except ValueError:
        logger.warning(f"Respuesta del servicio LLM no es un JSON valido")
        raise InvalidLLMResponseError("La respuesta del servicio LLM no es un JSON valido")

    if not isinstance(data, dict):
        logger.warning(f"Respuesta del servicio LLM no es un objeto JSON valido")
        raise InvalidLLMResponseError("La respuesta del servicio LLM no es un objeto valido")

    # Si no sucede ninguno de los errores anteriores, devolvemos la respuesta dada por el LLM
    logger.info(f"Respuesta del servicio LLM recibida y validada correctamente")
    return data