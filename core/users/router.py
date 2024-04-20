import logging
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from core.users.dependencies import get_user_service
from core.users.schemas import UserDTOCreateSchema
from core.users.schemas import UserDTOReadSchema
from core.users.service import UserService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.get(
    "/<int:pk>/",
    responses={
        status.HTTP_200_OK: {"model": UserDTOReadSchema},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
)
async def get_user(
    pk: int,
    service: Annotated[UserService, Depends(get_user_service)],
):
    user = await service.get_user_by_pk(pk)
    return UserDTOReadSchema.model_validate(user)


@router.post(
    "/create/",
    response_model=UserDTOReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request_data: UserDTOCreateSchema,
    service: Annotated[UserService, Depends(get_user_service)],
):
    user = await service.create_user(request_data)
    return UserDTOReadSchema.model_validate(user)
