from app.dao.user import *
from app.dto.user.UserRequest import *
from app.dto.user.UserResponse import *


class UserService:
    async def register(self, user: CreateUserRequest):
        is_find = await read_by_email(user.email)
        if is_find:
            raise ValueError("중복된 email 입니다.")
        res = await create(user)
        return None
