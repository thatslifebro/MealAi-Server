from fastapi import Depends, Header, HTTPException
from typing import Optional
import jwt
from jwt.exceptions import *
from starlette.config import Config
from app.error.auth import *

config = Config(".env")

ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET")
ALGORITHM = config("ALGORITHM")


async def current_user_id(authorization_: Optional[str] = Header(None)):
    if not authorization_:
        raise NotFoundAuthorizedHeaderException
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
