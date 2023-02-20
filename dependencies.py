from typing import AsyncGenerator

from fastapi import Depends

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings, get_settings


async def get_async_session(
    settings: Settings = Depends(get_settings)
) -> AsyncGenerator[AsyncSession, None]:
    database_url = settings.dsn_url
    engine = create_async_engine(database_url, echo=True, future=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
