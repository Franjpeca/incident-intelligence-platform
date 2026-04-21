import pytest
from playwright.sync_api import expect

from pages.incident_analysis_page import IncidentAnalysisPage



# Funcion test que prueba lanzar el analisis de una incidencia
def test_analyze_incident(page, base_url, create_incident_id):

    incident_id = create_incident_id["id"]

    analysis_page = IncidentAnalysisPage(page, base_url)

    analysis_page.goto()

    analysis_page.analyze_incident(incident_id)

    incident_analysis_feedback_locator = analysis_page.get_incident_analysis_feedback_locator()

    try:
        expect(incident_analysis_feedback_locator).to_contain_text(
            "Analisis lanzado correctamente", 
            ignore_case=True,
            timeout=60000 # Damos tiempo al modelo, en este caso, alto
            )
    except AssertionError:
        error_analysis = incident_analysis_feedback_locator.inner_text()
        pytest.fail(f"Error al analizar la incidencia {incident_id}: {error_analysis}")

    incident_analysis_response = analysis_page.get_incident_analysis_response_locator().inner_text().lower()
    assert incident_analysis_response != ""
    assert "analysis" in incident_analysis_response or "summary" in incident_analysis_response or "confidence" in incident_analysis_response




# Funcion test que prueba obtener el analisis de una incidencia
def test_get_incident_analysis(page, base_url, create_incident_id):

    incident_id = create_incident_id["id"]

    analysis_page = IncidentAnalysisPage(page, base_url)

    analysis_page.goto()

    analysis_page.analyze_incident(incident_id)

    incident_analysis_feedback_locator = analysis_page.get_incident_analysis_feedback_locator()

    try:
        expect(incident_analysis_feedback_locator).to_contain_text(
            "Analisis lanzado correctamente", 
            ignore_case=True,
            timeout=60000
            )
    except AssertionError:
        error_analysis = incident_analysis_feedback_locator.inner_text()
        pytest.fail(f"No se pudo lanzar el analisis previo de la incidencia {incident_id}: {error_analysis}")

    analysis_page.get_incident_analysis(incident_id)

    get_incident_analysis_feedback_locator = analysis_page.get_get_incident_analysis_feedback_locator()

    try:
        expect(get_incident_analysis_feedback_locator).to_contain_text(
            "Analisis obtenido correctamente", 
            ignore_case=True,
            timeout=60000
            )
    except AssertionError:
        error_get_analysis = get_incident_analysis_feedback_locator.inner_text()
        pytest.fail(f"Error al obtener el analisis de la incidencia {incident_id}: {error_get_analysis}")

    get_incident_analysis_response = analysis_page.get_get_incident_analysis_response_locator().inner_text().lower()
    assert get_incident_analysis_response != ""
    assert "analysis" in get_incident_analysis_response or "summary" in get_incident_analysis_response or "confidence" in get_incident_analysis_response




# Funcion test que prueba usar directamente el modelo
def test_use_model(page, base_url):

    analysis_page = IncidentAnalysisPage(page, base_url)

    analysis_page.goto()

    analysis_page.use_model(
        "Servidor caido en produccion. No responde el sistema.",
        "basic_analysis"
    )

    use_model_feedback_locator = analysis_page.get_use_model_feedback_locator()

    try:
        expect(use_model_feedback_locator).to_contain_text("" \
            "Texto analizado correctamente", 
            ignore_case=True,
            timeout=60000
            )
    except AssertionError:
        error_model = use_model_feedback_locator.inner_text()
        pytest.fail(f"Error al usar el modelo directamente: {error_model}")

    use_model_response = analysis_page.get_use_model_response_locator().inner_text().lower()
    assert use_model_response != ""