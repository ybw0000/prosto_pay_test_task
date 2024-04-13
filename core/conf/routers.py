from fastapi import FastAPI

from core.base import base_router
from core.conf.settings import settings


def init_routers(app: FastAPI) -> None:
    app.include_router(router=base_router, prefix=settings.PREFIX)
