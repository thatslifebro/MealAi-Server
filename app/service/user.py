from app.dao.user import *
from app.dto.user.UserRequest import *
from app.dto.user.UserResponse import *
from app.utils.hash_password import hash_password
import bcrypt
from app.error.user import *

goal_num = {
    "balance": [1, 1, 1, 1],
    "diet": [0.8, 0.8, 1, 0.8],
    "muscle": [1, 1, 1.5, 1],
    "lchf": [1, 0.5, 1, 1.3],
}


class UserService:
    def __init__(self):
        pass

    async def register(self, user: CreateUserRequest):
        is_find = await read_by_email(user.email)
        if is_find:
            raise DuplicatedEmailException
        if is_find and is_find.get("is_deleted"):
            raise DeletedEmailException
        user.password = hash_password(user.password)
        res = await create(user)

        created_user = await read_by_email(user.email)
        daily_nutrient = await read_by_gender_age(
            gender=created_user.gender, age_group=created_user.age_group
        )
        user_daily_nutrient = [
            i * j for (i, j) in zip(daily_nutrient, goal_num[created_user.goal])
        ]
        await create_user_daily_nutrient(created_user.user_id, user_daily_nutrient)
        return None

    async def get_user_info(self, user_id: int):
        user = await read_by_user_id(user_id=user_id)
        if not user:
            raise NotFoundUserException
        return user

    async def edit_user_info(self, user_id, update: EditUserInfoRequest):
        is_find = await read_by_user_id(user_id)
        if not is_find:
            raise NotFoundUserException
        res = await update_info(user=update, user_id=user_id)

        user = await read_by_user_id(user_id)
        daily_nutrient = await read_by_gender_age(
            gender=user.gender, age_group=user.age_group
        )
        user_daily_nutrient = [
            i * j for (i, j) in zip(daily_nutrient, goal_num[user.goal])
        ]
        await update_user_daily_nutrient(user.user_id, user_daily_nutrient)

        return None

    async def change_password(self, user_id: int, update: ChangePasswordRequest):
        await self.check_password(user_id, update.current_password)
        change_password = hash_password(update.change_password)
        res = await update_password(password=change_password, user_id=user_id)
        return None

    async def delete_user(self, user_id: int):
        user = await read_by_user_id(user_id=user_id)
        if not user:
            raise NotFoundUserException

        res = await delete(user_id=user_id)
        return None

    async def check_password(self, user_id: int, password: str):
        user = await read_by_user_id(user_id=user_id)
        if not user:
            raise NotFoundUserException
        if not bcrypt.checkpw(password.encode("utf-8"), user.password):
            raise NotMatchPasswordException
        return None
