import pytest

from app.core.exceptions import PromptNotFoundError, PromptFormattingError
from app.core.prompt_manager import get_prompt_name_for_analysis_type, build_prompt

# Test unitario para comprobar que se obtiene el prompt basico
def test_get_prompt_name_for_basic_analysis():
    result = get_prompt_name_for_analysis_type("basic_analysis")
    assert result == "incident_basic_analysis.txt"

# Test unitario para comprobar que se obtiene el prompt completo
def test_get_prompt_name_for_full_analysis():
    result = get_prompt_name_for_analysis_type("full_analysis")
    assert result == "incident_full_analysis.txt"

# Test unitario para comprobar que se obtiene el prompt basico por de fecto
def test_get_prompt_name_uses_default_when_none():
    result = get_prompt_name_for_analysis_type(None)
    assert result == "incident_basic_analysis.txt"

# Test unitario para comprobar que se obtiene la excepcion correta si el prompt no existe
def test_get_prompt_name_raises_for_unknown_analysis_type():
    # Obtenemos dicha excepcion
    with pytest.raises(PromptNotFoundError):
        get_prompt_name_for_analysis_type("unknown_analysis")

# Test para comprobar que el prompt se construye correctamente
def test_build_prompt_replaces_text_field():
    # Llamos a construir el prompt
    result = build_prompt(
        analysis_type="basic_analysis",
        text="Servidor caido en produccion"
    )

    # Comprobamos que el texto se encuentra en el prompt
    assert "Servidor caido en produccion" in result

# Test unitario para comprobar la falta de parametros al construir el prompt
def test_build_prompt_raises_when_field_is_missing():
    # Se espera capturar un error de formato del prompt
    with pytest.raises(PromptFormattingError):
        build_prompt(
            analysis_type="basic_analysis"
        )