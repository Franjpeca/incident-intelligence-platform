from sqlalchemy.orm import Session
from app.schemas.incident_request import IncidentCreateRequest
# Importamos las funciones de la capa de servicios
from app.application.services.incident_service import (
    create_incident,
    get_incidents,
    get_incident_by_id,
)

def create_incident_controller(data: IncidentCreateRequest, db: Session):
    return create_incident(data, db)

def get_incidents_controller(db: Session):
    return get_incidents(db)

def get_incident_by_id_controller(incident_id: int, db: Session):
    return get_incident_by_id(incident_id, db)