import json
from datetime import date
from functools import lru_cache
from typing import Any, List
from uuid import UUID

import pandas as pd
import plotly.graph_objs as go
from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.async_sqlmodel import paginate
from sqlmodel import select

from models import ChartTypeEnum, Performance

from .base import BaseService


class PerformanceService(BaseService):
    async def bulk_insert(self, records: List[Performance]) -> None:
        self._database.add_all(records)
        await self._database.commit()

    async def save(self, record: Performance) -> Performance:
        self._database.add(record)
        await self._database.commit()
        await self._database.refresh(record)
        return record

    async def get(self, uid: UUID) -> Performance:
        stmt = select(Performance).where(Performance.uid == uid)
        _result = await self._database.exec(statement=stmt)

        return _result.one()

    async def list(self, params: CursorParams) -> CursorPage[Performance]:
        stmt = select(Performance).order_by(
            Performance.date.desc()
        )
        return await paginate(self._database, stmt, params)

    def to_dataframe(self, start: date, end: date) -> pd.DataFrame:
        stmt = select(Performance).filter(
            Performance.date >= str(start)
        ).filter(Performance.date <= str(end)).order_by(
            Performance.date.desc()
        )
        return pd.read_sql(stmt, con=self._dsn_sync_url)

    async def to_ploty(self, chart_type: ChartTypeEnum, start: date, end: date) -> Any:
        df = self.to_dataframe(start=start, end=end)
        fig = None
        match chart_type:
            case ChartTypeEnum.BAR.value:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df["team"], y=df["review_time"]))
                fig.add_trace(go.Bar(x=df["team"], y=df["merge_time"]))
            case ChartTypeEnum.SCATTER.value:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df["team"], y=df["review_time"], mode="lines+markers"))
                fig.add_trace(go.Scatter(x=df["team"], y=df["merge_time"], mode="lines+markers"))
            case ChartTypeEnum.PIE.value:
                fig = go.Figure(data=[go.Pie(labels=df["team"], values=df["review_time"])])
        return fig

    @lru_cache
    async def summary(self, start: date, end: date) -> Any:
        df = self.to_dataframe(start=start, end=end)

        # Calculate the summary statistics
        summary = {}
        _series = [pd.Series.mean, pd.Series.median, pd.Series.mode, pd.Series.min, pd.Series.max]
        summary = df.groupby("team").agg({"review_time": _series, "merge_time": _series})

        return json.loads(summary.to_json())
