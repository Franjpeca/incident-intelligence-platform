from pydantic import BaseModel, Field
from app.domain.enums.incident_status import IncidentStatus

class IncidentUpdateRequest(BaseModel):
    # Se permite que sean opcionales, pero minimo debe de haber uno
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, min_length=10, max_length=10000)
    status: IncidentStatus | None = None