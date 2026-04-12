# Base comun para tratar las excepciones propias
class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# No hace falta cuerpo en las clases, solamente sirven para identificar el tipo de error y 
# manejarlo de forma adecuada en los controladores

# Icidente no encontrado
class IncidentNotFoundError(AppError):
    pass

# Analisis no existente
class AnalysisNotFoundError(AppError):
    pass

# Fallo al conectar con el servicio de LLM
class LLMServiceUnavailableError(AppError):
    pass

# Respuesta del LLM incorrecta
class InvalidLLMResponseError(AppError):
    pass

# Fallo en la base de datos
class DatabaseOperationError(AppError):
    pass