from selenium.webdriver.common.by import By
from .base_page import BasePage


class IncidentAnalysisPage(BasePage):
    # Direccion de la web a tratar, la que refleja esta clase
    PATH = "/pages/incident-analysis.html"

    # Localizadores de analisis de incidencia
    INCIDENT_ANALYSIS_ID_INPUT = (By.ID, "incident-analysis-id")
    INCIDENT_ANALYSIS_SUBMIT_BTN = (By.CSS_SELECTOR, "#incident-analysis-form button[type='submit']")
    INCIDENT_ANALYSIS_FEEDBACK_MSG = (By.ID, "incident-analysis-feedback")
    INCIDENT_ANALYSIS_RESPONSE_MSG = (By.ID, "incident-analysis-response")

    # Localizadores de obtener analisis
    GET_INCIDENT_ANALYSIS_ID_INPUT = (By.ID, "get-incident-analysis-id")
    GET_INCIDENT_ANALYSIS_SUBMIT_BTN = (By.CSS_SELECTOR, "#get-incident-analysis-form button[type='submit']")
    GET_INCIDENT_ANALYSIS_FEEDBACK_MSG = (By.ID, "get-incident-analysis-feedback")
    GET_INCIDENT_ANALYSIS_RESPONSE_MSG = (By.ID, "get-incident-analysis-response")

    # Localizadores de uso directo del modelo
    MODEL_TEXT_INPUT = (By.ID, "model-text")
    ANALYSIS_TYPE_INPUT = (By.ID, "analysis-type")
    USE_MODEL_SUBMIT_BTN = (By.CSS_SELECTOR, "#use-model-form button[type='submit']")
    USE_MODEL_FEEDBACK_MSG = (By.ID, "use-model-feedback")
    USE_MODEL_RESPONSE_MSG = (By.ID, "use-model-response")

    INCIDENT_ANALYSIS_SUCCESS_TEXT = "Analisis lanzado correctamente"
    GET_INCIDENT_ANALYSIS_SUCCESS_TEXT = "Analisis obtenido correctamente"
    USE_MODEL_SUCCESS_TEXT = "Texto analizado correctamente"

    def goto(self):
        # Accedemos al PATH, heredado
        super().goto(self.PATH)

    # Lanza el analisis de una incidencia
    def analyze_incident(self, incident_id):
        self.fill(*self.INCIDENT_ANALYSIS_ID_INPUT, str(incident_id))
        self.click(*self.INCIDENT_ANALYSIS_SUBMIT_BTN)

    # Obtiene el analisis ya generado de una incidencia
    def get_incident_analysis(self, incident_id):
        self.fill(*self.GET_INCIDENT_ANALYSIS_ID_INPUT, str(incident_id))
        self.click(*self.GET_INCIDENT_ANALYSIS_SUBMIT_BTN)

    # Usa el modelo directamente con un texto
    def use_model(self, text, analysis_type=""):
        self.fill(*self.MODEL_TEXT_INPUT, text)
        self.fill(*self.ANALYSIS_TYPE_INPUT, analysis_type)
        self.click(*self.USE_MODEL_SUBMIT_BTN)

    # Observadores del analisis de incidencia
    def get_incident_analysis_feedback_text(self):
        return self.get_text(*self.INCIDENT_ANALYSIS_FEEDBACK_MSG)

    def get_incident_analysis_response_text(self):
        return self.get_text(*self.INCIDENT_ANALYSIS_RESPONSE_MSG)

    # Observadores de obtener analisis
    def get_get_incident_analysis_feedback_text(self):
        return self.get_text(*self.GET_INCIDENT_ANALYSIS_FEEDBACK_MSG)

    def get_get_incident_analysis_response_text(self):
        return self.get_text(*self.GET_INCIDENT_ANALYSIS_RESPONSE_MSG)

    # Observadores del uso directo del modelo
    def get_use_model_feedback_text(self):
        return self.get_text(*self.USE_MODEL_FEEDBACK_MSG)

    def get_use_model_response_text(self):
        return self.get_text(*self.USE_MODEL_RESPONSE_MSG)

    # Esperas de exito
    def wait_for_incident_analysis_success_feedback(self):
        self.wait_for_text(
            *self.INCIDENT_ANALYSIS_FEEDBACK_MSG, 
            self.INCIDENT_ANALYSIS_SUCCESS_TEXT, 
            custom_timeout=60
        )

    def wait_for_get_incident_analysis_success_feedback(self):
        self.wait_for_text(
            *self.GET_INCIDENT_ANALYSIS_FEEDBACK_MSG, 
            self.GET_INCIDENT_ANALYSIS_SUCCESS_TEXT, 
            custom_timeout=60
        )

    def wait_for_use_model_success_feedback(self):
        self.wait_for_text(
            *self.USE_MODEL_FEEDBACK_MSG, 
            self.USE_MODEL_SUCCESS_TEXT, 
            custom_timeout=60
        )