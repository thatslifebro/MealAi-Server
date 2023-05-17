from fastapi import APIRouter, Response, Cookie

from app.dto.auth.AuthResponse import *
from app.service.auth import AuthService
from app.utils.depends import *

router = APIRouter(
    prefix="/api/auth",
)


@router.post("/login", description="로그인", response_model=LoginResponse, tags=["auth"])
async def login(
    request: LoginRequest, response: Response, redis: Redis = Depends(get_redis)
):
    res = await AuthService().login(login_info=request, redis=redis)
    response.set_cookie(
        key="refresh_token",
        value=res["refresh_token"],
        httponly=False,
        domain="kdt-ai6-team08.elicecoding.com",
    )
    return LoginResponse(access_token=res["access_token"])


@router.post("/logout", description="로그아웃", response_model=str, tags=["auth"])
async def logout(
    request: LogoutRequest = Depends(current_user_token),
    redis: Redis = Depends(get_redis),
):
    await AuthService().logout(user=request, redis=redis)
    return "로그아웃 완료"


@router.get(
    "/refresh", description="토큰 만료시 갱신", response_model=RefreshResponse, tags=["auth"]
)
async def refresh(refresh_token: str = Cookie(None), redis: Redis = Depends(get_redis)):
    return await AuthService().refresh(refresh_token=refresh_token, redis=redis)


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
