from sqlalchemy.orm import Session
from app.infrastructure.db.models.incident_model import Incident
from app.schemas.incident_request import IncidentCreateRequest
from app.domain.enums.incident_status import IncidentStatus
from app.infrastructure.clients.llm_service_client import analyze_text_with_llm
from app.core.exceptions import (
    IncidentNotFoundError,
    InvalidLLMResponseError,
    DatabaseOperationError,
)

from app.core.exceptions import (
    IncidentNotFoundError,
    AnalysisNotFoundError,
    InvalidLLMResponseError,
    DatabaseOperationError,
)

# Funcion que crea un registro de la tabla y lo introduce en la bd
def create_incident(data: IncidentCreateRequest, db: Session) -> Incident:
    # Bloque try para poder manejar cualquier error al acceder a la bd o al crear el objeto
    try:
        incident = Incident(
            title=data.title,
            description=data.description
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)

        return incident
    except Exception:
        db.rollback()
        raise DatabaseOperationError("Error al crear la incidencia")

# Obtiene todos los registros de la tabla de la bd
def get_incidents(db: Session):
    try:
        return db.query(Incident).all()
    except Exception:
        raise DatabaseOperationError("Error al obtener las incidencias")

# Obtiene un registro de la tabla usando su id
def get_incident_by_id(incident_id: int, db: Session):
    # En este caso, devuelve el primero que encuentra
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # SELECT * FROM incident WHERE id = incident_id LIMIT 1

    # Aqui no hacemos try porque puede devolver un valor vacio, no un fallo como tal
    if incident is None:
        raise IncidentNotFoundError("Incidencia no encontrada")

    return incident

# Actualiza el estado de una incidencia
def update_incident_status(incident_id: int, status: IncidentStatus, db: Session):
    # Consulta la BD y busca la incidencia
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # Devuelve None si no la encuentra
    if incident is None:
        raise IncidentNotFoundError("Incidencia no encontrada")
    # Si la encuentra, actualiza el estado
    # Hasta aqui similar a al funcion anterior

    # Aqui si hacemos un try porque es acceso a la bd y modificacion
    try:
        incident.status = status.value
        db.commit()
        db.refresh(incident)
        return incident
    except Exception:
        db.rollback()
        raise DatabaseOperationError("Error al actualizar el estado de la incidencia")

# Eliminar una incidencia dada su id
def delete_incident(incident_id: int, db: Session):
    # Similar a la funcion anterior
    # Consultamos y vemos si existe
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # Devolvemos None si no existe
    if incident is None:
        raise IncidentNotFoundError("Incidencia no encontrada")
    # DELETE FROM incident WHERE id = incident_id
    try:
        db.delete(incident)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise DatabaseOperationError("Error al eliminar la incidencia")

# Actualiza por completo una incidencia segun el id
def update_incident(incident_id: int, data, db: Session):
    # Similar a las funciones anteriores
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if incident is None:
        raise IncidentNotFoundError("Incidencia no encontrada")

    # La diferencia es que aqui asignamos valores antes de hacer el commit en la bd
    try:
        incident.title = data.title
        incident.description = data.description
        incident.status = data.status.value

        db.commit()
        db.refresh(incident)

        return incident
    except Exception:
        db.rollback()
        raise DatabaseOperationError("Error al actualizar la incidencia")

# Funcion que analiza el texto de una incidencia segun id
# Utiliza el codigo correspondiente para comunicarse con el microservicio del LLM
def analyze_incident(incident_id: int, db: Session):
    # Obtenemos la incidencia y comprobamos que existe
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if incident is None:
        raise IncidentNotFoundError("Incidencia no encontrada")

    # Establecemos el texto a analizar, en este caso el titulo y la descripcion de la incidencia
    text_to_analyze = f"Title: {incident.title}\nDescription: {incident.description}"
    analysis = analyze_text_with_llm(text_to_analyze)

    # Comprobamos que el json obtenido del LLM tiene los campos necesarios, si no es asi, lanzamos un error
    if not all(key in analysis for key in ["summary", "category", "priority", "confidence"]):
        raise InvalidLLMResponseError("Respuesta invalida del servicio LLM")

    # Introducimos el resultado del analisis en la incidencia y lo metemos en la bd
    # Nos aseguramos de que se guarda bien, si no, error
    try:
        incident.ai_summary = analysis["summary"]
        incident.category = analysis["category"]
        incident.priority = analysis["priority"]
        incident.ai_confidence = analysis["confidence"]

        db.commit()
        db.refresh(incident)

        return incident
    except Exception:
        db.rollback()
        raise DatabaseOperationError("Error al guardar el analisis")

# Getter del analisis de una incidencia usando el id
def get_incident_analysis(incident_id: int, db: Session):
    # Indicamos el id de la incidencia de la que obtenemos el id
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # Si no hay incidencia con ese id, devolvemos none

    # Comprobamos si la incidencia existe, si no, error
    if incident is None:
        raise IncidentNotFoundError("Incidencia no encontrada")
    
    if incident.ai_summary is None:
        raise AnalysisNotFoundError("Analysis not found for this incident")

    return {
        "ai_summary": incident.ai_summary,
        "category": incident.category,
        "priority": incident.priority,
        "ai_confidence": incident.ai_confidence,
    }