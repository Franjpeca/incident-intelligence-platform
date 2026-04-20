# Field nos permite indicar restricciones
from pydantic import BaseModel, Field
# Esquema del objeto que envia el usuario
class IncidentCreateRequest(BaseModel):
    title: str = Field(
        ...,    # "..." en Field indica que el parametro es obligatorio
        min_length=3, 
        max_length=100
    )
    description: str = Field(
        ...,
        min_length=10, 
        max_length=10000
    )