from fastapi import APIRouter, UploadFile

from app.dto.report.ReportResponse import *
from app.service.report import *
from app.utils.depends import *

from app.utils.upload_image import *

router = APIRouter(
    prefix="/api/reports",
)


@router.post(
    "/image",
    description="이미지 업로드하기",
    tags=["report"],
)
def post_image(file: UploadFile):
    contents = file.file.read()
    file.file.seek(0)
    return upload_file(file, 1)


@router.get(
    "/image",
    description="이미지 다운로드",
    tags=["report"],
)
def get_image():
    get_file()


@router.get(
    "/{week}",
    description="주간 통계",
    response_model=ReportResponse,
    tags=["report"],
)
async def get_report_week(week: int, user_id: int = Depends(current_user_id)):
    return await ReportService().service_get_report_week(week, user_id)
