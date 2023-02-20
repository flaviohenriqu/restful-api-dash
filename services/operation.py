from uuid import UUID

from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.async_sqlmodel import paginate
from sqlmodel import select

from models import Operation

from .base import BaseService


class OperationService(BaseService):
    async def save(self, record: Operation) -> Operation:
        self._database.add(record)
        await self._database.commit()
        await self._database.refresh(record)
        return record

    async def get(self, uid: UUID) -> Operation:
        stmt = select(Operation).where(Operation.uid == uid)
        _result = await self._database.exec(statement=stmt)

        return _result.one()

    async def list(self, params: CursorParams) -> CursorPage[Operation]:
        stmt = select(Operation).order_by(
            Operation.created.desc()
        )
        return await paginate(self._database, stmt, params)
