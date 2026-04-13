from enum import Enum

# Enum para representar estado posibles
# Se encuentra aqui ya que es parte del dominio
# Esta en la capa de negocio
class IncidentStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"