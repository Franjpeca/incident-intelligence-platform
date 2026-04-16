from .base_page import BasePage


class UpdateDeleteIncidentPage(BasePage):
    # Navegador hacia la pagina
    def goto(self):
        super().goto("/pages/update-delete-incident.html")

    # Funcion para actualizar una incidencia al completo
    def update_incident(self, incident_id, title="", description="", status=""):
        self.page.fill("#update-id", str(incident_id))

        self.page.locator("#update-title").clear()
        if title:
            self.page.fill("#update-title", title)

        self.page.locator("#update-description").clear()
        if description:
            self.page.fill("#update-description", description)

        if status:
            self.page.select_option("#update-status", status)

        self.page.click("#update-form button[type='submit']")

    # Funcion para actualizar el status de una incidencia
    def update_status_only(self, incident_id, status):
        self.page.fill("#status-id", str(incident_id))
        self.page.select_option("#status-only", status)
        self.page.click("#status-form button[type='submit']")

    # Funcion para eliminar una incidencia
    def delete_incident(self, incident_id):
        self.page.fill("#delete-id", str(incident_id))
        self.page.click("#delete-form button[type='submit']")

    # -- Observadores de feedback y locator para cada funcionalidad --
    def get_update_feedback_locator(self):
        return self.page.locator("#update-feedback")

    def get_update_response_locator(self):
        return self.page.locator("#update-response")

    def get_status_feedback_locator(self):
        return self.page.locator("#status-feedback")

    def get_status_response_locator(self):
        return self.page.locator("#status-response")

    def get_delete_feedback_locator(self):
        return self.page.locator("#delete-feedback")

    def get_delete_response_locator(self):
        return self.page.locator("#delete-response")