from pages.create_incident_page import CreateIncidentPage
from playwright.sync_api import expect

# Funcion que comprobara la creacion de una incidencia
def test_create_incident(page, base_url):
    # Obtenemos la pagina como objeto
    create_page = CreateIncidentPage(page, base_url)
    # Vamos a esa propia pagina (la web de crear incidencia)
    create_page.goto()

    create_page.create_incident(
        "Incidencia de prueba con Playwright", 
        "Cuerpo de dicha incidencia"
    )

    # Buscamos evitar condiciones de carrera (se ejecuta antes los asertos que la respuesta)
    feedback_locator = create_page.get_feedback_locator()

    expect(feedback_locator).to_contain_text("Incidencia creada correctamente", ignore_case=True)


    # Obtenemos el valor de feedback
    feedback = create_page.get_feedback_locator().inner_text().lower()
    # Validamos que la respuesta es un JSON con la estructura correcta
    response = create_page.get_response_locator().inner_text().lower()

    assert "incidencia creada correctamente" in feedback
    assert '"id"' in response