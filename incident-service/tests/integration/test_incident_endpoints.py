from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.infrastructure.db.models.incident_model import Incident



from app.main import app

# Simula un servidor, para poder realizar los tests
client = TestClient(app)

# Test de integracion que comprueba que el router funciona correctamente
# Se comprueba que la ruta es correcta, que se recibe un JSON y se transforma a objeto de python correctamente, etc 
def test_create_incident_endpoint(monkeypatch):
    # Monkeypatch permite que no se llame a la funcion del controlador, sino a una mock
    # La idea es comprobar las llamadas, no el propio funcionamiento, pues es una prueba de integracion

    # Simulacion de la funcion de crear incidencia, devuelve una respuesta mock
    def mock_create_incident_controller(data, db):
        now = datetime.now(timezone.utc)
        
        return Incident(
            id=1,
            title=data.title,
            description=data.description,
            status="open",
            priority="medium",
            category="general",
            created_at=now,
            updated_at=now  
        )

    # Atributos necesarios para poder llamar a la funcion mock
    monkeypatch.setattr(
        "app.api.v1.routers.incident_router.create_incident_controller",
        mock_create_incident_controller,
    )

    # Realizamos la prueba de llamar a la API con el endoint de crear incidencia
    response = client.post(
        "/api/v1/incidents",
        json={
            "title": "Servidor caido",
            "description": "La aplicacion no responde",
        },
    )

    # Elementos que se espera que se obtengan de la funcion simulada, si no, el test falla
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Servidor caido"
    assert body["description"] == "La aplicacion no responde"
    assert body["status"] == "open"


# Test de integracion para simular una respuesta erronea (no existe incidencia en la base de datos)
def test_get_incident_by_id_returns_404(monkeypatch):
    # Funcion mock para simular una incidencia no encontrada
    def mock_get_incident_by_id_controller(incident_id, db):
        return None

    # Atributos necesarios para llamar a la funcion mock
    monkeypatch.setattr(
        "app.api.v1.routers.incident_router.get_incident_by_id_controller",
        mock_get_incident_by_id_controller,
    )

    # Simulamos una llamada a dicho endpoint con una incidencia inexistente
    response = client.get("/api/v1/incidents/999")

    # Se espera que se devuelva el error de incidencia no encontrada
    assert response.status_code == 404
    assert response.json()["detail"] == "La incidencia con ese id no existe"