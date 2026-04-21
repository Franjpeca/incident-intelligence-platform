from app.core.config import PROMPTS_DIR, ANALYSIS_TYPE_TO_PROMPT, DEFAULT_ANALYSIS_TYPE
from app.core.exceptions import (
    PromptNotFoundError,
    PromptFormattingError,
)

import logging

logger = logging.getLogger(__name__)

# Funcion para cargar un prompt desde un archivo
def load_prompt(prompt_name: str) -> str:
    logger.info(f"Cargando el prompt: {prompt_name}")
    path = PROMPTS_DIR / prompt_name

    if not path.exists():
        logger.error(f"Plantilla no encontrada: {path}")
        raise PromptNotFoundError(f"Plantilla no encontrada: {path}")
    
    logger.info("Prompt encontrado, se devuelve")
    return path.read_text(encoding="utf-8")


def get_prompt_name_for_analysis_type(analysis_type: str | None) -> str:
    logger.info("Obteniendo el nombre del prompt")

    analysis_type_var = analysis_type or DEFAULT_ANALYSIS_TYPE

    # Obtenemos el nombre del fichero del prompt a partir del diccionario del fichero de configuracion
    prompt_name = ANALYSIS_TYPE_TO_PROMPT.get(analysis_type_var)

    if prompt_name is None:
        logger.info("No hay prompt configurado")
        raise PromptNotFoundError(f"No hay prompt configurado para el tipo de analisis: {analysis_type_var}")

    logger.info("Devolviendo el nombre del prompt")
    return prompt_name


# Funcion para construir un prompt a partir de una plantilla y argumentos
def build_prompt(analysis_type: str | None, **kwargs: str) -> str:
    logger.info("Construyendo el prompt")

    prompt_name = get_prompt_name_for_analysis_type(analysis_type)

    template = load_prompt(prompt_name)
    try:
        logger.info("Devolviendo el prompt")
        return template.format(**kwargs)
    except KeyError as exc:
        logger.error("Error al cargar el prompt, error en los campos")
        raise PromptFormattingError(f"Campo faltante: {exc.args[0]}") from exc
    


def get_input_text(tokenizer, analysis_type: str | None, text: str) -> str:

    logger.info(f"Construyendo el prompt del modelo con text: {text} y tipo de analisis: {analysis_type}")
    prompt = build_prompt(
        analysis_type=analysis_type,
        text=text
    )

    # Necesario para indicar identidad al mensaje y el contenido
    messages = [
        {"role": "user", "content": prompt}
    ]

    try:

        logger.info("Aplicando etiquetas al prompt del modelo")
        input_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    except Exception as exc:
            logger.error(f"Error al aplicar chat_template: {exc}")
            raise PromptFormattingError(f"Error al preparar el formato del LLM: {exc}") from exc

    return input_text