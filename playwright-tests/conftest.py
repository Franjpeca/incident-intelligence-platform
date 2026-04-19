from pages.create_incident_page import CreateIncidentPage
import pytest
import json
from playwright.sync_api import expect



@pytest.fixture
def create_incident_id(page, base_url):
    # Obtenemos la pagina como objeto y navegamos
    create_page = CreateIncidentPage(page, base_url)
    create_page.goto()
    # Creamos una incidencia
    create_page.create_incident("Incident for Search", "Description")
    
    feedback = create_page.get_feedback_locator()
    response = create_page.get_response_locator()

    try:
        # Esperamos el mensaje de exito
        expect(feedback).to_contain_text("correctamente", ignore_case=True)
        
        # En tal caso, extraemos el id
        response.wait_for(state="attached") 
        
        incident_data = json.loads(response.inner_text())
        return incident_data["id"]
        
    except Exception as e:
        #Si no se ha recibido o si no ha devuelto un id valido
        error_msg = feedback.inner_text() if feedback.is_visible() else "No visible feedback"
        # Forzamos el fallo del test
        pytest.fail(f"Setup Error: No se pudo crear la incidencia inicial. Web dice: {error_msg}")