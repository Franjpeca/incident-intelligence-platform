import logging

from sqlalchemy.orm import Session
from app.infrastructure.db.models.incident_model import Incident
from app.schemas.incident_request import IncidentCreateRequest
from app.domain.enums.incident_status import IncidentStatus
from app.infrastructure.clients.llm_service_client import analyze_text_with_llm
from app.application.services.incident_rules_service import analyze_text_with_rules

from app.core.exceptions import (
    IncidentNotFoundError,
    InvalidLLMResponseError,
    DatabaseOperationError,
    AnalysisNotFoundError,
    FieldError,
    LLMServiceUnavailableError,
)

logger = logging.getLogger("incident-service")

# Funcion que crea un registro de la tabla y lo introduce en la bd
def create_incident(data: IncidentCreateRequest, db: Session) -> Incident:
    # Bloque try para poder manejar cualquier error al acceder a la bd o al crear el objeto
    logger.info(f"Creando incidencia: '{data.title}'")

    try:
        incident = Incident(
            title=data.title,
            description=data.description
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)

        logger.info(f"Incidencia: '{data.title}' creada exitosamente con ID: {incident.id}")
        return incident
    except Exception as e:
        logger.exception(f"Error fatal al insertar incidencia en DB: {str(e)}")

        db.rollback()
        raise DatabaseOperationError("Error al crear la incidencia")

# Obtiene todos los registros de la tabla de la bd
def get_incidents(db: Session):
    try:
        logger.info(f"Obteniendo todas las incidencias")
        return db.query(Incident).all()
    except Exception as e:
        logger.exception(f"Error la intentar obtener todas las incidencias: {str(e)}")
        raise DatabaseOperationError("Error al obtener las incidencias")

# Obtiene un registro de la tabla usando su id
def get_incident_by_id(incident_id: int, db: Session):
    logger.info(f"Buscando incidencia con ID: {incident_id}")
    # En este caso, devuelve el primero que encuentra
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # SELECT * FROM incident WHERE id = incident_id LIMIT 1

    # Aqui no hacemos try porque puede devolver un valor vacio, no un fallo como tal
    if incident is None:
        # WARNING porque aunque no sea un error del programa, es una busqueda fallida
        logger.warning(f"Incidencia no encontrada: ID {incident_id}")

        raise IncidentNotFoundError("Incidencia no encontrada")

    return incident

# Actualiza el estado de una incidencia
def update_incident_status(incident_id: int, status: IncidentStatus, db: Session):
    logger.info(f"Actualizando estado de la incidencia con ID: {incident_id}")
    # Consulta la BD y busca la incidencia
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # Devuelve None si no la encuentra
    if incident is None:
        logger.warning(f"Incidencia no encontrada: ID {incident_id}")
        raise IncidentNotFoundError("Incidencia no encontrada")
    # Si la encuentra, actualiza el estado
    # Hasta aqui similar a al funcion anterior

    # Aqui si hacemos un try porque es acceso a la bd y modificacion
    try:

        incident.status = status.value
        db.commit()
        db.refresh(incident)
        logger.info(f"Estado de la incidencia con ID: {incident_id} actualizado")
        return incident
    except Exception as e:
        logger.warning(f"Fallo en la actualización de la incidencia: ID {incident_id}")
        db.rollback()
        raise DatabaseOperationError("Error al actualizar el estado de la incidencia")

# Eliminar una incidencia dada su id
def delete_incident(incident_id: int, db: Session):
    logger.info(f"Eliminando incidencia con ID: {incident_id}")
    # Similar a la funcion anterior
    # Consultamos y vemos si existe
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # Devolvemos None si no existe
    if incident is None:
        logger.info(f"Incidencia no encontrada: {incident_id}")
        raise IncidentNotFoundError("Incidencia no encontrada")
    # DELETE FROM incident WHERE id = incident_id
    try:
        db.delete(incident)
        db.commit()
        logger.info(f"Incidencia eliminada con ID: {incident_id}")
        return True
    except Exception as e:
        logger.warning(f"Fallo en la eliminacion de la incidencia: ID {incident_id}")
        db.rollback()
        raise DatabaseOperationError("Error al eliminar la incidencia")

