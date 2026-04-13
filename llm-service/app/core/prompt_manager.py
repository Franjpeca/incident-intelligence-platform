from app.core.config import PROMPTS_DIR, ANALYSIS_TYPE_TO_PROMPT, DEFAULT_ANALYSIS_TYPE
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


def get_prompt_name_for_analysis_type(analysis_type: str | None) -> str:
    # Logica para seleccionar el prompt indicado o uno por defecto en caso de que no haya
    analysis_type_var = analysis_type or DEFAULT_ANALYSIS_TYPE
    # Ahora obtenemos el nombre del fichero del prompt a partir del diccionario del fichero de configuracion
    prompt_name = ANALYSIS_TYPE_TO_PROMPT.get(analysis_type_var)

    if prompt_name is None:
        raise PromptNotFoundError(f"No hay prompt configurado para el tipo de analisis: {analysis_type_var}")
    # Lo devolvemos
    return prompt_name


# Funcion para construir un prompt a partir de una plantilla y argumentos
# En **kwargs se pasan una lista de campos (en nuestro caso 1) y su valores
# Estos campos se buscaran en el fichero de la plantilla y, para esos campos encontrados
# se reemplazaran por los valores pasados en **kwargs.
# Eg: Si en la plantilla pone {text} y en **kwargs se pasa text="Hola", entonces se reemplazara {text} por "Hola"
# Esto lo realiza la funcion .format
def build_prompt(analysis_type: str | None, **kwargs: str) -> str:
    # Buscamos el prompt usando el tipo de analis
    prompt_name = get_prompt_name_for_analysis_type(analysis_type)
    # Una vez encontrado, lo cargamos
    template = load_prompt(prompt_name)
    try:
        return template.format(**kwargs) # Se reemplaza en la plantilla los campos por su valor
    except KeyError as exc:
        raise PromptFormattingError(f"Campo faltante: {exc.args[0]}") from exc