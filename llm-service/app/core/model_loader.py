# Importamos las librerias necesarias para cargar el modelo y tokenizer de Hugging Face
from transformers import AutoModelForCausalLM, AutoTokenizer
 # Nombre del modelo a cargar
from app.core.config import MODEL_ID

# Variables que almacenaran el modelo y tokenizer cargados
# Se busca evitar cargarlo cada vez que se haga una peticion
_tokenizer = None
_model = None

def load_model():
    global _tokenizer, _model
    # Tomamos las variables gloables, y si no esta cargado el modelo y tokenizer, los cargamos
    print("[DEBUG] ID del modelo a cargar:", MODEL_ID)
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    if _model is None:
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="auto"  # Indicamos que se cargue en GPU, si no se puede, se cargara en CPU
        )

    return _tokenizer, _model




def is_model_loaded(): # Funcion para verificar si el modelo y tokenizer estan cargados, para el health check
    return _tokenizer is not None and _model is not None