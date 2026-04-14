import json
from app.core.exceptions import InvalidModelOutputError

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