import pytest
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.create_incident_page import CreateIncidentPage

@pytest.fixture
def base_url():
    # Usamos la URL que sea correcta en docker, sino localhost
    return os.getenv("BASE_URL", "http://localhost:5500")

@pytest.fixture
def driver():
    # Detectamos si estamos en Docker
    IN_DOCKER = os.getenv("TESTS_IN_PRODUCTION", "False").lower() == "true"
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if IN_DOCKER:
        # Configuracion para docker
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        # Configuracion para local
        chrome_options.add_argument("--start-maximized")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver
    driver.quit()

@pytest.fixture
def fixture_create_incident(driver, base_url):
    create_page = CreateIncidentPage(driver, base_url)
    create_page.goto()
    create_page.create_incident("Test Selenium", "Descripcion Selenium")

    try:
        create_page.wait_for_success_feedback()
        response_text = create_page.get_response_text()
        return json.loads(response_text)
    except Exception:
        error_visible = create_page.get_feedback_text()
        pytest.fail(f"No se pudo crear la incidencia de prueba. Web dice: '{error_visible}'")