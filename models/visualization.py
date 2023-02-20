from typing import Any, Dict

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Column, Field, JSON, SQLModel


class VisualizationBase(SQLModel):
    name: str = Field(...)
    data: Dict[Any, Any] = Field(sa_column=Column(JSON))
    type: str = Field(max_length=255)


class Visualization(VisualizationBase, table=True):
    uid: Optional[UUID] = Field(default=None, primary_key=True)
