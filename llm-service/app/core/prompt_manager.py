from app.core.config import PROMPTS_DIR


def load_prompt(prompt_name: str) -> str:
    path = PROMPTS_DIR / prompt_name

    if not path.exists():
        raise FileNotFoundError(f"Prompt no encontrado: {path}")

    return path.read_text(encoding="utf-8")



def build_prompt(prompt_name: str, **kwargs: str) -> str:
    template = load_prompt(prompt_name)

    try:
        return template.format(**kwargs)
    except KeyError as exc:
        raise ValueError(f"Elemento faltante: {exc.args[0]}") from exc