from httpx import AsyncClient
from starlette import status

from core.tests.users.factories import UserDTOCreateFactory


async def test_create_user_fail(http_client: AsyncClient) -> None:
    response = await http_client.post("users/create/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_user_success(http_client: AsyncClient) -> None:
    response = await http_client.post("users/create/", json=UserDTOCreateFactory().model_dump())
    assert response.status_code == status.HTTP_201_CREATED
