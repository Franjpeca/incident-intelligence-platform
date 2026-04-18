from selenium.webdriver.common.by import By
from .base_page import BasePage


class ViewIncidentPage(BasePage):
    # Direccion de la web a tratar, la que refleja esta clase
    PATH = "/pages/view-incident.html"

    # Localizadores
    SEARCH_ID_INPUT = (By.ID, "incident-id")
    SEARCH_BTN = (By.ID, "search-btn")
    SEARCH_FEEDBACK_MSG = (By.ID, "search-feedback")
    SEARCH_RESPONSE_MSG = (By.ID, "search-response")

    LOAD_BTN = (By.ID, "load-btn")
    LIST_FEEDBACK_MSG = (By.ID, "list-feedback")
    INCIDENTS_LIST = (By.ID, "incidents-list")

    SEARCH_SUCCESS_TEXT = "Incidencia encontrada"
    LIST_SUCCESS_TEXT = "Incidencias cargadas"

    def goto(self):
        # Accedemos al PATH, heredado
        super().goto(self.PATH)

    # Busqueda de una incidencia por su id
    def search_incident_by_id(self, incident_id):
        self.fill(*self.SEARCH_ID_INPUT, str(incident_id))
        self.click(*self.SEARCH_BTN)

    # Carga de todas las incidencias
    def load_all_incidents(self):
        self.click(*self.LOAD_BTN)

    # Observador del elemento feedback de busqueda
    def get_search_feedback_text(self):
        return self.get_text(*self.SEARCH_FEEDBACK_MSG)

    # Observador del elemento response de busqueda
    def get_search_response_text(self):
        return self.get_text(*self.SEARCH_RESPONSE_MSG)

    # Observador del elemento feedback de listado
    def get_list_feedback_text(self):
        return self.get_text(*self.LIST_FEEDBACK_MSG)

    # Observador del elemento que contiene la lista
    def get_incidents_list_text(self):
        return self.get_text(*self.INCIDENTS_LIST)

    # Espera a obtener la respuesta correcta al buscar por id
    def wait_for_search_success_feedback(self):
        self.wait_for_text(*self.SEARCH_FEEDBACK_MSG, self.SEARCH_SUCCESS_TEXT)

    # Espera a obtener la respuesta correcta al listar incidencias
    def wait_for_list_success_feedback(self):
        self.wait_for_text(*self.LIST_FEEDBACK_MSG, self.LIST_SUCCESS_TEXT)