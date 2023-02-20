from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from dependencies import get_async_session
from settings import Settings, get_settings


class BaseService:
    def __init__(
        self,
        database: AsyncSession = Depends(get_async_session),
        settings: Settings = Depends(get_settings),
    ) -> None:
        self._database = database
        self._dsn_sync_url = settings.dsn_sync_url
