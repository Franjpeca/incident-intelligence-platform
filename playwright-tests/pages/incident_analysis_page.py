from .base_page import BasePage


class IncidentAnalysisPage(BasePage):
    # Para movernos a la pagina
    def goto(self):
        super().goto("/pages/incident-analysis.html")
    
    # Rellenar campo de analizar incidencia y mandar a analizar
    def analyze_incident(self, incident_id):
        self.page.fill("#incident-analysis-id", str(incident_id))
        self.page.click("#incident-analysis-form button[type='submit']")
    
    # Obtener incidencia por id
    def get_incident_analysis(self, incident_id):
        self.page.fill("#get-incident-analysis-id", str(incident_id))
        self.page.click("#get-incident-analysis-form button[type='submit']")
    
    # Usar el modelo directamente
    def use_model(self, text, analysis_type=""):
        self.page.fill("#model-text", text)

        analysis_type_input = self.page.locator("#analysis-type")
        analysis_type_input.clear()

        if analysis_type:
            self.page.fill("#analysis-type", analysis_type)

        self.page.click("#use-model-form button[type='submit']")

    # -- Observadores de las diferentes respuestas feedback y response --
    def get_incident_analysis_feedback_locator(self):
        return self.page.locator("#incident-analysis-feedback")

    def get_incident_analysis_response_locator(self):
        return self.page.locator("#incident-analysis-response")

    def get_get_incident_analysis_feedback_locator(self):
        return self.page.locator("#get-incident-analysis-feedback")

    def get_get_incident_analysis_response_locator(self):
        return self.page.locator("#get-incident-analysis-response")

    def get_use_model_feedback_locator(self):
        return self.page.locator("#use-model-feedback")

    def get_use_model_response_locator(self):
        return self.page.locator("#use-model-response")