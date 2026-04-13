from pydantic import BaseModel

class IncidentRulesResult(BaseModel):
    use_llm: bool
    analysis_type: str | None = None
    summary: str | None = None
    category: str | None = None
    priority: str | None = None
    confidence: int | None = None