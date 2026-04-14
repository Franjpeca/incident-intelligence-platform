from app.application.services.incident_rules_service import analyze_text_with_rules

# Test unitario para comprobar incidencias criticas
# Se busca que la funcion no llame al LLM para incidencias criticas (comportamiento deseado)
def test_rules_return_no_llm_for_critical_incident():
    # Enviamos una incidencia de ejemplo que deberia etiquetarse como critica
    result = analyze_text_with_rules(
        title="Servidor caido en produccion",
        description="El sistema no responde"
    )

    # Comprobamos los valores del resultado con asertos, si hay algo mal, falla el test
    assert result.use_llm is False
    assert result.analysis_type is None
    assert result.priority == "high"

# Test unitario para comprobar incidencias al completo
# Se busca que la funcion llame al LLM y ademas utilice el prompt que analiza al completo
def test_rules_return_full_analysis_for_detailed_incident():
    # Generamos este tipo dde incidencia
    result = analyze_text_with_rules(
        title="Error en API",
        description="Timeout exception al procesar transacciones"
    )

    # Creamos asertos para que le test falle en caso de comportamiento no deseado
    assert result.use_llm is True
    assert result.analysis_type == "full_analysis"
    assert result.priority == "medium"

# Test unitario para comprobar incidencias normales
# Se busca que la funcion llame al LLM y ademas utilice un prompt de analisis mas basico
def test_rules_return_basic_analysis_for_normal_incident():
    # Generamos este tipo de incidencia basica
    result = analyze_text_with_rules(
        title="Consulta usuario",
        description="Cambio de contraseña"
    )

    # Creamos los asertos necesarios, falla el test si no se cumple lo esperado
    assert result.use_llm is True
    assert result.analysis_type == "basic_analysis"
    assert result.priority == "medium"