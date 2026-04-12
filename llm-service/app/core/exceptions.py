class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# Modelo no cargado
class ModelNotLoadedError(AppError):
    pass

# Error al cargar el modelo
class ModelLoadError(AppError):
    pass

# Prompt no encontrado
class PromptNotFoundError(AppError):
    pass

# Error durante la inferencia del modelo (uso del modelo)
class ModelInferenceError(AppError):
    pass

# Salida del modelo invalida o inesperada
class InvalidModelOutputError(AppError):
    pass

# Error al formatear el prompt o respuesta
class PromptFormattingError(AppError):
    pass