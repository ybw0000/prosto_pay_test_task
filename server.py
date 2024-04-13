import uvicorn

from core.conf.app import create_app
from core.conf.logging import LOG_CONFIG
from core.conf.settings import settings

# from g50_api.conf.logging import LOG_CONFIG

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.value.lower(),
        log_config=LOG_CONFIG,
        loop="uvloop",
    )
