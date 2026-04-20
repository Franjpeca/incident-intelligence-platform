from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.schemas.incident_request import IncidentCreateRequest
from app.infrastructure.db.models.incident_model import Incident
from app.schemas.incident_update_request import IncidentUpdateRequest
from app.domain.enums.incident_status import IncidentStatus
    


# Importamos las funciones de la capa de servicios
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

# Introducir una incidencia
def create_incident_controller(data: IncidentCreateRequest, db: Session) -> Incident:
    return create_incident(data, db)

# Obtener todas las incidencias
def get_incidents_controller(db: Session) -> List[Incident]:
    return get_incidents(db)

# Obtener una incidencia por su id
def get_incident_by_id_controller(incident_id: int, db: Session) -> Incident:
    return get_incident_by_id(incident_id, db)

# Modificar el estado de una incidencia
def update_incident_status_controller(incident_id: int, status: IncidentStatus, db: Session) -> Incident:
    return update_incident_status(incident_id, status, db)

# Elimina una incidencia
def delete_incident_controller(incident_id: int, db: Session) -> bool:
    return delete_incident(incident_id, db)

# Actualiza por completo una incidencia usando el id
def update_incident_controller(incident_id: int, data: IncidentUpdateRequest, db: Session) -> Incident:
    return update_incident(incident_id, data, db)

# Analiza una incidencia
def analyze_incident_controller(incident_id: int, db: Session) -> Incident:
    return analyze_incident(incident_id, db)

# Obtener analisis de uan incidencia
def get_incident_analysis_controller(incident_id: int, db: Session) -> Dict[str, Any]:
    return get_incident_analysis(incident_id, db)