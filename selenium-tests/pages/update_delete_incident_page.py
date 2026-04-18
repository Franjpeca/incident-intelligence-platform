from selenium.webdriver.common.by import By
from .base_page import BasePage


class UpdateDeleteIncidentPage(BasePage):
    # Direccion de la web a tratar, la que refleja esta clase
    PATH = "/pages/update-delete-incident.html"

    # Localizadores de actualizacion general
    UPDATE_ID_INPUT = (By.ID, "update-id")
    UPDATE_TITLE_INPUT = (By.ID, "update-title")
    UPDATE_DESC_INPUT = (By.ID, "update-description")
    UPDATE_STATUS_SELECT = (By.ID, "update-status")
    UPDATE_SUBMIT_BTN = (By.CSS_SELECTOR, "#update-form button[type='submit']")
    UPDATE_FEEDBACK_MSG = (By.ID, "update-feedback")
    UPDATE_RESPONSE_MSG = (By.ID, "update-response")

    # Localizadores de actualizacion de estado
    STATUS_ID_INPUT = (By.ID, "status-id")
    STATUS_ONLY_SELECT = (By.ID, "status-only")
    STATUS_SUBMIT_BTN = (By.CSS_SELECTOR, "#status-form button[type='submit']")
    STATUS_FEEDBACK_MSG = (By.ID, "status-feedback")
    STATUS_RESPONSE_MSG = (By.ID, "status-response")

    # Localizadores de borrado
    DELETE_ID_INPUT = (By.ID, "delete-id")
    DELETE_SUBMIT_BTN = (By.CSS_SELECTOR, "#delete-form button[type='submit']")
    DELETE_FEEDBACK_MSG = (By.ID, "delete-feedback")
    DELETE_RESPONSE_MSG = (By.ID, "delete-response")

    UPDATE_SUCCESS_TEXT = "Incidencia actualizada correctamente"
    STATUS_SUCCESS_TEXT = "Estado actualizado correctamente"
    DELETE_SUCCESS_TEXT = "Incidencia borrada correctamente"

    def goto(self):
        # Accedemos al PATH, heredado
        super().goto(self.PATH)

    # Actualizacion general de una incidencia
    def update_incident(self, incident_id, title="", description="", status=""):
        self.fill(*self.UPDATE_ID_INPUT, str(incident_id))
        self.fill(*self.UPDATE_TITLE_INPUT, title)
        self.fill(*self.UPDATE_DESC_INPUT, description)

        if status:
            self.find(*self.UPDATE_STATUS_SELECT).send_keys(status)

        self.click(*self.UPDATE_SUBMIT_BTN)

    # Actualizacion del estado de una incidencia
    def update_status_only(self, incident_id, status):
        self.fill(*self.STATUS_ID_INPUT, str(incident_id))
        self.find(*self.STATUS_ONLY_SELECT).send_keys(status)
        self.click(*self.STATUS_SUBMIT_BTN)

    # Borrado de una incidencia
    def delete_incident(self, incident_id):
        self.fill(*self.DELETE_ID_INPUT, str(incident_id))
        self.click(*self.DELETE_SUBMIT_BTN)

    # Observadores de actualizacion general
    def get_update_feedback_text(self):
        return self.get_text(*self.UPDATE_FEEDBACK_MSG)

    def get_update_response_text(self):
        return self.get_text(*self.UPDATE_RESPONSE_MSG)

    # Observadores de actualizacion de estado
    def get_status_feedback_text(self):
        return self.get_text(*self.STATUS_FEEDBACK_MSG)

    def get_status_response_text(self):
        return self.get_text(*self.STATUS_RESPONSE_MSG)

    # Observadores de borrado
    def get_delete_feedback_text(self):
        return self.get_text(*self.DELETE_FEEDBACK_MSG)

    def get_delete_response_text(self):
        return self.get_text(*self.DELETE_RESPONSE_MSG)

    # Esperas de exito
    def wait_for_update_success_feedback(self):
        self.wait_for_text(*self.UPDATE_FEEDBACK_MSG, self.UPDATE_SUCCESS_TEXT)

    def wait_for_status_success_feedback(self):
        self.wait_for_text(*self.STATUS_FEEDBACK_MSG, self.STATUS_SUCCESS_TEXT)

    def wait_for_delete_success_feedback(self):
        self.wait_for_text(*self.DELETE_FEEDBACK_MSG, self.DELETE_SUCCESS_TEXT)