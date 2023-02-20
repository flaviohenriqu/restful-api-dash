import enum
from datetime import date as _date
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import root_validator
from sqlmodel import Field, SQLModel


class ChartTypeEnum(str, enum.Enum):
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"


class DateRange(SQLModel):
    start: _date
    end: Optional[_date] = _date.today()

    @root_validator
    def validate(cls, values):
        if values["start"] > _date.today():
            raise ValueError("Start date invalid")
        if values["start"] > values.get("end"):
            raise ValueError("start date cannot be greater than end date")
        return values


class PerformanceBase(SQLModel):
    review_time: int = Field(...)
    merge_time: int = Field(...)
    date: _date = Field(default=datetime.utcnow().date())
    team: str = Field(max_length=255)


class Performance(PerformanceBase, table=True):
    uid: Optional[UUID] = Field(default=None, primary_key=True)
