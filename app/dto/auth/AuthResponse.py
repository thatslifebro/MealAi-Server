from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Access token")


class EmailResponse(BaseModel):
    authentication_number: int = Field(..., description="인증번호")


class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="Access Token")
