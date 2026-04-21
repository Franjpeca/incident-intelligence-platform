from selenium.webdriver.common.by import By
from .base_page import BasePage

class CreateIncidentPage(BasePage):
    # Direccion de la web a tratar, la que refleja esta clase
    PATH = "/pages/create-incident.html"

    # Localizadores
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
        self.fill(*self.TITLE_INPUT, title)
        self.fill(*self.DESC_INPUT, description)
        self.click(*self.SUBMIT_BTN)

    # Observador del elemento feedback
    def get_feedback_text(self):
        return self.get_text(*self.FEEDBACK_MSG)
    
    # Observador del elemento response
    def get_response_text(self):
        return self.get_text(*self.RESPONSE_MSG)

    # Espera a obtener la respuesta
    def wait_for_success_feedback(self):
        # Reutilizamos el localizador y el texto esperado
        self.wait_for_text(*self.FEEDBACK_MSG, self.SUCCESS_TEXT)