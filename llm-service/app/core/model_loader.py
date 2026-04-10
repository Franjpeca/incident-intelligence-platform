# Importamos las librerias necesarias para cargar el modelo y tokenizer de Hugging Face
from transformers import AutoModelForCausalLM, AutoTokenizer
 # Nombre del modelo a cargar
from app.core.config import MODEL_ID

# Variables que almacenaran el modelo y tokenizer cargados
# Se busca evitar cargarlo cada vez que se haga una peticion
tokenizer = None
model = None

def load_model():
    global tokenizer, model
    # Tomamos las variables gloables, y si no esta cargado el modelo y tokenizer, los cargamos
    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="auto" # Indicamos que se cargue en GPU, si no se puede, se cargara en CPU
        )

    return tokenizer, model

def is_model_loaded(): # Funcion para verificar si el modelo y tokenizer estan cargados, para el health check
    return tokenizer is not None and model is not None