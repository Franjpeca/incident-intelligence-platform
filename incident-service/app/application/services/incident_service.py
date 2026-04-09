from sqlalchemy.orm import Session
from app.infrastructure.db.models.incident_model import Incident
from app.schemas.incident_request import IncidentCreateRequest

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