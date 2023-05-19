import random
from datetime import datetime, timedelta

import bcrypt
import jwt
from jwt.exceptions import *
from starlette.config import Config

from app.dao.user import *
from app.dto.auth.AuthRequest import *
from app.dto.auth.AuthResponse import *
from app.error.auth import *
from app.error.user import *
from app.service.user import check_user
from app.utils.hash_password import hash_password
from app.utils.send_mail import send_mail

config = Config(".env")

ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = config("REFRESH_TOKEN_SECRET")
ACCESS_TOKEN_EXPIRES_MINUTES = int(config("ACCESS_TOKEN_EXPIRES_MINUTES"))
REFRESH_TOKEN_EXPIRES_DAY = int(config("REFRESH_TOKEN_EXPIRES_DAY"))
REFRESH_TOKEN_EXPIRES_DAY_REDIS = int(config("REFRESH_TOKEN_EXPIRES_DAY_REDIS"))
ALGORITHM = config("ALGORITHM")


class AuthService:
    def __init__(self):
        pass

    async def login(self, login_info: LoginRequest, redis):
        email, password = login_info.email, login_info.password
        user = await read_by_email(email=email)
        check_user(user)

        if not bcrypt.checkpw(password.encode("utf-8"), user.password):
            raise NotMatchPasswordException

        access_token = create_access_token(user.user_id)
        refresh_token = create_refresh_token(user.user_id)

        pre_refresh_token = redis.get(user.user_id)
        if pre_refresh_token:
            redis.sadd("blacklist", pre_refresh_token.decode())

        redis.set(
            name=str(user.user_id),
            value=refresh_token,
            ex=REFRESH_TOKEN_EXPIRES_DAY_REDIS,
        )

        res = dict({"access_token": access_token, "refresh_token": refresh_token})
        return res

    async def logout(self, user: LogoutRequest, refresh_token: str, redis):
        redis.sadd("blacklist", user.access_token)
        redis.sadd("blacklist", refresh_token)
        return None

    async def send_mail_for_register(self, receiver_email: str):
        user = await read_by_email(receiver_email)

        if user:
            raise DuplicatedEmailException

        auth_num = make_randint_string(6)

        send_mail("register", receiver_email, auth_num)

        return auth_num

    async def send_mail_for_reset_pw(self, receiver_email: str):
        user = await read_by_email(receiver_email)

        check_user(user)

        auth_num = make_randint_string(8)
        changed_password = hash_password(auth_num)

        await update_password(password=changed_password, user_id=user.user_id)

        send_mail("find", receiver_email, auth_num)

        return None

    async def refresh(self, refresh_token: str, redis):
        try:
            payload = jwt.decode(
                jwt=refresh_token, key=REFRESH_TOKEN_SECRET, algorithms=ALGORITHM
            )
            user_id = payload.get("user_id")

            db_refresh_token = redis.get(str(user_id)).decode()

            if refresh_token != db_refresh_token:
                raise NotMatchRefreshTokenException

            access_token = create_access_token(user_id=user_id)

            return RefreshResponse(access_token=access_token)
        except ExpiredSignatureError:
            raise ExpiredAccessTokenException
        except (InvalidSignatureError, DecodeError):
            raise InvalidTokenException


def make_randint_string(length: int):
    return str(random.randint(10 ** (length - 1), 10**length - 1))


def create_access_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES),
    }
    access_token = jwt.encode(
        payload,
        ACCESS_TOKEN_SECRET,
        ALGORITHM,
    )
    return access_token


def create_refresh_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRES_DAY),
    }
    refresh_token = jwt.encode(payload, REFRESH_TOKEN_SECRET, ALGORITHM)
    return refresh_token
