from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.infrastructure.db.models.incident_model import Incident
from fastapi import HTTPException


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
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Servidor caido"
    assert body["description"] == "La aplicacion no responde"
    assert body["status"] == "open"


# Test de integracion para simular una respuesta erronea (no existe incidencia en la base de datos)
def test_get_incident_by_id_returns_404(monkeypatch):
    # Funcion mock para simular una incidencia no encontrada
    def mock_get_incident_by_id_controller(incident_id, db):
        raise HTTPException(status_code=404, detail="La incidencia con ese id no existe")

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


# Test de integracion que simula el retorno de todas las incidencias
def test_get_all_incidents_endpoint(monkeypatch):
    # Funcion mock que devolveria todas las incidencias
    # Aqui no testeamos que se devuelvan todas, sino al comunicacion, por eso es integracion
    def mock_get_incidents_controller(db):
        return [
            {
                "id": 1,
                "title": "Servidor caido",
                "description": "Error en produccion",
                "status": "open",
                "priority": "high",
                "category": "software",
                "analysis_summary": None,
                "analysis_confidence": None,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            }
        ]

    # Atributos para llamar a la funcion mock
    monkeypatch.setattr(
        "app.api.v1.routers.incident_router.get_incidents_controller",
        mock_get_incidents_controller,
    )

    # Simulamos una llamada a dicho endpoint
    response = client.get("/api/v1/incidents")

    # Asertos esperados, si fallan lanzamos error
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["title"] == "Servidor caido"


# Simulamos la llamada a analizar una incidencia
def test_analyze_incident_endpoint(monkeypatch):
    # Funcion mock
    def mock_analyze_incident_controller(incident_id, db):
        return {
            "id": incident_id,
            "title": "Servidor caido",
            "description": "La aplicacion no responde",
            "status": "open",
            "priority": "high",
            "category": "software",
            "analysis_summary": "Incidencia critica detectada",
            "analysis_confidence": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

    # Atributos para el funcionamiento del mock
    monkeypatch.setattr(
        "app.api.v1.routers.incident_router.analyze_incident_controller",
        mock_analyze_incident_controller,
    )

    # Simulamos una llamada al endpoint real
    response = client.post("/api/v1/incidents/1/analysis")

    # Comprobamos si se devuelve correctamente los datos
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["priority"] == "high"
    assert body["category"] == "software"
    assert body["analysis_summary"] == "Incidencia critica detectada"