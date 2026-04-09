from sqlalchemy.orm import Session
from app.infrastructure.db.models.incident_model import Incident
from app.schemas.incident_request import IncidentCreateRequest
from app.domain.enums.incident_status import IncidentStatus
from app.infrastructure.clients.llm_service_client import analyze_text_with_llm

# Funcion que crea un registro de la tabla y lo introduce en la bd
def create_incident(data: IncidentCreateRequest, db: Session) -> Incident:
    incident = Incident(
        title=data.title,
        description=data.description
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident

# Obtiene todos los registros de la tabla de la bd
def get_incidents(db: Session):
    return db.query(Incident).all()

# Obtiene un registro de la tabla usando su id
def get_incident_by_id(incident_id: int, db: Session):
    # En este caso, devuelve el primero que encuentra
    return db.query(Incident).filter(Incident.id == incident_id).first()
    # SELECT * FROM incident WHERE id = incident_id LIMIT 1

# Actualiza el estado de una incidencia
def update_incident_status(incident_id: int, status: IncidentStatus, db: Session):
    # Consulta la BD y busca la incidencia
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # Devuelve None si no la encuentra
    if incident is None:
        return None
    # Si la encuentra, actualiza el estado
    incident.status = status.value
    db.commit()
    db.refresh(incident)

    return incident

# Eliminar una incidencia dada su id
def delete_incident(incident_id: int, db: Session):
    # Consultamos y vemos si existe
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    # Devolvemos None si no existe
    if incident is None:
        return None
    # DELETE FROM incident WHERE id = incident_id
    db.delete(incident)
    db.commit()

    return True

# Actualiza por completo una incidencia segun el id
def update_incident(incident_id: int, data, db: Session):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if incident is None:
        return None

    incident.title = data.title
    incident.description = data.description
    incident.status = data.status.value

    db.commit()
    db.refresh(incident)

    return incident

# Funcion que analiza el texto de una incidencia segun id
# Utiliza el codigo correspondiente para comunicarse con el microservicio del LLM
def analyze_incident(incident_id: int, db: Session):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if incident is None:
        return None

    text_to_analyze = f"Title: {incident.title}\nDescription: {incident.description}"
    analysis = analyze_text_with_llm(text_to_analyze)

    incident.ai_summary = analysis["summary"]
    incident.category = analysis["category"]
    incident.priority = analysis["priority"]
    incident.ai_confidence = analysis["confidence"]

    db.commit()
    db.refresh(incident)

    return incident