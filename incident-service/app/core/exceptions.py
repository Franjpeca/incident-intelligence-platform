# Base comun para tratar las excepciones propias
class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# Incidencia no encontrado
class IncidentNotFoundError(AppError):
    pass

# Errores de los campos en los datos
class FieldError(AppError):
    pass

# Error en la regla
class BusinessRuleError(AppError):
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

