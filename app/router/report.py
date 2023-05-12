from fastapi import APIRouter, UploadFile

from app.dto.report.ReportResponse import *
from app.service.report import *
from app.utils.depends import *

from app.utils.upload_image import *

router = APIRouter(
    prefix="/api/reports",
)


@router.get(
    "/history/{week}",
    description="주간 통계",
    response_model=ReportHistoryResponse,
    tags=["report"],
)
async def get_report_week(week: int, user_id: int = Depends(current_user_id)):
    return await ReportService().service_get_report_history(week, user_id)


@router.get(
    "/report/{week}",
    description="주간 통계",
    response_model=ReportResponse,
    tags=["report"],
)
async def get_report_week(week: int, user_id: int = Depends(current_user_id)):
    return await ReportService().service_get_report_week(week, user_id)
