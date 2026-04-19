import logging
import logging.config
from pathlib import Path
import os

def setup_logging(service_name: str = "incident-service"):
    default_log_dir = Path(__file__).resolve().parent / "logs"
    env_log_path = os.getenv("LOG_DIR_PATH")
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # Seleccion del directorio
    if env_log_path:
        LOG_DIR = Path(env_log_path)
    else:
        LOG_DIR = default_log_dir

    # Se crea el directorio en la ruta indicada creando carpetas padre si faltan, si existe, no se crea y continua
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    # Se indica el fichero log
    log_file_path = LOG_DIR / f"{service_name}.log"

    # Configuracion del logger
    logging.config.dictConfig({
        "version": 1,  # Version del esquema python para el logging
        "disable_existing_loggers": False,  # Que no desactive otros loggers si los hay
        "formatters": {
            "standard": {   # Indicamos el formato estandar de logging
                "format": f"%(asctime)s | %(levelname)s | {service_name} | %(name)s | %(message)s"
            },
            "detailed": {   # Indicamos el formato avanzado de logging
                "format": f"%(asctime)s | %(levelname)s | {service_name} | %(name)s | %(filename)s:%(lineno)d | %(message)s"
            },
        },
        "handlers": {       # Manejador para llevar mensajes a donde corresponda
            "console": {    # Para escribir en el terminal se usa la class indicada
                "class": "logging.StreamHandler",
                "level": log_level,    # Obtenemos la variable de entorno para saber el nivel de logging
                "formatter": "standard",    # Formato simple (el de arriba)
                "stream": "ext://sys.stdout",   # Lo enviamos a la salida estandar del sistema, es decir, terminal
            },
            "file": {       # Ahora el mensaje se mandara a un fichero para persistencia
                "class": "logging.handlers.RotatingFileHandler", # Clase para poder escribir en un fichero
                "level": "DEBUG",   # Nivel de logging, es el nivel a partir del cual se realiza esta escritura
                "formatter": "detailed",    # Formatos, nombre de fichero, etc
                "filename": str(log_file_path),
                "maxBytes": 100000000,
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        "root": {   # Primer filtro, espera minimo nivel INFO, si es DEBUG no pasa  
            "level": log_level,    
            "handlers": ["console", "file"],
        },
    })
    
    # Se devuelve un objeto logg para poder ser usado en el programa
    return logging.getLogger(service_name)