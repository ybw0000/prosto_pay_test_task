from fastapi import FastAPI

from core.base import base_router
from core.conf.settings import settings
from core.users import users_router


def init_routers(app: FastAPI) -> None:
    app.include_router(router=base_router, prefix=settings.PREFIX, tags=["Base"])
    app.include_router(router=users_router, prefix=settings.PREFIX, tags=["Users"])
