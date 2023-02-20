import logging
from uuid import uuid4

import pandas as pd
from fastapi import UploadFile

from models import Operation, OperationStatusEnum
from services import OperationService

logger = logging.getLogger(__name__)


async def process(
    file: UploadFile,
    operation_service: OperationService,
    operation: Operation,
    chunksize: int = 200,
) -> None:
    logger.info("Starting processing")
    operation.status = OperationStatusEnum.IN_PROGRESS
    operation = await operation_service.save(operation)

    try:
        df = pd.read_csv(file.file)
        logger.info(f"dataframe size: {df.size}")
        df['uid'] = [uuid4() for _ in range(len(df.index))]
        file.file.close()
        df.to_sql(
            "performance",
            con=operation_service._dsn_sync_url,
            if_exists="replace",
            chunksize=chunksize
        )
        operation.status = OperationStatusEnum.COMPLETED
    except Exception as exc:
        logger.exception(exc)
        operation.status = OperationStatusEnum.CANCELLED
    finally:
        await operation_service.save(operation)
        logger.info(f"total data processed: {df.size}")
