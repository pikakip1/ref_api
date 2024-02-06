import uuid
from asyncio import current_task
from datetime import datetime

import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import (async_scoped_session, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class AsyncDatabaseManager:
    async_engine = create_async_engine(
        url=settings.database_url_asyncpg,
        echo=True,
    )
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.async_session_factory,
            scopefunc=current_task,
        )
        return session

    async def scoped_session_dependency(self):
        async_session = self.get_scoped_session()
        yield async_session
        await async_session.close()


async_db_manager = AsyncDatabaseManager()


class Base(DeclarativeBase):
    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
