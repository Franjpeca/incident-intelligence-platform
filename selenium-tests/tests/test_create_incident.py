import json
import pytest

from pages.create_incident_page import CreateIncidentPage

# Test principal
def test_create_incident(driver, base_url):
    create_page = CreateIncidentPage(driver, base_url)
    create_page.goto()

    create_page.create_incident("Test usando selenium", "Descripcion directa")

    try:
        create_page.wait_for_success_feedback()
    except Exception:
        error_visible = create_page.get_feedback_text()
        pytest.fail(f"Error al crear incidencia: {error_visible}")

    # Validaciones finales
    feedback = create_page.get_feedback_text().lower()
    response = create_page.get_response_text().lower()

    assert "incidencia creada correctamente" in feedback
    assert "id" in response
    assert "test usando selenium" in response