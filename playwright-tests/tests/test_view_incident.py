import json
import pytest
from playwright.sync_api import expect


# Necesitamos crear una incidencia para testear
# Nota: La idea es hacer pruebas usando la web, suponiendo que no tenemos acceso a la API
from pages.create_incident_page import CreateIncidentPage
from pages.view_incident_page import ViewIncidentPage

import json
import pytest
from playwright.sync_api import expect


@pytest.fixture
def create_incident_id(page, base_url):
    # Obtenemos la pagina como objeto y navegamos
    create_page = CreateIncidentPage(page, base_url)
    create_page.goto()
    
    # Creamos una incidencia
    create_page.create_incident("Incident for search", "Description for search")
    
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

# Funcion que realiza el test de observar una incidencia usando el id
# create_incident_id para poder usar la funcion auxiliar de crear incidencia
def test_view_incident_by_id(page, base_url, create_incident_id):
    # Creamos la incidencia
    incident_id = create_incident_id
    # Creamos la pagina de ver incidencias
    view_page = ViewIncidentPage(page, base_url)
    # Navegamos a la pagina
    view_page.goto()
    view_page.search_incident_by_id(incident_id)

    # Obtenemos feedback para asegurarnos de que se ha obtenido bien respuesta
    search_feedback_locator = view_page.get_search_feedback_locator()
    
    try:
        expect(search_feedback_locator).to_contain_text("Incidencia encontrada", ignore_case=True)
    except AssertionError:
        error_busqueda = search_feedback_locator.inner_text()
        pytest.fail(f"Error al buscar la incidencia {incident_id}: {error_busqueda}")

    # Si todo va bien, hacemos los asserts finales de los datos
    search_response = view_page.get_search_response_locator().inner_text().lower()
    assert f'"id": {incident_id}' in search_response
    assert '"title": "incident for search"' in search_response

# Funcion test que prueba a mostrar todas las incidencias
# create_incident_id para poder usar la funcion auxiliar de crear incidencia
def test_view_all_incidents(page, base_url, create_incident_id):
    # Creamos la incidencia
    incident_id = create_incident_id
    # Creamos la pagina de ver incidencias
    view_page = ViewIncidentPage(page, base_url)
    # Navegamos a la pagina
    view_page.goto()
    # Cargamos todas las incidencias
    view_page.load_all_incidents()

    expect(view_page.get_list_feedback_locator()).to_contain_text("cargadas", ignore_case=True)

    feedback = view_page.get_list_feedback_locator().inner_text().lower()
    incidents_text = view_page.get_incidents_list_locator().inner_text().lower()

    assert incident_id is not None
    assert "incidencias cargadas" in feedback or "correctamente" in feedback
    assert "incident for search" in incidents_text