# Importamos la clase de la pagina de creacion de incidencia
import pytest
from pages.create_incident_page import CreateIncidentPage
from playwright.sync_api import expect

# Funcion que comprobara la creacion de una incidencia
def test_create_incident(page, base_url):
    # Obtenemos la pagina como objeto
    create_page = CreateIncidentPage(page, base_url)
    # Vamos a esa propia pagina (la web de crear incidencia)
    create_page.goto()
    # Creamos una incidencia con el titulo y descripcion deseado
    create_page.create_incident(
        "Incidencia de prueba con Playwright", 
        "Cuerpo de dicha incidencia"
    )

    # Buscamos evitar condiciones de carrera (se ejecuta antes los asertos que la respuesta)
    feedback_locator = create_page.get_feedback_locator()
    # Usamos expect para manejar la asincronía: reintenta hasta que el texto aparece 
    # evitando fallos si la API tarda unos milisegundos, espera hasta un maximo de 5 segundos
    expect(feedback_locator).to_contain_text("Incidencia creada correctamente", ignore_case=True)


    # Obtenemos el valor de feedback
    feedback = create_page.get_feedback_locator().inner_text().lower()
    # Validamos que la respuesta es un JSON con la estructura correcta
    response = create_page.get_response_locator().inner_text().lower()

    # Con pytest, comprobamos con asertos que correctamente se ha obtenido lo deseado
    assert "incidencia creada correctamente" in feedback
    assert '"id"' in response