from copy import deepcopy

from pythonjsonlogger import jsonlogger

from core.conf.settings import Env
from core.conf.settings import settings


class BaseJsonFormatter(jsonlogger.JsonFormatter):

    def add_fields(self, log_record, record, message_dict):
        super(BaseJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        if isinstance(record.msg, dict):
            log_record["json"] = deepcopy(record.msg.get("json"))
            log_record["text"] = deepcopy(record.msg.get("text"))


log_level = settings.LOG_LEVEL.value

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": BaseJsonFormatter,
        },
        "uvicorn_json": {
            "()": BaseJsonFormatter,
        },
        "local": {
            "()": "logging.Formatter",
        },
    },
    "handlers": {
        "default": {
            "formatter": "local" if settings.ENV == Env.LOCAL else "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "gunicorn_uvicorn": {
            "formatter": "local" if settings.ENV == Env.LOCAL else "uvicorn_json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "dramatiq": {"handlers": ["default"], "level": log_level},
        "uvicorn": {"handlers": [], "level": log_level},
        "gunicorn": {"handlers": ["gunicorn_uvicorn"], "level": log_level},
        "gunicorn.access": {"handlers": ["gunicorn_uvicorn"], "level": log_level},
        "gunicorn.error": {"handlers": ["gunicorn_uvicorn"], "level": log_level},
    },
    "root": {"handlers": ["default"], "level": log_level},
}
