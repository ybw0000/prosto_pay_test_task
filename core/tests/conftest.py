from typing import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient

from core.conf.app import create_app


@pytest_asyncio.fixture(scope="session")
async def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture(scope="function")
async def http_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://test/api/v1/",
    ) as http_client:
        yield http_client
