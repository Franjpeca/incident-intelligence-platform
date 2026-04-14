from fastapi.testclient import TestClient
import pytest

from app.core.exceptions import InvalidModelOutputError
from app.main import app


client = TestClient(app)

# Test de prueba del endpoint healt
def test_health_endpoint_returns_ok(monkeypatch):
    # Configuracion de monkeypatch para poder simular la funcion
    monkeypatch.setattr(
        "app.main.is_model_loaded",
        lambda: True
    )

    # Accedemos al endpoint
    response = client.get("/health")

    # Respuesta esperada
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True

# Test para comprobar la respuesta del analisis
def test_analysis_text_endpoint_returns_analysis(monkeypatch):
    # Funcion mock que simula el analisis de un texto
    def mock_analyze_text_controller(data):
        return {
            "summary": "Resumen generado",
            "category": "software",
            "priority": "high",
            "confidence": 90,
        }

    # Configuracion para simular la funcion
    monkeypatch.setattr(
        "app.api.v1.routers.analysis_router.analyze_text_controller",
        mock_analyze_text_controller,
    )

    # Realizamos la peticion
    response = client.post(
        "/api/v1/analysis/text",
        json={
            "text": "Servidor caido en produccion",
            "analysis_type": "basic_analysis",
        },
    )

    # Evaluamos la respuesta obtenida
    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == "Resumen generado"
    assert body["category"] == "software"
    assert body["priority"] == "high"