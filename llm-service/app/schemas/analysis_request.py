from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    text: str
    analysis_type: str  # Por ejemplo, "sentiment", "entities", etc.