import logging

from fastapi import APIRouter
from starlette import status

from core.base.schemas import PingResponseSchema

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/ping", responses={status.HTTP_200_OK: {"model": PingResponseSchema}})
async def ping() -> PingResponseSchema:
    return PingResponseSchema(OK=True)
