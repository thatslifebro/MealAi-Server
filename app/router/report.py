from fastapi import APIRouter
from app.service.report import *

router = APIRouter(
    prefix="/api/reports",
)


@router.get(
    "/{week}",
    description="주간 통계",
    # response_model=List[ReportData],
    tags=["report"],
)
def get_report_week(week: int):
    return ReportService().service_get_report_week(week)
