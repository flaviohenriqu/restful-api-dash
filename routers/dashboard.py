import json
from typing import Any, Optional
from uuid import UUID, uuid4

from fastapi import (APIRouter, BackgroundTasks, Body, Depends, HTTPException,
                     Query, UploadFile)
from fastapi.responses import JSONResponse

from models import ChartTypeEnum, DateRange, Operation, Visualization
from services import OperationService, PerformanceService, VisualizationService
from tasks import upload_file

router = APIRouter()


@router.post("/upload", summary="Upload")
async def upload(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    operation_service: OperationService = Depends(),
) -> Any:
    operation = await operation_service.save(
        Operation(uid=uuid4(), input_ref=file.filename),
    )
    background_tasks.add_task(
        upload_file.process,
        file,
        operation_service,
        operation,
    )
    return {"message": f"starting processing file: {operation.uid}"}


@router.post("/summary")
async def generate_summary(
    date_range: DateRange = Depends(),
    performance_service: PerformanceService = Depends(),
):
    return await performance_service.summary(date_range.start, date_range.end)


@router.post("/visualizations")
async def generate_visualization(
    date_range: DateRange = Depends(),
    visualization_service: VisualizationService = Depends(),
    performance_service: PerformanceService = Depends(),
    chart_type: ChartTypeEnum = Body(...),
    chart_name: Optional[str] = Body(...),
):
    fig = await performance_service.to_ploty(
        chart_type=chart_type, start=date_range.start, end=date_range.end
    )
    if fig is None:
        return JSONResponse(content={"error": "Invalid chart type"}, status_code=400)

    # Save the visualization to the database
    data = json.loads(fig.to_json())
    uid = uuid4()
    visualization = await visualization_service.save(
        Visualization(uid=uid, name=chart_name or f"{str(uid)}", type=chart_type, data=data)
    )
    return {**{"uid": visualization.uid}, **data}


@router.get(
    "/visualizations/{visualization_id}",
    response_model=Optional[Visualization]
)
async def get_visualization(
    visualization_id: UUID,
    visualization_service: VisualizationService = Depends(),
) -> Optional[Visualization]:
    try:
        return await visualization_service.get(uid=visualization_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Visualization not found")
