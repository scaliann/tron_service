import asyncio
import time
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine, async_sessionmaker
from core.config import settings
from sqlalchemy.orm import sessionmaker
from asyncio import current_task


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )


    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper = DatabaseHelper(url=settings.db.url, echo=settings.db.echo)
