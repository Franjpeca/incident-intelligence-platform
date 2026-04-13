import logging
import logging.config
from pathlib import Path
import os

# Usamos una variable para el nombre del servicio, así el archivo es reutilizable
def setup_logging(service_name: str = "llm-service"):
    LOG_DIR = Path("logs")
    LOG_DIR.mkdir(exist_ok=True)

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                # Añadimos el service_name al string para identificarlo en la consola unificada de Docker
                "format": f"%(asctime)s | %(levelname)s | {service_name} | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": f"%(asctime)s | %(levelname)s | {service_name} | %(name)s | %(filename)s:%(lineno)d | %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
                "stream": "ext://sys.stdout", # Forzamos salida estándar para Docker
            },
            "file": {
                # Cambiamos a RotatingFileHandler: evita que el log llene el disco del servidor
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": str(LOG_DIR / f"{service_name}.log"),
                "maxBytes": 10485760, # 10MB
                "backupCount": 3,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": "INFO", # INFO en root evita que librerías externas saturen la consola
            "handlers": ["console", "file"],
        },
    })