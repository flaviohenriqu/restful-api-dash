from typing import Any
from uuid import UUID

from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.async_sqlmodel import paginate
from sqlmodel import select

from models import Visualization

from .base import BaseService


class VisualizationService(BaseService):
    async def save(self, record: Visualization) -> Visualization:
        self._database.add(record)
        await self._database.commit()
        await self._database.refresh(record)
        return record

    async def get(self, uid: UUID) -> Visualization:
        stmt = select(Visualization).where(Visualization.uid == uid)
        _result = await self._database.exec(statement=stmt)

        return _result.one()

    async def list(self, params: CursorParams) -> CursorPage[Visualization]:
        stmt = select(Visualization).order_by(
            Visualization.created.desc()
        )
        return await paginate(self._database, stmt, params)
