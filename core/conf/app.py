import logging

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from core import __version__
from core.base.models import metadata
from core.conf.db import async_session
from core.conf.exception_handlers import init_exception_handlers
from core.conf.middlewares import init_middlewares
from core.conf.routers import init_routers
from core.conf.settings import settings
from core.conf.settings import Settings

logger = logging.getLogger(__name__)


def init_db(app_settings: Settings):
    """Init database"""
    engine = create_async_engine(app_settings.sqlalchemy_database_uri)
    async_session.configure(bind=engine)
    metadata.bind = engine


def create_app(app_settings: Settings | None = None) -> "FastAPI":
    """Create app with including configurations"""
    app_settings = app_settings if app_settings is not None else settings
    init_db(app_settings)
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
    init_exception_handlers(app)
    return app
