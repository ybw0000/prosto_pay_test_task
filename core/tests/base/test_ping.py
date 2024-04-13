import pytest
from starlette import status

from core.base.schemas import PingResponseSchema


@pytest.mark.asyncio
async def test_ping(http_client) -> None:
    response = await http_client.get("ping")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == PingResponseSchema(OK=True).model_dump()
