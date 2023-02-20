from typing import Optional
from uuid import UUID

from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi import APIRouter, Depends, HTTPException

from models import Operation
from services import OperationService

router = APIRouter()


@router.get(
    "/operation",
    response_model=CursorPage[Operation],
    summary="List operations",
)
async def list_operation(
    service: OperationService = Depends(),
    params: CursorParams = Depends(),
) -> CursorPage[Operation]:
    return await service.list(params=params)


@router.get("/operation/{uid}", summary="Get operation")
async def get_operation(
    uid: UUID,
    service: OperationService = Depends(),
) -> Optional[Operation]:
    try:
        return await service.get(uid=uid)
    except Exception:
        raise HTTPException(status_code=404, detail="Operation not found")
