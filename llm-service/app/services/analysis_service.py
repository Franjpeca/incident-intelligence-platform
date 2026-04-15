import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.core.config import DO_SAMPLE, MAX_NEW_TOKENS, TEMPERATURE, TOP_P
from app.core.model_loader import load_model
from app.core.output_parser import extract_json
from app.core.prompt_manager import build_prompt
from app.schemas.analysis_response import AnalysisResponse
# Importaciones de excepciones propias
from app.core.exceptions import ModelInferenceError, InvalidModelOutputError

import logging

logger = logging.getLogger(__name__)

# Funcion principal del servicios de analisis
# Recibe el texto del cliente a analizar
# Devuelve un objeto con el resumen, categoria, prioridad y confianza
def analyze_text(text: str, analysis_type: str = None) -> AnalysisResponse:
    logging.info("Iniciando analisis de texto usando LLM")
    # Cargamos el modelo y el tokenizer
    # El modelo se carga una sola vez y se reutiliza en cada llamada a la función
    logging.info("Cargando el modelo LLM")
    _tokenizer, _model = load_model()

    # Construimos el prompt con el texto del cliente y nuestra plantilla
    logging.info(f"Construyendo el prompt del modelo con text: {text} y tipo de analisis: {analysis_type}")
    prompt = build_prompt(
        analysis_type=analysis_type,
        text=text
    )

    # Necesario para indicar al modelo quienes somos y poder darle una entrada
    messages = [
        {"role": "user", "content": prompt}
    ]

    # Modificamos nuestro texto + plantilla para agregar campos necesarios para la entrada
    # Son etiquetas especiales necesitadas por el modelo
    logging.info("Aplicando etiquetas al prompt del modelo")
    input_text = _tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Transformamos este texto a tokens que entendera el modelo y los movemos a memoria
    # Es cargar la entrada
    try:
        logging.info("Tokenizando el input del modelo")
        inputs = _tokenizer(input_text, return_tensors="pt").to(_model.device)
    except Exception as exc:
        logging.error("Error al tokenizar el modelo")
        raise ModelInferenceError("Error al preparar el input del modelo") from exc

    # Generamos la respuesta del modelo
    # Aqui se introducen al modelo la entrada que ya ha sido cargada y se pide generar una respuesta
    # Se le indican parametros del mismo, como la temperatura
    try:
        logging.info("Generando la salida del modelo, iniciando inferencia")
        outputs = _model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=DO_SAMPLE
        )
    except Exception as exc:
        logging.warning("Error realizar la inferencia del modelo")
        raise ModelInferenceError("Error durante la inferencia del modelo") from exc
    # La respuesta viene mezclada con la entrada, por lo que hay que separar la parte de la respuesta que nos interesa
    logging.info("Obteniendo la salida del modelo")
    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    # Proceso inverso, pasamos de token a texto legible
    try:
        logging.info("Decodificando la salida del modelo a texto legible")
        output_text = _tokenizer.decode(generated_ids, skip_special_tokens=True)
    except Exception as exc:
        logging.error("Error el pasar de token a texto legible")
        raise ModelInferenceError("Error al decodificar la salida del modelo") from exc
    # Extraemos el JSON de la respuesta del modelo y lo parseamos a un diccionario
    logging.info("Extrayendo el JSON de la respuesta del modelo")
    parsed = extract_json(output_text)

    # Intentamos crear el objeto AnalysisResponse directamente
    # Pydantic se encargara de comprobar si faltan campos o si los tipos estan mal.
    # Esto permite que sea escalable, sin tener que especificar en esta parte del codigo campos fijos
    try:
        logging.info("Devolviendo la respuesta del modelo")
        return AnalysisResponse(**parsed) 
    except Exception as exc:
        logging.error("Error al devolver al respuesta del modelo, faltan campos o hay tipos incorrectos")
        raise InvalidModelOutputError(f"La salida del modelo no es valida: {str(exc)}")