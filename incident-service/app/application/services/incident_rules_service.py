import logging

from app.schemas.incident_rules_result import IncidentRulesResult
# Funciones con logica de negocio para detectar las palabras clave
from app.domain.rules.incident_rules import contains_critical_terms, contains_technical_terms

logger = logging.getLogger("incident-service")

# Funcion que analiza el texto de una incidencia mediante reglas clasicas
def analyze_text_with_rules(title: str, description: str) -> IncidentRulesResult:
    # Tratamiento del texto para poder encontrar bien las palabras clave
    logger.info(f"Inicio del analisis de la incidencia: {title}")
    text = f"{title} {description}".lower()

    # Caso donde no encontramos las palabras clave pero si encontramos palabras tecnicas
    # Aqui tenemos incidencias complejas, por lo que mejor un analisis completo
    if contains_critical_terms(text):
        logger.info(f"Generando analisis de la incidencia usando unicamente reglas: {title}")
        return IncidentRulesResult(
            use_llm=False,
            summary="Incidencia critica detectada automaticamente",
            category="system",
            priority="high",
            confidence=95
        )

    # Caso donde encontramos palabras clave criticas, no se llama al modelo
    if contains_technical_terms(text):
        logger.info(f"Generando analisis de la incidencia usando reglas y LLM con analisis completo")
        return IncidentRulesResult(
            use_llm=True,
            analysis_type="full_analysis",
            priority="medium",
            confidence=60
        )

    # Caso donde no encontramos nada de lo anterior, ni critico ni tecnico
    # Por lo que se hace un analisis basico y no tan detallado, para ahorrar recursos
    logger.info(f"Generando analisis de la incidencia usando reglas y LLM con analisis basico")
    return IncidentRulesResult(
        use_llm=True,
        analysis_type="basic_analysis",
        priority="medium",
        confidence=50
    )