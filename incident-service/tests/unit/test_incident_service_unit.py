import pytest
from app.application.services.incident_service import delete_incident
from app.infrastructure.db.models.incident_model import Incident
from app.core.exceptions import BusinessRuleError

# Test para comprobar que el servicio lee bien la regla de negocio
# La idea es ver si la regla es obtenida correctamente simulando con monkeypatch 
def test_service_prevents_delete_if_open(monkeypatch):
    # Creamos una incidencia falsa que esta abierta (no se puede borrar)
    incidencia_falsa = Incident(id=1, status="open")
    # "Engañamos" al programa para que cuando busque la incidencia, devuelva la nuestra
    def mock_get_by_id(id, db):
        return incidencia_falsa
    # Aplicamos el engaño
    # Sustituye la funcion real de obtener por id por nuestro mock para probar la logica sin tocar la base de datos
    monkeypatch.setattr("app.application.services.incident_service.get_incident_by_id", mock_get_by_id)

    # Comprobamos que el servicio lanza el error esperado al intentar borrarla
    # Usamos pytest.raises que es la forma estandard de decir "espero este error"
    with pytest.raises(BusinessRuleError):
        # El parametro db da igual porque lo hemos mockeado arriba, pasamos None
        delete_incident(incident_id=1, db=None)