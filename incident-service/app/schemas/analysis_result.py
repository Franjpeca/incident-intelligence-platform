from pydantic import BaseModel, ConfigDict

class IncidentAnalysisResponse(BaseModel):
    summary: str
    category: str
    priority: str
    confidence: int
    
    # Para que Pydantic gestione el objeto al devolverlo
    model_config = ConfigDict(from_attributes=True)