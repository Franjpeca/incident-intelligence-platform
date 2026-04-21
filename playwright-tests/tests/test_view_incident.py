import pytest
from playwright.sync_api import expect

from pages.view_incident_page import ViewIncidentPage

# Funcion que realiza el test de observar una incidencia usando el id
# create_incident_id para poder usar la funcion auxiliar de crear incidencia
def test_view_incident_by_id(page, base_url, create_incident_id):

    incident = create_incident_id
    incident_id = incident["id"]

    view_page = ViewIncidentPage(page, base_url)

    view_page.goto()
    view_page.search_incident_by_id(incident_id)

    # Obtenemos feedback para asegurarnos de que se ha obtenido bien respuesta
    search_feedback_locator = view_page.get_search_feedback_locator()
    
    try:
        expect(search_feedback_locator).to_contain_text("Incidencia encontrada", ignore_case=True)
    except AssertionError:
        error_busqueda = search_feedback_locator.inner_text()
        pytest.fail(f"Error al buscar la incidencia {incident_id}: {error_busqueda}")

    search_response = view_page.get_search_response_locator().inner_text().lower()
    assert f'"id": {incident_id}' in search_response
    assert f'"title": "{incident["title"].lower()}"' in search_response

# Funcion test que prueba a mostrar todas las incidencias
# create_incident_id para poder usar la funcion auxiliar de crear incidencia
def test_view_all_incidents(page, base_url, create_incident_id):

    incident = create_incident_id
    incident_id = incident["id"]

    view_page = ViewIncidentPage(page, base_url)

    view_page.goto()

    view_page.load_all_incidents()

    expect(view_page.get_list_feedback_locator()).to_contain_text("cargadas", ignore_case=True)

    feedback = view_page.get_list_feedback_locator().inner_text().lower()
    incidents_text = view_page.get_incidents_list_locator().inner_text().lower()

    assert incident_id is not None
    assert "incidencias cargadas" in feedback or "correctamente" in feedback
    assert incident["title"].lower() in incidents_text