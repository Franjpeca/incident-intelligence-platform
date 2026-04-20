from app.schemas.analysis_result import AnalysisResult

class IncidentRulesResult(AnalysisResult):
    use_llm: bool
    analysis_type: str | None = None
    # Necesario para que hayan parametros opcionales que decidira el modelo en tal caso
    summary: str | None = None
    category: str | None = None