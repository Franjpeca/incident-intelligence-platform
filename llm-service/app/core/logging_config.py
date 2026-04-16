import logging
import logging.config
from pathlib import Path
import os

def setup_logging(service_name: str = "llm-service"):
    default_log_dir = Path(__file__).resolve().parent / "logs"
    env_log_path = os.getenv("LOG_DIR_PATH")

    if env_log_path:
        LOG_DIR = Path(env_log_path)
    else:
        LOG_DIR = default_log_dir

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file_path = LOG_DIR / f"{service_name}.log"

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
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
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": str(log_file_path),
                "maxBytes": 10485760,
                "backupCount": 3,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    })
    
    return logging.getLogger(service_name)