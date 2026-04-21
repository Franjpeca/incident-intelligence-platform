from sqlalchemy.orm import Session
from app.infrastructure.db.models.incident_model import Incident
from app.core.exceptions import DatabaseOperationError
import logging

logger = logging.getLogger(__name__)

def get_by_id(db: Session, incident_id: int):
    # En este caso, devuelve el primero que encuentra
    return db.query(Incident).filter(Incident.id == incident_id).first()

def list_incidents(db: Session, limit: int = 100):
    return db.query(Incident).order_by(Incident.created_at.desc()).limit(limit).all()

def save(db: Session, incident: Incident):
    try:
        db.add(incident)
        db.commit()
        db.refresh(incident)
        return incident
    except Exception as e:
        logger.warning(f"Fallo en la operacion de la incidencia")
        db.rollback()
        raise DatabaseOperationError("Error al procesar la operacion en la base de datos")
    

def delete(db: Session, incident: Incident):
    try:
        db.delete(incident)
        db.commit()
        return True
    except Exception:
        db.rollback()
        logger.exception("Error fatal al eliminar en la base de datos")
        raise DatabaseOperationError("Error al eliminar el registro")