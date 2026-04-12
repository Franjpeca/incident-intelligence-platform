from app.core.config import PROMPTS_DIR
from app.core.exceptions import (
    PromptNotFoundError,
    PromptFormattingError,
)

# Funcion para cargar un prompt desde un archivo
def load_prompt(prompt_name: str) -> str:
    path = PROMPTS_DIR / prompt_name

    # Lanzamos error si el fichero a encontrar no existe
    if not path.exists():
        raise PromptNotFoundError(f"Plantilla no encontrada: {path}")

    return path.read_text(encoding="utf-8")


# Funcion para construir un prompt a partir de una plantilla y argumentos
# En **kwargs se pasan una lista de campos (en nuestro caso 1) y su valores
# Estos campos se buscaran en el fichero de la plantilla y, para esos campos encontrados
# se reemplazaran por los valores pasados en **kwargs.
# Eg: Si en la plantilla pone {text} y en **kwargs se pasa text="Hola", entonces se reemplazara {text} por "Hola"
# Esto lo realiza la funcion .format
def build_prompt(prompt_name: str, **kwargs: str) -> str:
    template = load_prompt(prompt_name)

    try:
        return template.format(**kwargs) # Se reemplaza en la plantilla los campos por su valor
    except KeyError as exc:
        raise PromptFormattingError(f"Campo faltante: {exc.args[0]}") from exc