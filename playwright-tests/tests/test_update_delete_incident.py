import json
import pytest
from playwright.sync_api import expect

from pages.create_incident_page import CreateIncidentPage
from pages.update_delete_incident_page import UpdateDeleteIncidentPage
from pages.view_incident_page import ViewIncidentPage

# Funcion auxiliar para crear una incidencia
@pytest.fixture
def create_incident_id(page, base_url):
    # Obtenemos la pagina como objeto y navegamos
    create_page = CreateIncidentPage(page, base_url)
    create_page.goto()

    # Creamos una incidencia
    create_page.create_incident("Incident for update", "Description for update")

    # Obtenemos el feedback, para ver si se ha ejecutado bien
    feedback_locator = create_page.get_feedback_locator()

    try:
        # Esperamos el mensaje de exito
        expect(feedback_locator).to_contain_text("Incidencia creada correctamente", ignore_case=True)

        # En tal caso, extraemos el id
        response_text = create_page.get_response_locator().inner_text()
        incident_data = json.loads(response_text)
        return incident_data["id"]

    except AssertionError:
        #Si no se ha recibido o si no ha devuelto un id valido
        error_visible_en_web = feedback_locator.inner_text()

        # Forzamos el fallo del test
        pytest.fail(
            f"La precondicion fallo: No se pudo crear la incidencia.\n"
            f"Mensaje devuelto por el microservicio: '{error_visible_en_web}'"
        )


# Funcion auxiliar que comprueba que una incidencia existe y que puede recuperarse por id
def assert_incident_exists(view_page, incident_id, expected_title=None):
    # Buscamos la incidencia
    view_page.search_incident_by_id(incident_id)

    # Obtenemos feedback para asegurarnos de que se ha obtenido bien respuesta
    feedback_locator = view_page.get_search_feedback_locator()

    try:
        expect(feedback_locator).to_contain_text("Incidencia encontrada", ignore_case=True)
    except AssertionError:
        error_busqueda = feedback_locator.inner_text()
        pytest.fail(f"No se pudo encontrar la incidencia {incident_id}: {error_busqueda}")

    # Si todo va bien, hacemos los asserts finales de los datos
    response_text = view_page.get_search_response_locator().inner_text().lower()
    assert f'"id": {incident_id}' in response_text

    if expected_title is not None:
        assert f'"title": "{expected_title.lower()}"' in response_text


# Funcion auxiliar que comprueba que una incidencia ya no existe
def assert_incident_not_exists(view_page, incident_id):
    # Buscamos la incidencia
    view_page.search_incident_by_id(incident_id)

    # Obtenemos feedback para asegurarnos de que la web muestra error
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
    # Creamos la incidencia
    incident_id = create_incident_id
    # Creamos la pagina de actualizar/borrar incidencias
    update_page = UpdateDeleteIncidentPage(page, base_url)
    # Navegamos a la pagina
    update_page.goto()

    # Actualizamos campos de la incidencia
    update_page.update_incident(
        incident_id,
        title="Titulo actualizado",
        description="Descripcion actualizada",
        status="in_progress"
    )

    # Obtenemos feedback para asegurarnos de que se ha obtenido bien respuesta
    update_feedback_locator = update_page.get_update_feedback_locator()

    try:
        expect(update_feedback_locator).to_contain_text("Incidencia actualizada correctamente", ignore_case=True)
    except AssertionError:
        error_update = update_feedback_locator.inner_text()
        pytest.fail(f"Error al actualizar la incidencia {incident_id}: {error_update}")

    # Si todo va bien, hacemos los asserts finales de los datos
    update_response = update_page.get_update_response_locator().inner_text().lower()
    assert f'"id": {incident_id}' in update_response
    assert '"title": "titulo actualizado"' in update_response
    assert '"description": "descripcion actualizada"' in update_response
    assert '"status": "in_progress"' in update_response



# Funcion test que prueba la actualizacion unicamente del estado
def test_update_incident_status(page, base_url, create_incident_id):
    # Creamos la incidencia
    incident_id = create_incident_id
    # Creamos la pagina de actualizar/borrar incidencias
    update_page = UpdateDeleteIncidentPage(page, base_url)
    # Navegamos a la pagina
    update_page.goto()

    # Actualizamos solo el estado
    update_page.update_status_only(incident_id, "closed")

    # Obtenemos feedback para asegurarnos de que se ha obtenido bien respuesta
    status_feedback_locator = update_page.get_status_feedback_locator()

    try:
        expect(status_feedback_locator).to_contain_text("Estado actualizado correctamente", ignore_case=True)
    except AssertionError:
        error_status = status_feedback_locator.inner_text()
        pytest.fail(f"Error al actualizar el estado de la incidencia {incident_id}: {error_status}")

    # Si todo va bien, hacemos los asserts finales de los datos
    status_response = update_page.get_status_response_locator().inner_text().lower()
    assert f'"id": {incident_id}' in status_response
    assert '"status": "closed"' in status_response



# Funcion test que prueba el borrado de una incidencia
def test_delete_incident(page, base_url, create_incident_id):
    # Creamos la incidencia
    incident_id = create_incident_id
    # Creamos la pagina de actualizar/borrar incidencias
    update_page = UpdateDeleteIncidentPage(page, base_url)
    # Navegamos a la pagina
    update_page.goto()

    # Borramos la incidencia
    update_page.delete_incident(incident_id)

    # Obtenemos feedback para asegurarnos de que se ha obtenido bien respuesta
    delete_feedback_locator = update_page.get_delete_feedback_locator()

    try:
        expect(delete_feedback_locator).to_contain_text("Incidencia borrada correctamente", ignore_case=True)
    except AssertionError:
        error_delete = delete_feedback_locator.inner_text()
        pytest.fail(f"Error al borrar la incidencia {incident_id}: {error_delete}")

    # Creamos la pagina de ver incidencias
    view_page = ViewIncidentPage(page, base_url)
    # Navegamos a la pagina
    view_page.goto()

    # Comprobamos usando la funcion auxiliar que ya no exista
    assert_incident_not_exists(view_page, incident_id)