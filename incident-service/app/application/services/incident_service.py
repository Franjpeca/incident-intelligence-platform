import logging
# Para incluir lo que retornan las funciones
# Mejora la legibilidad y autocompletado en ciertos IDE
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from app.infrastructure.db.models.incident_model import Incident
from app.schemas.incident_request import IncidentCreateRequest
from app.schemas.incident_update_request import IncidentUpdateRequest
from app.schemas.analysis_result import AnalysisResult
from app.domain.enums.incident_status import IncidentStatus
from app.infrastructure.clients.llm_service_client import analyze_text_with_llm
from app.application.services.incident_rules_service import analyze_text_with_rules
from app.infrastructure.db.repositories import incident_repositories as db_operations

from app.core.exceptions import (
    IncidentNotFoundError,
    InvalidLLMResponseError,
    AnalysisNotFoundError,
    FieldError,
    LLMServiceUnavailableError,
    BusinessRuleError,
)

logger = logging.getLogger("incident-service")


# Funcion que crea un registro de la tabla y lo introduce en la bd
def create_incident(data: IncidentCreateRequest, db: Session) -> Incident:
    # Bloque try para poder manejar cualquier error al acceder a la bd o al crear el objeto
    logger.info(f"Creando incidencia: '{data.title}'")

    incident = Incident(
        title=data.title,
        description=data.description
    )

    saved_incident = db_operations.save(db, incident)

    logger.info(f"Incidencia: '{data.title}' creada exitosamente con ID: {saved_incident.id}")
    return saved_incident


# Obtiene todos los registros de la tabla de la bd
def get_incidents(db: Session) -> List[Incident]:
    # Para no mostrar toda la base de datos, ya que puede generar problemas de memoria, mostramos los ultimos 100
    # Se podria aplicar paginacion y scroll infinito en el front si se desea de ver todo, pero para el proposito de
    # este proyecto poner un limite es suficiente. Lo importante es controlar que a futuro no colapse el servidor
    MAX_SAFETY_LIMIT = 100 
    logger.info(f"Obteniendo las últimas {MAX_SAFETY_LIMIT} incidencias")
    
    return db_operations.list_incidents(db, limit=MAX_SAFETY_LIMIT)


# Obtiene un registro de la tabla usando su id
def get_incident_by_id(incident_id: int, db: Session) -> Incident:
    logger.info(f"Buscando incidencia con ID: {incident_id}")
    
    incident = db_operations.get_by_id(db, incident_id)

    # Aqui no hacemos try porque puede devolver un valor vacio, no un fallo como tal
    if incident is None:
        # WARNING porque aunque no sea un error del programa, es una busqueda fallida
        logger.warning(f"Incidencia no encontrada: ID {incident_id}")

        raise IncidentNotFoundError("Incidencia no encontrada")

    return incident


# Actualiza el estado de una incidencia
def update_incident_status(incident_id: int, status: IncidentStatus, db: Session) -> Incident:
    logger.info(f"Actualizando estado de la incidencia con ID: {incident_id}")
    
    # Consulta la BD y busca la incidencia
    # Devuelve None si no la encuentra (lanza error si no la encuentra)
    incident = get_incident_by_id(incident_id, db)

    # Si la encuentra, actualiza el estado
    # Hasta aqui similar a al funcion anterior
    incident.status = status.value
    
    # Aqui si hacemos un try porque es acceso a la bd y modificacion
    saved_incident = db_operations.save(db, incident)
    
    logger.info(f"Estado de la incidencia con ID: {incident_id} actualizado")
    return saved_incident


# Eliminar una incidencia dada su id
def delete_incident(incident_id: int, db: Session) -> bool:
    logger.info(f"Eliminando incidencia con ID: {incident_id}")
    # Similar a la funcion anterior

    # Consultamos y vemos si existe
    incident = get_incident_by_id(incident_id, db)

    # Consultamos la regla de negocio sobre si se puede borrar
    # Nota: Se lanzan aqui errores porque indicarlo en la regla no es correcto, no es su responsabilidad
    # y llevarse esto a una clase seria redundante
    if not incident.can_be_deleted():
        logger.warning("Intento de borrado no permitido para incidencia id=%s", incident_id)
        raise BusinessRuleError(
            f"No se puede eliminar la incidencia {incident_id} porque su estado es {incident.status}. "
            "Solo se permite el borrado en estado CLOSED."
        )

    # Si la encuentra, la eliminamos
    result = db_operations.delete(db, incident)
    
    logger.info(f"Incidencia eliminada con ID: {incident_id}")
    return result


