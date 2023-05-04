from app.dao.user import *
from app.dto.user.UserRequest import *
from app.dto.user.UserResponse import *

import bcrypt


class UserService:
    def __init__(self):
        pass

    async def register(self, user: CreateUserRequest):
        is_find = await read_by_email(user.email)
        if is_find:
            raise ValueError("중복된 email 입니다.")
        user.password = self.hash_password(user.password)
        res = await create(user)
        return None

    async def get_user_info(self, user_id: int):
        user = await read_by_user_id(user_id=user_id)
        if not user:
            raise ValueError("DB에 없는 user 입니다.")
        return user

    async def edit_user_info(self, user_id, update: EditUserInfoRequest):
        is_find = await read_by_user_id(user_id)
        if not is_find:
            raise ValueError("DB에 없는 user 입니다.")
        res = await update_info(user=update, user_id=user_id)
        return None

    async def change_password(self, user_id: int, update: ChangePasswordRequest):
        await self.check_password(user_id, update.current_password)
        change_password = self.hash_password(update.change_password)
        res = await update_password(password=change_password, user_id=user_id)
        return None

    async def delete_user(self, user_id: int):
        user = await read_by_user_id(user_id=user_id)
        if not user:
            raise ValueError("DB에 없는 user 입니다.")

        res = await delete(user_id=user_id)
        return None

    async def check_password(self, user_id: int, password: str):
        user = await read_by_user_id(user_id=user_id)
        if not user:
            raise ValueError("DB에 없는 user 입니다.")
        if not bcrypt.checkpw(password.encode("utf-8"), user.password):
            raise ValueError("현재 비밀번호가 일치하지 않습니다.")
        return None

    def hash_password(self, password: str) -> bytes:
        password_bytes = password.encode("utf-8")

        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        return hashed_bytes
