import pytest
from httpx import AsyncClient
from starlette import status

from core.base.schemas import PingResponseSchema


@pytest.mark.asyncio
async def test_ping(http_client: AsyncClient) -> None:
    response = await http_client.get("base/ping")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == PingResponseSchema(OK=True).model_dump()
