from pydantic import BaseModel
from app.domain.enums.incident_status import IncidentStatus

class IncidentUpdateRequest(BaseModel):
    title: str
    description: str
    status: IncidentStatus