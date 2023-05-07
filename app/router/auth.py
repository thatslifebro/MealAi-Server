from fastapi import APIRouter
from app.dto.auth.AuthRequest import *
from app.dto.auth.AuthResponse import *
from app.service.auth import AuthService

router = APIRouter(
    prefix="/api/auth",
)


@router.post("/login", description="로그인", response_model=LoginResponse, tags=["auth"])
async def login(request: LoginRequest):
    return await AuthService().login(login_info=request)


@router.delete("/logout", description="로그아웃", response_model=None, tags=["auth"])
async def logout():
    pass


@router.post(
    "/refresh", description="토큰 만료시 갱신", response_model=RefreshResponse, tags=["auth"]
)
async def refresh(request: RefreshRequest):
    return await AuthService().refresh(refresh_token=request)


@router.post(
    "/check_email",
    description="회원가입 시 이메일 인증",
    response_model=EmailResponse,
    tags=["auth"],
)
async def check_email(email: EmailRequest):
    res = await AuthService().send_mail_for_register(receiver_email=email.email)
    return EmailResponse(authentication_number=res)


@router.post(
    "/reset_password", description="임시 비밀번호 발급", response_model=str, tags=["auth"]
)
async def reset_password(email: EmailRequest):
    res = await AuthService().send_mail_for_reset_pw(receiver_email=email.email)
    return "임시 비밀번호 발급 완료"
