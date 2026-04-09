from sqlalchemy.orm import Session
from app.infrastructure.db.models.incident_model import Incident
from app.schemas.incident_request import IncidentCreateRequest

def create_incident(data: IncidentCreateRequest, db: Session) -> Incident:
    incident = Incident(
        title=data.title,
        description=data.description
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def get_incidents(db: Session):
    return db.query(Incident).all()