import json
import re
import json_repair
from app.core.exceptions import InvalidModelOutputError, ModelInferenceError
from app.schemas.analysis_response import AnalysisResponse
import logging

logger = logging.getLogger(__name__)


def _find_json_in_markdown(text: str) -> str | None:
    # Intenta extraer contenido de bloques markdown ```json ... ```
    match = re.search(r"```json\s+(.*?)\s+```", text, re.DOTALL)
    return match.group(1).strip() if match else None

def _find_json_by_braces(text: str) -> str | None:
    # Busca el contenido entre la primera y ultima llave
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return None



# Comprueba si sera un JSON valido, si no lo es, lanza una excepcion
def extract_json(output_text: str) -> dict:
    logger.info("Iniciando la extraccion del JSON")

    # Intentamos obtener el texto generado en markdown y si no en llaves
    json_text = _find_json_in_markdown(output_text) or _find_json_by_braces(output_text)


    if not json_text:
        logger.error("El modelo no ha generado un JSON")
        raise InvalidModelOutputError("El modelo no ha devuelto un JSON")

    # Comprobamos si el texto extraido es un JSON valido
    try:
        logger.info("Devolviendo el JSON extraido")
        # Con JSON repair nos aseguramos de que problemas posibles en el JSON, como comillas dobles/simples, comas extra, etc
        return json_repair.loads(json_text) 
    except json.JSONDecodeError as exc:
        logger.error("El modelo no ha devuelto un JSON valido")
        raise InvalidModelOutputError("El JSON devuelto por el modelo no es valido") from exc
    


def parse_and_validate_response(outputs, inputs, tokenizer) -> AnalysisResponse:
    logger.info("Obteniendo la salida del modelo")
    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    # Proceso inverso, pasamos de token a texto legible
    try:
        logger.info("Decodificando la salida del modelo a texto legible")
        output_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
    except Exception as exc:
        logger.error("Error al pasar de token a texto legible")
        raise ModelInferenceError("Error al decodificar la salida del modelo") from exc

    logger.info("Extrayendo el JSON de la respuesta del modelo")
    parsed = extract_json(output_text)

    try:
        logger.info("Devolviendo la respuesta del modelo")
        return AnalysisResponse(**parsed) 
    except Exception as exc:
        logger.error("Error al devolver al respuesta del modelo, faltan campos o hay tipos incorrectos")
        raise InvalidModelOutputError(f"La salida del modelo no es valida: {str(exc)}")