# Actualiza por completo una incidencia segun el id
def update_incident(incident_id: int, data, db: Session):
    logger.info(f"Actualizando incidencia con ID: {incident_id}")
    # Similar a las funciones anteriores
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if incident is None:
        logger.info(f"Incidencia no encontrada: {incident_id}")
        raise IncidentNotFoundError("Incidencia no encontrada")

    # La diferencia es que aqui asignamos valores antes de hacer el commit en la bd
    try:
        if data.title is None and data.description is None and data.status is None:
            logger.error(f"No se recibieron campos para actualizar en la incidencia: {incident_id}")
            raise FieldError("Debes enviar al menos un campo para actualizar")

        if data.title is not None:
            incident.title = data.title
        if data.description is not None:
            incident.description = data.description
        if data.status is not None:
            incident.status = data.status.value

        db.commit()
        db.refresh(incident)
        logger.info(f"Incidencia actualizada con ID: {incident_id}")
        return incident
    except ValueError:
        db.rollback()
        raise
    except Exception as e:
        logger.warning(f"Fallo en la eliminacion de la incidencia: ID {incident_id}")
        db.rollback()
        raise DatabaseOperationError("Error al actualizar la incidencia")

# Funcion que analiza el texto de una incidencia segun id
# Primero se analiza usando reglas, y dependiendo del resultado, se llamara al LLM o no
# Tambien indicara que prompt usar en el LLM, para mas eficiencia
def analyze_incident(incident_id: int, db: Session):
    logger.info(f"Analizando incidencia con ID: {incident_id}")
    # Obtenemos la incidencia y comprobamos que existe
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    # Si no existe, lanzamos error
    if incident is None:
        logger.info(f"Incidencia no encontrada: {incident_id}")
        raise IncidentNotFoundError("Incidencia no encontrada")

    # Indicamos cada campo correspondiente de la incidencia a tratar
    logger.info(f"Analizando incidencia {incident_id} usando reglas")
    rules_result = analyze_text_with_rules(
        title=incident.title,
        description=incident.description
    )

    # Si el sistema de reglas lo indica, usamos el LLM
    if rules_result.use_llm:
        try:
            logger.info(f"Las reglas dictan el uso de LLM para analizar la incidencia {incident_id}")
            analysis_type = rules_result.analysis_type

            # Establecemos el texto a analizar, en este caso el titulo y la descripcion de la incidencia
            text_to_analyze = f"Title: {incident.title}\nDescription: {incident.description}"

            logger.info(f"Analizando incidencia {incident_id} usando LLM con el modo: {analysis_type}")
            analysis = analyze_text_with_llm(text_to_analyze, analysis_type)

            logger.info(f"Analisis completado para la incidencia {incident_id}, comprobadodo la respuesta del LLM")
            # Comprobamos que el json obtenido del LLM tiene los campos necesarios, si no es asi, lanzamos un error
            if not all(key in analysis for key in ["summary", "category", "priority", "confidence"]):
                logger.warning(f"Fallo en la generacion del analisis por parte del LLM para la incidencia: {incident_id}")
                raise InvalidLLMResponseError("Respuesta invalida del servicio LLM")

            # GUardamos el resultado obtenido por el LLM
            incident.analysis_summary = analysis["summary"]
            incident.category = analysis["category"]
            incident.priority = analysis["priority"]
            incident.analysis_confidence = analysis["confidence"]

        except (LLMServiceUnavailableError, InvalidLLMResponseError) as e:
                    # Fallback del LLM, se guarda como analis el resultado de las reglas
                    logger.warning(f"Fallo en servicio LLM ({str(e)}). Aplicando fallback de reglas para ID {incident_id}")
                    
                    incident.analysis_summary = f"Fallback: Sin resumen"
                    incident.category = "Fallback: Sin categoria"
                    incident.priority = rules_result.priority
                    incident.analysis_confidence = 0.5

    # Si no, pues simplemente guardamos el resultado
    else:
        incident.analysis_summary = rules_result.summary
        incident.category = rules_result.category
        incident.priority = rules_result.priority
        incident.analysis_confidence = rules_result.confidence

    # Introducimos el resultado del analisis en la incidencia y lo metemos en la bd
    # Nos aseguramos de que se guarda bien, si no, error
    try:
        logger.info(f"Guardando el resultado del analisis para la incidencia {incident_id} en la base de datos")
        db.commit()
        db.refresh(incident)

        return incident
    except Exception as e:
        logger.warning(f"Fallo al guardar el resultado del analisis para la incidencia: ID {incident_id}")
        db.rollback()
        raise DatabaseOperationError("Error al guardar el analisis")

# Getter del analisis de una incidencia usando el id
def get_incident_analysis(incident_id: int, db: Session):
    logger.info(f"Obteniendo analisis de la incidencia con ID: {incident_id}")
    # Indicamos el id de la incidencia de la que obtenemos el id
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # Si no hay incidencia con ese id, devolvemos none

    # Comprobamos si la incidencia existe, si no, error
    if incident is None:
        logger.info(f"Incidencia no encontrada: {incident_id}")
        raise IncidentNotFoundError("Incidencia no encontrada")
    
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