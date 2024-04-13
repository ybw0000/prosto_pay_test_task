from enum import Enum

from pydantic_settings import BaseSettings


class Env(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    PREFIX: str = "/api/v1"
    PORT: int = 8000
    DEBUG: bool = True
    ENV: Env = Env.LOCAL
    LOG_LEVEL: LogLevel = LogLevel.INFO


settings = Settings()
