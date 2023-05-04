from fastapi import Depends, Header, HTTPException
from typing import Optional
import jwt
from starlette.config import Config

config = Config(".env")

ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET")
ALGORITHM = config("ALGORITHM")


async def current_user_id(authorization_: Optional[str] = Header(None)):
    if not authorization_:
        raise HTTPException(status_code=401, detail="Authorization 헤더를 찾을 수 없습니다")
    try:
        token_type, token = authorization_.split()

        if token_type != "Bearer":
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰 타입입니다")
        payload = jwt.decode(jwt=token, key=ACCESS_TOKEN_SECRET, algorithms=ALGORITHM)

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="잘못된 토큰입니다")
        return user_id
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="잘못된 토큰입니다")
