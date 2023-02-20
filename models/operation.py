import enum
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Column, Enum, Field, SQLModel


class OperationStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class OperationBase(SQLModel):
    input_ref: Optional[str] = Field(max_length=255)
    created: datetime = Field(default=datetime.utcnow())
    status: OperationStatusEnum = Field(
        sa_column=Column(Enum(OperationStatusEnum)),
        default=OperationStatusEnum.PENDING,
    )


class Operation(OperationBase, table=True):
    uid: Optional[UUID] = Field(default=None, primary_key=True)
