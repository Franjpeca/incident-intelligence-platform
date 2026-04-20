import re
import json
from pathlib import Path

# Al ser logica de dominio, lo lo indicamos el env, no es relacionado con la propia ejecucion
KEYWORDS_PATH = Path(__file__).parent / "keywords.json"

# Intenamos leer el fichero JSON, con control en caso de que haya fallo
def _load_keywords():
    try:
        with open(KEYWORDS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"critical": [], "technical": []}

# Dejamos cargadas las palabras
KEYWORDS = _load_keywords()

# Patrones de busqueda, para que el caso en el que aumente de tamaño se maneje mejor
# Basicamente es una expresion regular, ya que puede haber falsos positivos 
# con palabras como "down" y "countdown" entre otros
# Es por robustez en las reglas
CRITICAL_PATTERN = re.compile(
    rf"\b({'|'.join(re.escape(w) for w in KEYWORDS.get('critical', []))})\b", 
    re.IGNORECASE
)

TECHNICAL_PATTERN = re.compile(
    rf"\b({'|'.join(re.escape(w) for w in KEYWORDS.get('technical', []))})\b", 
    re.IGNORECASE
)

# Funciones que detectan palabras
# Es logica de negocio, por lo que se indican en esta capa de dominio, y no en la de infraestructura o aplicacion
def contains_critical_terms(text: str) -> bool:
    if not KEYWORDS.get("critical"): return False
    return bool(CRITICAL_PATTERN.search(text))

def contains_technical_terms(text: str) -> bool:
    if not KEYWORDS.get("technical"): return False
    return bool(TECHNICAL_PATTERN.search(text))