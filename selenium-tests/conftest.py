import pytest
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.create_incident_page import CreateIncidentPage

# Pruebas en "local"
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Decorador necesario para que pytest entienda que no es un test, sino una utilidad
@pytest.fixture
def base_url():
    # Se indica a que web realizar los tests
    return "http://localhost:5500"



@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service)
    
    driver.maximize_window()
    
    yield driver
    driver.quit()




# Fixture auxiliar para crear una incidencia
# Se usara en otros test, por lo que es correcto hubicarlo aqui para reutilizar
@pytest.fixture
def fixture_create_incident(driver, base_url):
    create_page = CreateIncidentPage(driver, base_url)
    create_page.goto()

    create_page.create_incident("Test Selenium", "Descripcion Selenium")

    try:
        # Esperamos mensaje de exito
        create_page.wait_for_success_feedback()

        # Obtenemos respuesta JSON
        response_text = create_page.get_response_text()
        incident_data = json.loads(response_text)

        return incident_data

    except Exception:
        error_visible = create_page.get_feedback_text()

        pytest.fail(
            f"No se pudo crear la incidencia.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )