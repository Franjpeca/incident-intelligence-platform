import pytest

from pages.incident_analysis_page import IncidentAnalysisPage


# Funcion test que prueba lanzar el analisis de una incidencia
def test_analyze_incident(driver, base_url, fixture_create_incident):
    incident_id = fixture_create_incident["id"]

    analysis_page = IncidentAnalysisPage(driver, base_url)

    analysis_page.goto()

    analysis_page.analyze_incident(incident_id)

    try:
        analysis_page.wait_for_incident_analysis_success_feedback()
    except Exception:
        error_visible = analysis_page.get_incident_analysis_feedback_text()

        pytest.fail(
            f"No se pudo lanzar el analisis de la incidencia con id {incident_id}.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    feedback = analysis_page.get_incident_analysis_feedback_text().lower()
    response = analysis_page.get_incident_analysis_response_text().lower()

    assert "analisis lanzado correctamente" in feedback
    assert response != ""


# Funcion test que prueba obtener el analisis de una incidencia
def test_get_incident_analysis(driver, base_url, fixture_create_incident):

    incident_id = fixture_create_incident["id"]

    analysis_page = IncidentAnalysisPage(driver, base_url)

    analysis_page.goto()

    analysis_page.analyze_incident(incident_id)

    try:
        analysis_page.wait_for_incident_analysis_success_feedback()
    except Exception:
        error_visible = analysis_page.get_incident_analysis_feedback_text()

        pytest.fail(
            f"No se pudo lanzar el analisis previo de la incidencia con id {incident_id}.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    analysis_page.get_incident_analysis(incident_id)

    try:
        analysis_page.wait_for_get_incident_analysis_success_feedback()
    except Exception:
        error_visible = analysis_page.get_get_incident_analysis_feedback_text()

        pytest.fail(
            f"No se pudo obtener el analisis de la incidencia con id {incident_id}.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    feedback = analysis_page.get_get_incident_analysis_feedback_text().lower()
    response = analysis_page.get_get_incident_analysis_response_text().lower()

    assert "analisis obtenido correctamente" in feedback
    assert response != ""


# Funcion test que prueba usar directamente el modelo
def test_use_model(driver, base_url):

    analysis_page = IncidentAnalysisPage(driver, base_url)

    analysis_page.goto()

    analysis_page.use_model(
        "Servidor caido en produccion. No responde el sistema."
    )

    try:
        analysis_page.wait_for_use_model_success_feedback()
    except Exception:
        error_visible = analysis_page.get_use_model_feedback_text()

        pytest.fail(
            f"No se pudo usar el modelo directamente.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    feedback = analysis_page.get_use_model_feedback_text().lower()
    response = analysis_page.get_use_model_response_text().lower()

    assert "texto analizado correctamente" in feedback
    assert response != ""