from pydantic import BaseModel
from app.domain.enums.incident_status import IncidentStatus

class IncidentUpdateRequest(BaseModel):
    # Se permite que sean opcionales, pero minimo debe de haber uno
    title: str | None = None
    description: str | None = None
    status: IncidentStatus | None = None