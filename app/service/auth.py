from app.dao.user import *
import bcrypt, jwt
from app.dao.user import *
from app.dto.auth.AuthRequest import *
from app.dto.auth.AuthResponse import *
from starlette.config import Config

config = Config(".env")
ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET")
ALGORITHM = config("ALGORITHM")


class AuthService:
    def __init__(self):
        pass

    async def login(self, login_info: LoginRequest):
        email, password = login_info.email, login_info.password
        user = await read_by_email(email=email)

        if not user:
            raise ValueError("email이 존재하지 않습니다.")

        if not bcrypt.checkpw(password.encode("utf-8"), user.password):
            raise ValueError("현재 비밀번호가 일치하지 않습니다.")

        return LoginResponse(
            access_token=self.create_access_token(user.user_id),
            refresh_token=self.create_refresh_token(),
        )

    def create_access_token(self, user_id: int):
        payload = {"user_id": user_id}
        access_token = jwt.encode(payload, ACCESS_TOKEN_SECRET, ALGORITHM)
        return access_token

    def create_refresh_token(self):
        payload = {}
        refresh_token = jwt.encode(payload, ACCESS_TOKEN_SECRET, ALGORITHM)
        return refresh_token
