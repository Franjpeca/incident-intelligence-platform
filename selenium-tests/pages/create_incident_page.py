from selenium.webdriver.common.by import By
from .base_page import BasePage

class CreateIncidentPage(BasePage):
    # Direccion de la web a tratar, la que refleja esta clase
    PATH = "/pages/create-incident.html"

    # Localizadores
    # Se indican aqui por si la pagina cambia
    # Es una de las debilidades de selenium, por eso el tenerlas claras a mano para cambiar
    TITLE_INPUT  = (By.ID, "title")
    DESC_INPUT   = (By.ID, "description")
    SUBMIT_BTN   = (By.CSS_SELECTOR, "button[type='submit']")
    FEEDBACK_MSG = (By.ID, "feedback")
    RESPONSE_MSG = (By.ID, "response")
    
    SUCCESS_TEXT = "Incidencia creada correctamente"

    def goto(self):
        # Accedemos al PATH, heredado
        super().goto(self.PATH)

    # Creacion de la incidencia en la web
    def create_incident(self, title, description):
        # Esto pasa (By.ID, "title") como dos argumentos separados a self.fill
        # Es una caracteristica de python, de las tuplas
        self.fill(*self.TITLE_INPUT, title)
        self.fill(*self.DESC_INPUT, description)
        self.click(*self.SUBMIT_BTN)

    # Observador del elemento feedback
    def get_feedback_text(self):
        return self.get_text(*self.FEEDBACK_MSG)
    
    # Observaodr del elemento response
    def get_response_text(self):
        return self.get_text(*self.RESPONSE_MSG)

    # Espera a obtener la respuesta
    def wait_for_success_feedback(self):
        # Reutilizamos el localizador y el texto esperado
        self.wait_for_text(*self.FEEDBACK_MSG, self.SUCCESS_TEXT)