from .base_page import BasePage

# Creamos la clase con la clase base y es la pagina de crear una incidencia
class CreateIncidentPage(BasePage):

    # Metodo para acceder a dicha pagina
    def goto(self):
        super().goto("/pages/create-incident.html")

    # Metodo para crear una incidencia en esa pagina
    # title: titulo de la incidencia, es lo que se va a introducir en el campo de la web
    # descripcion: descripcion de la incidencia
    def create_incident(self, title, description):
        self.page.fill("#title", title)
        self.page.fill("#description", description)
        self.page.click("button[type='submit']")

    # Funcion para evitar condiciones de carrera (intentamos comprobar algo que aun no ha terminado de hacerse)
    # La idea es esperar a un elemento, en este caso, al cuadro de respuesta
    def get_feedback_locator(self):
        return self.page.locator("#feedback")
    
    def get_response_locator(self):
        return self.page.locator("#response")