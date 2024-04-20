from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.base.dependencies import get_db_session
from core.users.service import UserService


async def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserService:
    """Dependency to get UserService instance"""
    return UserService(session)
