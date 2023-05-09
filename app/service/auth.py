from app.error.user import *
import bcrypt, jwt
from app.dao.user import *
from app.dto.auth.AuthRequest import *
from app.dto.auth.AuthResponse import *
from starlette.config import Config
from datetime import datetime, timedelta
import time
import smtplib, ssl
import random
from email.message import EmailMessage
from app.utils.hash_password import hash_password
from app.dao.auth import *
from jwt.exceptions import *
from app.error.auth import *


config = Config(".env")

ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = config("REFRESH_TOKEN_SECRET")
ALGORITHM = config("ALGORITHM")
SMTP_SERVER = config("SMTP_SERVER")
SMTP_SSL_PORT = config("SMTP_SSL_PORT")
SENDER_EMAIL = config("SENDER_EMAIL")
SENDER_PASSWORD = config("SENDER_PASSWORD")


class AuthService:
    def __init__(self):
        pass

    async def login(self, login_info: LoginRequest):
        email, password = login_info.email, login_info.password
        user = await read_by_email(email=email)

        if not user:
            raise NotFoundUserException
        if user.is_deleted:
            raise DeletedEmailException
        if not bcrypt.checkpw(password.encode("utf-8"), user.password):
            raise NotMatchPasswordException

        access_token = self.create_access_token(user.user_id)
        refresh_token = self.create_refresh_token(user.user_id)

        await upsert_refresh_token(user.user_id, refresh_token)
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def logout(self, user: LogoutRequest, redis):
        await delete_refresh_token(user_id=user.user_id)
        redis.sadd("blacklist", user.access_token)
        return None

    def create_access_token(self, user_id: int):
        minutes = 30
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=minutes),
        }
        access_token = jwt.encode(
            payload,
            ACCESS_TOKEN_SECRET,
            ALGORITHM,
        )
        return access_token

    def create_refresh_token(self, user_id: int):
        minutes = 60 * 24 * 30
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=minutes),
        }
        refresh_token = jwt.encode(payload, REFRESH_TOKEN_SECRET, ALGORITHM)
        return refresh_token

    async def send_mail_for_register(self, receiver_email: str):
        user = await read_by_email(receiver_email)

        if user:
            raise DuplicatedEmailException

        msg = EmailMessage()
        msg["Subject"] = "MealAi 회원가입 이메일 인증"
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        auth_num = str(random.randint(100000, 999999))

        msg.set_content(f"회원가입을 위한 이메일 인증번호는 {auth_num}입니다.")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return auth_num

    async def send_mail_for_reset_pw(self, receiver_email: str):
        user = await read_by_email(receiver_email)

        if not user:
            raise NotFoundUserException
        if user.is_deleted:
            raise DeletedEmailException

        auth_num = str(random.randint(100000, 999999))
        changed_password = hash_password(auth_num)
        await update_password(password=changed_password, user_id=user.user_id)

        msg = EmailMessage()
        msg["Subject"] = "MealAi 로그인 임시 비밀번호 발급"
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        msg.set_content(
            f"MealAi 로그인 임시 비밀번호 발급 \n 임시 비밀번호는 {auth_num}입니다. \n 개인 정보 보호를 위해 비밀번호를 꼭 변경해 주세요."
        )

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return None

    async def refresh(self, refresh_token: RefreshRequest):
        refresh_token = refresh_token.refresh_token
        try:
            payload = jwt.decode(
                jwt=refresh_token, key=REFRESH_TOKEN_SECRET, algorithms=ALGORITHM
            )
            user_id = payload.get("user_id")
            db_refresh_token = await read_refresh_token_by_user_id(user_id=user_id)
            if refresh_token != db_refresh_token.refresh_token:
                raise NotFoundUserException

            access_token = self.create_access_token(user_id=user_id)
            refresh_token = self.create_refresh_token(user_id=user_id)

            await upsert_refresh_token(user_id, refresh_token=refresh_token)

            return RefreshResponse(
                access_token=access_token,
                refresh_token=refresh_token,
            )
        except ExpiredSignatureError:
            raise ExpiredAccessTokenException
        except InvalidSignatureError:
            raise InvalidTokenException
