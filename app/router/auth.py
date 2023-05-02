from fastapi import APIRouter
from app.dto.auth.AuthRequest import *
from app.dto.auth.AuthResponse import *

router = APIRouter(
    prefix="/api",
)


@router.post("/login", description="로그인", response_model=LoginResponse, tags=["auth"])
async def login(request: LoginRequest):
    pass


@router.delete("/logout", description="로그아웃", response_model=None, tags=["auth"])
async def logout():
    pass


@router.post("/refresh", description="토큰 만료시 갱신", response_model=None, tags=["auth"])
async def refresh():
    pass
