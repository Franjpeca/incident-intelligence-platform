import json

# Slicer que extrae el texto del JSON
# Comprueba si sera un JSON valido, si no lo es, lanza una excepcion
# La idea es encontrar que esta entre corchetes y luego parsearlo a un diccionario para asegurar la forma de la salida
def extract_json(output_text: str) -> dict:
    start = output_text.find("{")
    end = output_text.rfind("}")

    # Aqui se comprueba que el modelo es un JSON a traves de 
    if start == -1 or end == -1 or end <= start:
        raise ValueError("El modelo no ha devuelto un JSON")

    json_text = output_text[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError("El JSON devuelto por el modelo no es valido") from exc