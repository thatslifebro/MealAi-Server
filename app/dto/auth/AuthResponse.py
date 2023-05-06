from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")


class EmailResponse(BaseModel):
    authentication_number: int = Field(..., description="인증번호")
