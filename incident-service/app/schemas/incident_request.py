from pydantic import BaseModel
# Esquema del objeto que envia el usuario
class IncidentCreateRequest(BaseModel):
    title: str
    description: str