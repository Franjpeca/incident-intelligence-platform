from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.schemas.incident_request import IncidentCreateRequest
from app.infrastructure.db.models.incident_model import Incident
from app.schemas.incident_update_request import IncidentUpdateRequest
from app.domain.enums.incident_status import IncidentStatus
    
from app.application.services.incident_service import (
    create_incident,
    get_incidents,
    get_incident_by_id,
    update_incident_status,
    delete_incident,
    update_incident,
    analyze_incident,
    get_incident_analysis, 
)


def create_incident_controller(data: IncidentCreateRequest, db: Session) -> Incident:
    return create_incident(data, db)


def get_incidents_controller(db: Session) -> List[Incident]:
    return get_incidents(db)


def get_incident_by_id_controller(incident_id: int, db: Session) -> Incident:
    return get_incident_by_id(incident_id, db)


def update_incident_status_controller(incident_id: int, status: IncidentStatus, db: Session) -> Incident:
    return update_incident_status(incident_id, status, db)


def delete_incident_controller(incident_id: int, db: Session) -> bool:
    return delete_incident(incident_id, db)


def update_incident_controller(incident_id: int, data: IncidentUpdateRequest, db: Session) -> Incident:
    return update_incident(incident_id, data, db)


def analyze_incident_controller(incident_id: int, db: Session) -> Incident:
    return analyze_incident(incident_id, db)


def get_incident_analysis_controller(incident_id: int, db: Session) -> Dict[str, Any]:
    return get_incident_analysis(incident_id, db)