import pytest

from pages.view_incident_page import ViewIncidentPage


def test_view_incident_by_id(driver, base_url, fixture_create_incident):
    # Obtenemos el id de la incidencia creada
    incident_id = fixture_create_incident["id"]

    # Creamos la pagina de ver incidencias
    view_page = ViewIncidentPage(driver, base_url)
    # Navegamos a la pagina
    view_page.goto()

    # Buscamos la incidencia por id
    view_page.search_incident_by_id(incident_id)

    try:
        # Esperamos el mensaje de exito
        view_page.wait_for_search_success_feedback()
    except Exception:
        error_visible = view_page.get_search_feedback_text()

        pytest.fail(
            f"No se pudo encontrar la incidencia con id {incident_id}.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    # Validaciones finales
    feedback = view_page.get_search_feedback_text().lower()
    response = view_page.get_search_response_text().lower()

    assert "incidencia encontrada" in feedback
    assert f'"id": {incident_id}' in response
    assert '"title": "test selenium"' in response



def test_view_all_incidents(driver, base_url, fixture_create_incident):
    # Obtenemos la incidencia creada para asegurarnos de que existe contenido
    created_incident = fixture_create_incident

    # Creamos la pagina de ver incidencias
    view_page = ViewIncidentPage(driver, base_url)
    # Navegamos a la pagina
    view_page.goto()

    # Cargamos todas las incidencias
    view_page.load_all_incidents()

    try:
        # Esperamos el mensaje de exito
        view_page.wait_for_list_success_feedback()
    except Exception:
        error_visible = view_page.get_list_feedback_text()

        pytest.fail(
            f"No se pudieron cargar las incidencias.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    # Validaciones finales
    feedback = view_page.get_list_feedback_text().lower()
    incidents_list = view_page.get_incidents_list_text().lower()

    assert created_incident["id"] is not None
    assert "incidencias cargadas" in feedback
    assert "test selenium" in incidents_list