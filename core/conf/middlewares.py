import logging
import uuid

import orjson
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from core.conf.schemas import RequestLogSchema
from core.conf.schemas import ResponseLogSchema

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def unpack_body(body: bytes) -> dict:
        try:
            return orjson.loads(body)
        except orjson.JSONDecodeError:
            return {}

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)

            # Log incoming request
            request_id = uuid.uuid4()
            body = self.unpack_body(await request.body())
            logger.info(
                RequestLogSchema(
                    url=request.url, headers=request.headers, request_id=request_id, body=body
                ).model_dump()
            )

            response_schema = ResponseLogSchema(
                url=request.url,
                request_id=request_id,
            )

            async def custom_send(message: dict):
                if message["type"] == "http.response.start":
                    response_schema.headers = message.get("headers")
                    response_schema.status_code = message.get("status")
                if message["type"] == "http.response.body":
                    response_schema.body = self.unpack_body(message.get("body", b""))

                await send(message)

            await self.app(scope, receive, custom_send)
            logger.info(response_schema.model_dump())
        else:
            await self.app(scope, receive, send)


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
    )
    app.add_middleware(
        LoggingMiddleware,
    )
