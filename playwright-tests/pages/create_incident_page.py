from .base_page import BasePage

class CreateIncidentPage(BasePage):

    def goto(self):
        super().goto("/pages/create-incident.html")

    # Metodo para crear una incidencia en esa pagina, usando el titulo y descripcion indicados
    def create_incident(self, title, description):
        self.page.fill("#title", title)
        self.page.fill("#description", description)
        self.page.click("button[type='submit']")

    # Funciones para tratar condiciones de carrera
    def get_feedback_locator(self):
        return self.page.locator("#feedback")
    
    def get_response_locator(self):
        return self.page.locator("#response")