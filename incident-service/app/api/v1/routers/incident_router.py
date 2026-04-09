from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.controllers.incident_controller import (
    create_incident_controller,
    get_incidents_controller,
    get_incident_by_id_controller,
)
from app.infrastructure.db.session import get_db
from app.schemas.incident_request import IncidentCreateRequest
from app.schemas.incident_response import IncidentResponse

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

@router.post("", response_model=IncidentResponse)
# Creacion de una incidencia, data viene del usuario y db no, por el depends
def create_incident(data: IncidentCreateRequest, db: Session = Depends(get_db)):
    return create_incident_controller(data, db)


@router.get("", response_model=list[IncidentResponse])
# Obtiene todos los datos de la tabla de incidencias. Devuelve en este caso una lista
def get_incidents(db: Session = Depends(get_db)):
    return get_incidents_controller(db)

# Aqui indicamos que el id va en la ruta
# Luego, en la funcion indicamos el nombre del parametro y lo reconoce
@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident_by_id(incident_id: int, db: Session = Depends(get_db)):
    incident = get_incident_by_id_controller(incident_id, db)

    if incident is None:
        raise HTTPException(status_code=404, detail="La incidencia con ese id no existe")

    return incident