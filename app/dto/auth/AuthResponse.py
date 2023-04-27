from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    token: str = Field(..., description="token")
    refresh_token: str = Field(..., description="Refresh token")
