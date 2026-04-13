from app.schemas.incident_rules_result import IncidentRulesResult
# Funciones con logica de negocio para detectar las palabras clave
from app.domain.rules.incident_rules import contains_critical_terms, contains_technical_terms

# Funcion que analiza el texto de una incidencia mediante reglas clasicas
def analyze_text_with_rules(title: str, description: str) -> IncidentRulesResult:
    # Tratamiento del texto para poder encontrarb ien las palabras clave
    text = f"{title} {description}".lower()

    # Caso donde no encontramos las palabras clave pero si encontramos palabras tecnias
    # Aqui tenemos incidencias complejas, por lo que mejor un analisis completo
    if contains_critical_terms(text):
        return IncidentRulesResult(
            use_llm=False,
            summary="Incidencia critica detectada automaticamente",
            category="system",
            priority="high",
            confidence=95
        )

    # Caso donde encontramos palabras clave criticas, no se llama al modelo
    if contains_technical_terms(text):
        return IncidentRulesResult(
            use_llm=True,
            analysis_type="full_analysis",
            priority="medium",
            confidence=60
        )

    # Caso donde no encontramos nada de lo anterior, ni critico ni tecnico
    # Por lo que se hace un analisis basico y no tan detallado, para ahorrar recursos
    return IncidentRulesResult(
        use_llm=True,
        analysis_type="basic_analysis",
        priority="medium",
        confidence=50
    )