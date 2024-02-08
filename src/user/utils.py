from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_db_manager
from src.user.models import User


async def get_user_db(session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
    yield SQLAlchemyUserDatabase(session, User)
