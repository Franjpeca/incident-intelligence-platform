CRITICAL_KEYWORDS = {
    "caido", "caída", "produccion", "produccion",
    "urgente", "critico", "crítico", "no responde", "down"
}

TECHNICAL_KEYWORDS = {
    "error", "exception", "timeout", "fail", 
    "stacktrace", "log", "nullpointer"
}

# Funciones que detectan palabras
# Es logica de negocio, por lo que se indican en esta capa de dominio, y no en la de infraestructura o aplicacion
def contains_critical_terms(text: str) -> bool:
    normalized_text = text.lower()
    return any(word in normalized_text for word in CRITICAL_KEYWORDS)

def contains_technical_terms(text: str) -> bool:
    normalized_text = text.lower()
    return any(word in normalized_text for word in TECHNICAL_KEYWORDS)