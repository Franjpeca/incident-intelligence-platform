import logging
import logging.config
from pathlib import Path
import os

def setup_logging(service_name: str = "app-service"):
    LOG_DIR = Path("logs")
    LOG_DIR.mkdir(exist_ok=True)

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                # Añadimos el service_name al formato para identificarlo en Docker
                "format": f"%(asctime)s | %(levelname)s | {service_name} | %(name)s | %(message)s"
            },
            "detailed": {
                "format": f"%(asctime)s | %(levelname)s | {service_name} | %(name)s | %(filename)s:%(lineno)d | %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": os.getenv("LOG_LEVEL", "INFO"), # Dinamico
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler", # Mejor que FileHandler (rota archivos)
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": str(LOG_DIR / f"{service_name}.log"),
                "maxBytes": 10485760, # 10MB y crea uno nuevo
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    })
    
    return logging.getLogger(service_name)