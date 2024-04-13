import logging

from fastapi import FastAPI

from core import __version__
from core.conf.middlewares import init_middlewares
from core.conf.routers import init_routers
from core.conf.settings import settings
from core.conf.settings import Settings

logger = logging.getLogger(__name__)


def create_app(app_settings: Settings | None = None) -> "FastAPI":
    """Create app with including configurations"""
    app_settings = app_settings if app_settings is not None else settings
    app = FastAPI(
        title="ProstoPay test task",
        debug=app_settings.DEBUG,
        docs_url=settings.PREFIX + "/docs",
        redoc_url=settings.PREFIX + "/redoc",
        openapi_url=f"{settings.PREFIX}/openapi.json",
        version=__version__,
    )
    init_middlewares(app)
    init_routers(app)
    return app
