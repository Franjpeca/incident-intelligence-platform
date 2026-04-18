import pytest
from pages.view_incident_page import ViewIncidentPage

# Funcion auxiliar que comprueba que una incidencia existe y que puede recuperarse por id
def assert_incident_exists(driver, base_url, incident_id, expected_title=None):
    # Creamos la pagina de ver incidencias
    view_page = ViewIncidentPage(driver, base_url)
    # Navegamos a la pagina
    view_page.goto()

    # Buscamos la incidencia
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
    response = view_page.get_search_response_text().lower()

    assert f'"id": {incident_id}' in response

    if expected_title is not None:
        assert f'"title": "{expected_title.lower()}"' in response


# Funcion auxiliar que comprueba que una incidencia ya no existe
def assert_incident_not_exists(driver, base_url, incident_id):
    # Creamos la pagina de ver incidencias
    view_page = ViewIncidentPage(driver, base_url)
    # Navegamos a la pagina
    view_page.goto()

    # Buscamos la incidencia
    view_page.search_incident_by_id(incident_id)

    feedback = view_page.get_search_feedback_text().lower()
    response = view_page.get_search_response_text().lower()

    assert "no se pudo" in feedback or "error" in feedback
    assert "no encontrada" in response or "error" in response