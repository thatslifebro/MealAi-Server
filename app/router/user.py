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


@router.get("/db", description="모든 유저 DB 조회 연습", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user.get_users(db, skip=skip, limit=limit)
    return users


@router.post("", description="회원가입", response_model=CreateUserResponse, tags=["user"])
async def register(request: CreateUserRequest):
    await UserService().register(request)
    return CreateUserResponse(email=request.email, nickname=request.nickname)


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
