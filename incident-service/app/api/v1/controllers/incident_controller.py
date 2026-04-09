from sqlalchemy.orm import Session
from app.schemas.incident_request import IncidentCreateRequest
from app.application.services.incident_service import create_incident, get_incidents

def create_incident_controller(data: IncidentCreateRequest, db: Session):
    return create_incident(data, db)

def get_incidents_controller(db: Session):
    return get_incidents(db)