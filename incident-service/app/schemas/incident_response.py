# Importacion para el estandar actual de pydantic
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from pydantic import BaseModel
# Esquema de la respuesta que se devolvera al cleinte tras una llamada

# Pydantic se encarga de validar los datos
# None permite indicar que no es un campo obligatorio
# Esto debe de ser coherente con lo que tenemos en el modelo de SQLAlchemy
class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str | None
    category: str | None
    analysis_summary: str | None
    analysis_confidence: int | None
    created_at: datetime
    updated_at: datetime

    # Con esto lee como un objeto de la base de datos y con sus restricciones, gracias a SQLAlchemy
    model_config = ConfigDict(from_attributes=True)