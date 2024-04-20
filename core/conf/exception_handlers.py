from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exception_handlers import http_exception_handler
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from core.conf.exceptions import DoesNotExistException


async def does_not_exist_exception_handler(request: Request, exc: DoesNotExistException) -> Response:
    return await http_exception_handler(
        request=request, exc=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(DoesNotExistException)(does_not_exist_exception_handler)
