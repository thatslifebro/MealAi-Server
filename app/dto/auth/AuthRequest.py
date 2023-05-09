from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., title="사용자 Email")
    password: str = Field(..., title="사용자 비밀번호")


class EmailRequest(BaseModel):
    email: EmailStr = Field(..., title="사용자 Email")


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., title="refresh Token")


class LogoutRequest(BaseModel):
    refresh_token: str = Field(..., title="refresh Token")
