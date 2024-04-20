from core.base.service import BaseService
from core.conf.exceptions import DoesNotExistException
from core.users.models import User
from core.users.schemas import UserDTOCreateSchema


class UserService(BaseService):
    MODEL = User

    async def get_user_by_pk(self, pk: int) -> User | None:
        """Get user by his primary key."""
        filters = (self.MODEL.id == pk,)
        user = await self.fetch_one(filters)
        if not user:
            raise DoesNotExistException("User with pk: %s not found" % pk)
        return user

    async def create_user(self, request_data: UserDTOCreateSchema) -> User:
        """Create a new user."""
        user = await self.insert(request_data.get_data_to_create())
        return user