# Actualiza por completo una incidencia segun el id
def update_incident(incident_id: int, data: IncidentUpdateRequest, db: Session) -> Incident:
    logger.info(f"Actualizando incidencia con ID: {incident_id}")
    # Similar a las funciones anteriores
    incident = get_incident_by_id(incident_id, db)

    # La diferencia es que aqui asignamos valores antes de hacer el commit en la bd
    if data.title is None and data.description is None and data.status is None:
        logger.error(f"No se recibieron campos para actualizar en la incidencia: {incident_id}")
        raise FieldError("Debes enviar al menos un campo para actualizar")

    if data.title is not None:
        incident.title = data.title
    if data.description is not None:
        incident.description = data.description
    if data.status is not None:
        incident.status = data.status.value

    saved_incident = db_operations.save(db, incident)
    
    logger.info(f"Incidencia actualizada con ID: {incident_id}")
    return saved_incident



# Getter del analisis de una incidencia usando el id
def get_incident_analysis(incident_id: int, db: Session) -> Dict[str, Any]:
    logger.info(f"Obteniendo analisis de la incidencia con ID: {incident_id}")
    
    # Comprobamos si la incidencia existe, si no, error
    incident = get_incident_by_id(incident_id, db)
    
    if incident.analysis_summary is None:
        logger.info(f"Analisis no encontrado para la incidencia: {incident_id}")
        raise AnalysisNotFoundError("Analisis no encontrado para esta incidencia")

    logger.info(f"Analisis encontrado para la incidencia: {incident_id}")
    return {
        "analysis_summary": incident.analysis_summary,
        "category": incident.category,
        "priority": incident.priority,
        "analysis_confidence": incident.analysis_confidence,
    }


# Funcion que analiza el texto de una incidencia segun id
# Primero se analiza usando reglas, y dependiendo del resultado, se llamara al LLM o no
# Tambien indicara que prompt usar en el LLM, para mas eficiencia
def analyze_incident(incident_id: int, db: Session) -> Incident:
    logger.info(f"Analizando incidencia con ID: {incident_id}")
    # Obtenemos la incidencia y comprobamos que existe
    incident = get_incident_by_id(incident_id, db)

    # Indicamos cada campo correspondiente de la incidencia a tratar
    logger.info(f"Analizando incidencia {incident_id} usando reglas")
    rules_result = analyze_text_with_rules(incident.title, incident.description)

    final_analysis: AnalysisResult

    # Si el sistema de reglas lo indica, usamos el LLM
    if rules_result.use_llm:
        try:
            logger.info(f"Las reglas dictan el uso de LLM para analizar la incidencia {incident_id}")
            text_to_analyze = _prepare_llm_text(incident)
            
            logger.info(f"Analizando incidencia {incident_id} usando LLM")
            analysis_dict = analyze_text_with_llm(text_to_analyze, rules_result.analysis_type)
            
            # La validación se realiza automáticamente al instanciar el esquema
            final_analysis = AnalysisResult(**analysis_dict)

        except (LLMServiceUnavailableError, InvalidLLMResponseError, Exception) as e:
            logger.warning(f"Fallo en servicio LLM ({str(e)}). Aplicando fallback")
            final_analysis = _get_llm_fallback_values(rules_result)
    else:
        # Si no, pues simplemente guardamos el resultado dado por las reglas
        final_analysis = AnalysisResult(
            summary=rules_result.summary,
            category=rules_result.category,
            priority=rules_result.priority,
            confidence=rules_result.confidence
        )

    # Metemos los datos en la incidencia y lo metemos en la bd
    _apply_analysis_to_incident(incident, final_analysis)
    
    logger.info(f"Guardando el resultado del analisis para la incidencia {incident_id}")
    return db_operations.save(db, incident)



# Funciones privadas
# Funciones concretas utilizadas en algunas de las funciones anteriores
# Esta decision es recomendada en el libro "Clean Code" 
# Son funciones que se usan de forma puntual y solo sirven para estos servicios
# Por tanto, mejor dejarlas aqui y al final del fichero
def _prepare_llm_text(incident: Incident) -> str:
    # Establecemos el texto a analizar, en este caso el titulo y la descripcion de la incidencia
    return f"Title: {incident.title}\nDescription: {incident.description}"

def _get_llm_fallback_values(rules_result) -> AnalysisResult:
    # Fallback del LLM, se guarda como analis el resultado de las reglas
    # Ahora usamos el schema definido para la respuesta
    return AnalysisResult(
        summary="Fallback: Sin resumen",
        category="Fallback: Sin categoria",
        priority=rules_result.priority,
        confidence=0.5
    )

def _apply_analysis_to_incident(incident: Incident, analysis_data: AnalysisResult):
    # Introducimos el resultado del analisis en la incidencia
    incident.analysis_summary = analysis_data.summary
    incident.category = analysis_data.category
    incident.priority = analysis_data.priority
    incident.analysis_confidence = analysis_data.confidence
