import json
from app.core.exceptions import InvalidModelOutputError, ModelInferenceError
from app.schemas.analysis_response import AnalysisResponse
import logging

logger = logging.getLogger(__name__)

# Slicer que extrae el texto del JSON
# Comprueba si sera un JSON valido, si no lo es, lanza una excepcion
# La idea es encontrar que esta entre corchetes y luego parsearlo a un diccionario para asegurar la forma de la salida
def extract_json(output_text: str) -> dict:
    logging.info("Iniciando la extracion del JSON")
    start = output_text.find("{")
    end = output_text.rfind("}")

    # Aqui se comprueba que el modelo es un JSON
    if start == -1 or end == -1 or end <= start:
        logging.error("El modelo no ha generado un JSON")
        raise InvalidModelOutputError("El modleo no ha devuelto un JSON")

    json_text = output_text[start:end + 1]

    # Aqui comprobamos que el texto extraido es un JSON valido, si no lo es, lanzamos una excepcion 
    # Pasamos de json a un objeto python, si da error es porque el texto no es un JSON
    try:
        logging.info("Devolviendo el JSON extraido")
        return json.loads(json_text) 
    except json.JSONDecodeError as exc:
        logging.error("El modelo no ha devuelto un JSON valido")
        raise InvalidModelOutputError("El JSON devuelto por el modelo no es valido") from exc
    


def parse_and_validate_response(outputs, inputs, tokenizer) -> AnalysisResponse:
    logging.info("Obteniendo la salida del modelo")
    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    # Proceso inverso, pasamos de token a texto legible
    try:
        logging.info("Decodificando la salida del modelo a texto legible")
        output_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
    except Exception as exc:
        logging.error("Error el pasar de token a texto legible")
        raise ModelInferenceError("Error al decodificar la salida del modelo") from exc
    # Extraemos el JSON de la respuesta del modelo y lo parseamos a un diccionario
    logging.info("Extrayendo el JSON de la respuesta del modelo")
    parsed = extract_json(output_text)
    # Intentamos crear el objeto AnalysisResponse directamente
    # Pydantic se encargara de comprobar si faltan campos o si los tipos estan mal.
    # Esto permite que sea escalable, sin tener que especificar en esta parte del codigo campos fijos
    try:
        logging.info("Devolviendo la respuesta del modelo")
        return AnalysisResponse(**parsed) 
    except Exception as exc:
        logging.error("Error al devolver al respuesta del modelo, faltan campos o hay tipos incorrectos")
        raise InvalidModelOutputError(f"La salida del modelo no es valida: {str(exc)}")