import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.core.config import DO_SAMPLE, MAX_NEW_TOKENS, PROMPT_BASIC_FILE, TEMPERATURE, TOP_P, MODEL_ID
from app.core.model_loader import load_model
from app.core.output_parser import extract_json
from app.core.prompt_manager import build_prompt
from app.schemas.analysis_response import AnalysisResponse



# Funcion principal del servicios de analisis
# Recibe el texto del cliente a analizar
# Devuelve un objeto con el resumen, categoria, prioridad y confianza
def analyze_text(text: str) -> AnalysisResponse:
    # Cargamos el modelo y el tokenizer
    # El modelo se carga una sola vez y se reutiliza en cada llamada a la función
    _tokenizer, _model = load_model()

    # Construimos el prompt con el texto del cliente y nuestra plantilla
    prompt = build_prompt(
        prompt_name=PROMPT_BASIC_FILE,
        text=text
    )

    # Necesario para indicar al modelo quienes somos y poder darle una entrada
    messages = [
        {"role": "user", "content": prompt}
    ]

    # Modificamos nuestro texto + plantilla para agregar campos necesarios para la entrada
    # Son etiquetas especiales necesitadas por el modelo
    input_text = _tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Transformamos este texto a tokens que entendera el modelo y los movemos a memoria
    # Es cargar la entrada
    inputs = _tokenizer(input_text, return_tensors="pt").to(_model.device)

    # Generamos la respuesta del modelo
    # Aqui se introducen al modelo la entrada que ya ha sido cargada y se pide generar una respuesta
    # Se le indican parametros del mismo, como la temperatura
    outputs = _model.generate(
        **inputs,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        do_sample=DO_SAMPLE
    )

    # La respuesta viene mezclada con la entrada, por lo que hay que separar la parte de la respuesta que nos interesa
    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    # Proceso inverso, pasamos de token a texto legible
    output_text = _tokenizer.decode(generated_ids, skip_special_tokens=True)

    # Extraemos el JSON de la respuesta del modelo y lo parseamos a un diccionario
    parsed = extract_json(output_text)

    # Devolvemos la respuesta con el formato esperado
    return AnalysisResponse(
        summary=str(parsed["summary"]),
        category=str(parsed["category"]),
        priority=str(parsed["priority"]),
        confidence=int(parsed["confidence"])
    )