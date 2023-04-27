from app.dto.user.UserRequest import (
    CreateUserRequest,
    EditUserInfoRequest,
    CurrentUserId,
    ChangePasswordRequest,
    CheckPasswordRequest,
)
from app.dto.user.UserResponse import (
    CreateUserResponse,
    GetUserInfoResponse,
    EditUserInfoResponse,
)
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
)


@router.post(
    "",
    description="회원가입",
    response_model=CreateUserResponse,
)
async def register(request: CreateUserRequest):
    pass


@router.get("", description="회원정보 조회", response_model=GetUserInfoResponse)
async def get_user_info(user_id: CurrentUserId):
    pass


@router.patch("", description="회원정보 수정", response_model=EditUserInfoResponse)
async def edit_user_info(request: EditUserInfoRequest, user_id: CurrentUserId):
    pass


@router.patch("/change_password", description="비밀번호 변경", response_model=None)
async def change_password(request: ChangePasswordRequest, user_id: CurrentUserId):
    pass


@router.post("/check_password", description="현재 비밀번호 확인", response_model=None)
async def check_password(user_id: CurrentUserId):
    pass


@router.delete("", description="회원 탈퇴", response_model=None)
async def delete_user(user_id: CurrentUserId):
    pass
