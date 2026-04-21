import pytest
from playwright.sync_api import expect

from pages.create_incident_page import CreateIncidentPage
from pages.update_delete_incident_page import UpdateDeleteIncidentPage
from pages.view_incident_page import ViewIncidentPage


# Funcion auxiliar que comprueba que una incidencia existe y que puede recuperarse por id
def assert_incident_exists(view_page, incident_id, expected_title=None):

    view_page.search_incident_by_id(incident_id)

    feedback_locator = view_page.get_search_feedback_locator()

    try:
        expect(feedback_locator).to_contain_text("Incidencia encontrada", ignore_case=True)
    except AssertionError:
        error_busqueda = feedback_locator.inner_text()
        pytest.fail(f"No se pudo encontrar la incidencia {incident_id}: {error_busqueda}")

    response_text = view_page.get_search_response_locator().inner_text().lower()
    assert f'"id": {incident_id}' in response_text

    if expected_title is not None:
        assert f'"title": "{expected_title.lower()}"' in response_text


# Funcion auxiliar que comprueba que una incidencia ya no existe
def assert_incident_not_exists(view_page, incident_id):

    view_page.search_incident_by_id(incident_id)

    feedback_locator = view_page.get_search_feedback_locator()

    # La diferencia es que el "error" este caso es encontrar la incidencia
    try:
        expect(feedback_locator).to_contain_text("Error al buscar incidencia", ignore_case=True)
    except AssertionError:
        error_busqueda = feedback_locator.inner_text()
        pytest.fail(
            f"La incidencia {incident_id} seguia apareciendo tras el borrado o devolvio un mensaje inesperado: "
            f"{error_busqueda}"
        )


# --- Funciones de test ---

# Funcion test que prueba la actualizacion general de una incidencia
def test_update_incident(page, base_url, create_incident_id):

    incident_id = create_incident_id["id"]

    update_page = UpdateDeleteIncidentPage(page, base_url)

    update_page.goto()

    update_page.update_incident(
        incident_id,
        title="Titulo actualizado",
        description="Descripcion actualizada",
        status="in_progress"
    )


    update_feedback_locator = update_page.get_update_feedback_locator()

    try:
        expect(update_feedback_locator).to_contain_text("Incidencia actualizada correctamente", ignore_case=True)
    except AssertionError:
        error_update = update_feedback_locator.inner_text()
        pytest.fail(f"Error al actualizar la incidencia {incident_id}: {error_update}")

    update_response = update_page.get_update_response_locator().inner_text().lower()
    assert f'"id": {incident_id}' in update_response
    assert '"title": "titulo actualizado"' in update_response
    assert '"description": "descripcion actualizada"' in update_response
    assert '"status": "in_progress"' in update_response



# Funcion test que prueba la actualizacion unicamente del estado
def test_update_incident_status(page, base_url, create_incident_id):

    incident_id = create_incident_id["id"]

    update_page = UpdateDeleteIncidentPage(page, base_url)

    update_page.goto()

    update_page.update_status_only(incident_id, "closed")

    status_feedback_locator = update_page.get_status_feedback_locator()

    try:
        expect(status_feedback_locator).to_contain_text("Estado actualizado correctamente", ignore_case=True)
    except AssertionError:
        error_status = status_feedback_locator.inner_text()
        pytest.fail(f"Error al actualizar el estado de la incidencia {incident_id}: {error_status}")

    status_response = update_page.get_status_response_locator().inner_text().lower()
    assert f'"id": {incident_id}' in status_response
    assert '"status": "closed"' in status_response



# Funcion test que prueba el borrado de una incidencia
def test_delete_incident(page, base_url, create_incident_id):

    incident_id = create_incident_id["id"]

    update_page = UpdateDeleteIncidentPage(page, base_url)

    update_page.goto()

    update_page.update_status_only(incident_id, "closed")

    update_page.delete_incident(incident_id)

    delete_feedback_locator = update_page.get_delete_feedback_locator()

    try:
        expect(delete_feedback_locator).to_contain_text("Incidencia borrada correctamente", ignore_case=True)
    except AssertionError:
        error_delete = delete_feedback_locator.inner_text()
        pytest.fail(f"Error al borrar la incidencia {incident_id}: {error_delete}")

    view_page = ViewIncidentPage(page, base_url)
 
    view_page.goto()

    # Comprobamos usando la funcion auxiliar que ya no exista
    assert_incident_not_exists(view_page, incident_id)