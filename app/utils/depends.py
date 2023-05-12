from fastapi import Depends, Header, HTTPException
from typing import Optional
import jwt
from jwt.exceptions import *
from starlette.config import Config
from app.error.auth import *
from app.dto.auth.AuthRequest import *
from app.database.token import Redis, get_redis

config = Config(".env")

ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET")
ALGORITHM = config("ALGORITHM")


async def current_user_id(
    authorization_: Optional[str] = Header(None), redis: Redis = Depends(get_redis)
) -> int:
    if not authorization_:
        raise NotFoundAuthorizedHeaderException

    if not authorization_.startswith("Bearer "):
        raise NoTypeBearerException

    token_type, token = authorization_.split()

    is_blacklist_token(token, redis)

    payload = jwt_verify(token)

    user_id = payload.get("user_id")

    return user_id


async def current_user_token(
    authorization_: Optional[str] = Header(None), redis: Redis = Depends(get_redis)
) -> LogoutRequest:
    if not authorization_:
        raise NotFoundAuthorizedHeaderException

    if not authorization_.startswith("Bearer "):
        raise NoTypeBearerException

    token_type, token = authorization_.split()

    is_blacklist_token(token, redis)

    payload = jwt_verify(token)

    user_id = payload.get("user_id")

    return LogoutRequest(user_id=user_id, access_token=token)


async def current_user_id_for_feed(authorization_: Optional[str] = Header(None)):
    if not authorization_:
        return -1
    try:
        token_type, token = authorization_.split()
        if token_type != "Bearer":
            raise InvalidTokenException
        payload = jwt.decode(jwt=token, key=ACCESS_TOKEN_SECRET, algorithms=ALGORITHM)

        user_id = payload.get("user_id")

        if user_id is None:
            raise InvalidTokenException
        return user_id

    except ExpiredSignatureError:
        raise ExpiredAccessTokenException
    except InvalidSignatureError:
        raise InvalidTokenException
    except:
        raise InvalidTokenException


def is_blacklist_token(access_token: str, redis: Redis):
    if redis.sismember("blacklist", access_token):
        raise TokenIsBlacklist


def jwt_verify(token: str):
    try:
        payload = jwt.decode(jwt=token, key=ACCESS_TOKEN_SECRET, algorithms=ALGORITHM)
        return payload
    except ExpiredSignatureError:
        raise ExpiredAccessTokenException
    except (InvalidSignatureError, DecodeError):
        raise InvalidTokenException
