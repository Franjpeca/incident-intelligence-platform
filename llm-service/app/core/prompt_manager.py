from app.core.config import PROMPTS_DIR

# Funcion para cargar un prompt desde un archivo
def load_prompt(prompt_name: str) -> str:
    path = PROMPTS_DIR / prompt_name

    if not path.exists():
        raise FileNotFoundError(f"Prompt no encontrado: {path}")

    return path.read_text(encoding="utf-8")


# Funcion para construir un prompt a partir de una plantilla y argumentos
def build_prompt(prompt_name: str, **kwargs: str) -> str:
    template = load_prompt(prompt_name)

    try:
        return template.format(**kwargs)
    except KeyError as exc:
        raise ValueError(f"Elemento faltante: {exc.args[0]}") from exc