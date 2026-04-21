from .base_page import BasePage


class ViewIncidentPage(BasePage):

    def goto(self):
        super().goto("/pages/view-incident.html")

    # Funcion para buscar una incidencia por ID
    def search_incident_by_id(self, incident_id):
        self.page.fill("#incident-id", str(incident_id))
        self.page.click("#search-btn")

    # Funcion para cargar todas las incidencias
    def load_all_incidents(self):
        self.page.click("#load-btn")

    # Observamos feedback para la busqueda por id
    def get_search_feedback_locator(self):
        return self.page.locator("#search-feedback")

    # Observamos response para la busqueda por id
    def get_search_response_locator(self):
        return self.page.locator("#search-response")

    # Observamos feedback para la busqueda de todas las incidencias
    def get_list_feedback_locator(self):
        return self.page.locator("#list-feedback")

    # Observamos la "response" pero de la lista de incidencias (incidents-list)
    def get_incidents_list_locator(self):
        return self.page.locator("#incidents-list")