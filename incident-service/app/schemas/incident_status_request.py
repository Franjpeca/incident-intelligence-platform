from pydantic import BaseModel
from app.domain.enums.incident_status import IncidentStatus

class StatusUpdateRequest(BaseModel):
    status: IncidentStatus