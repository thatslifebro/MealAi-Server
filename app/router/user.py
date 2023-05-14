from fastapi import APIRouter

from app.database.database import SessionLocal
from app.dto.user.UserRequest import *
from app.dto.user.UserResponse import *
from app.service.user import UserService
from app.utils.depends import *

router = APIRouter(
    prefix="/api/users",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    description="회원가입",
    response_model=CreateUserResponse,
    tags=["user"],
    status_code=201,
)
async def register(request: CreateUserRequest):
    await UserService().register(user=request)
    return CreateUserResponse(email=request.email, nickname=request.nickname)


@router.get(
    "", description="회원정보 조회", response_model=GetUserInfoResponse, tags=["user"]
)
async def get_user_info(user_id: int = Depends(current_user_id)):
    res = await UserService().get_user_info(user_id=user_id)
    res = res._asdict()
    return GetUserInfoResponse(**res)


@router.patch(
    "", description="회원정보 수정", response_model=EditUserInfoResponse, tags=["user"]
)
async def edit_user_info(
    request: EditUserInfoRequest, user_id: int = Depends(current_user_id)
):
    await UserService().edit_user_info(update=request, user_id=user_id)
    res = request.dict()
    return EditUserInfoResponse(**res)


@router.patch(
    "/change_password", description="비밀번호 변경", response_model=str, tags=["user"]
)
async def change_password(
    request: ChangePasswordRequest, user_id: int = Depends(current_user_id)
):
    await UserService().change_password(update=request, user_id=user_id)
    return "변경완료"


@router.post(
    "/check_password", description="현재 비밀번호 확인", response_model=str, tags=["user"]
)
async def check_password(
    request: CheckPasswordRequest, user_id: int = Depends(current_user_id)
):
    await UserService().check_password(password=request.password, user_id=user_id)
    return "확인완료"


@router.delete("", description="회원 탈퇴", response_model=str, tags=["user"])
async def delete_user(user_id: int = Depends(current_user_id)):
    await UserService().delete_user(user_id=user_id)
    return "탈퇴완료"
