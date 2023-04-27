from app.dto.user.UserRequest import *
from app.dto.user.UserResponse import *
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
)


@router.post("", description="회원가입", response_model=CreateUserResponse, tags=["user"])
async def register(request: CreateUserRequest):
    pass


@router.get(
    "", description="회원정보 조회", response_model=GetUserInfoResponse, tags=["user"]
)
async def get_user_info(user_id: CurrentUserId):
    pass


@router.patch(
    "", description="회원정보 수정", response_model=EditUserInfoResponse, tags=["user"]
)
async def edit_user_info(request: EditUserInfoRequest, user_id: CurrentUserId):
    pass


@router.patch(
    "/change_password", description="비밀번호 변경", response_model=None, tags=["user"]
)
async def change_password(request: ChangePasswordRequest, user_id: CurrentUserId):
    pass


@router.post(
    "/check_password", description="현재 비밀번호 확인", response_model=None, tags=["user"]
)
async def check_password(request: CheckPasswordRequest):
    pass


@router.delete("", description="회원 탈퇴", response_model=None, tags=["user"])
async def delete_user(user_id: CurrentUserId):
    pass
