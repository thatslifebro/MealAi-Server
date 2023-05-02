from typing import List

from sqlalchemy.orm import Session
from app.dao import user
from app.database import schemas
from app.database.database import SessionLocal
from app.dto.user.UserRequest import *
from app.dto.user.UserResponse import *
from fastapi import APIRouter, Depends
from app.service.user import UserService

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
async def get_user_info():
    user = await UserService().get_user_info(user_id=1)
    return GetUserInfoResponse(**user)


@router.patch(
    "", description="회원정보 수정", response_model=EditUserInfoResponse, tags=["user"]
)
async def edit_user_info(request: EditUserInfoRequest, user_id: CurrentUserId):
    await UserService().edit_user_info(update=request, user_id=1)
    res = request.dict()
    return EditUserInfoResponse(**res)


@router.patch(
    "/change_password", description="비밀번호 변경", response_model=str, tags=["user"]
)
async def change_password(request: ChangePasswordRequest, user_id: CurrentUserId):
    await UserService().change_password(update=request, user_id=1)
    return "변경완료"


@router.post(
    "/check_password", description="현재 비밀번호 확인", response_model=str, tags=["user"]
)
async def check_password(request: CheckPasswordRequest, user_id: CurrentUserId):
    await UserService().check_password(password=request, user_id=1)
    return "확인완료"


@router.delete("", description="회원 탈퇴", response_model=str, tags=["user"])
async def delete_user(user_id: CurrentUserId):
    await UserService().delete_user(user_id=10)
    return "탈퇴완료"
