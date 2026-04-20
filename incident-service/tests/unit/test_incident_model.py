from app.infrastructure.db.models.incident_model import Incident
from app.domain.enums.incident_status import IncidentStatus

# Test unitario para comprobar si una incidencia se puede borrar segun su estado
def test_can_be_deleted_logic():
    # Caso 1: La incidencia esta closed
    # Debe de devolter true
    incidencia_cerrada = Incident(status=IncidentStatus.CLOSED.value)
    assert incidencia_cerrada.can_be_deleted() == True

    # Caso 2: Incidencia abierta. 
    # Deberia devolver false
    incidencia_abierta = Incident(status=IncidentStatus.OPEN.value)
    assert incidencia_abierta.can_be_deleted() == False