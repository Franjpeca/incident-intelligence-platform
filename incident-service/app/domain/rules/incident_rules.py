import re
import json
from pathlib import Path

KEYWORDS_PATH = Path(__file__).parent / "keywords.json"

# Carga de las keywords usando fichero
def _load_keywords():
    try:
        with open(KEYWORDS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"critical": [], "technical": []}


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

def contains_critical_terms(text: str) -> bool:
    if not KEYWORDS.get("critical"): return False
    return bool(CRITICAL_PATTERN.search(text))

def contains_technical_terms(text: str) -> bool:
    if not KEYWORDS.get("technical"): return False
    return bool(TECHNICAL_PATTERN.search(text))