from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.infrastructure.db.session import get_db

from app.schemas.incident_request import IncidentCreateRequest
from app.schemas.incident_response import IncidentResponse
from app.schemas.incident_status_request import StatusUpdateRequest
from app.schemas.incident_update_request import IncidentUpdateRequest

from app.api.v1.controllers.incident_controller import (
    create_incident_controller,
    get_incidents_controller,
    get_incident_by_id_controller,
    update_incident_status_controller,
    delete_incident_controller,
    update_incident_controller,
    analyze_incident_controller,
)

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
    # Control de error si no existe dicha incidencia
    if incident is None:
        raise HTTPException(status_code=404, detail="La incidencia con ese id no existe")

    return incident

# Similar al anterior pero con /status para diferenciar
@router.patch("/{incident_id}/status", response_model=IncidentResponse)
def update_incident_status(incident_id: int, data: StatusUpdateRequest, db: Session = Depends(get_db)):
    incident = update_incident_status_controller(incident_id, data.status, db)
    # Control de error si no existe dicha incidencia
    if incident is None:
        raise HTTPException(status_code=404, detail="Error al actualizar. Incidencia no encontrada")

    return incident

# DELETE para poder eliminar una incidencia dada una id
@router.delete("/{incident_id}")
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    result = delete_incident_controller(incident_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="Error al borrar. Incidencia no encontrada")

    return {"message": "Incidencia eliminada correctamente"}

# Actualiza por completo una incidencia dada su id
# PUT espera todos los campos obligatorios en el mensaje del usuario
@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, data: IncidentUpdateRequest, db: Session = Depends(get_db)):
    incident = update_incident_controller(incident_id, data, db)

    if incident is None:
        raise HTTPException(status_code=404, detail="Error al borrar. Incidencia no encontrada")

    return incident

# Establecemos la ruta para usar el analisis usando LLM
@router.post("/{incident_id}/analysis")
def analyze_incident(incident_id: int, db: Session = Depends(get_db)):
    analysis = analyze_incident_controller(incident_id, db)

    if analysis is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return analysis