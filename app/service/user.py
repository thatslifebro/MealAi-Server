import bcrypt

from app.dao.user import *
from app.dto.user.UserRequest import *
from app.error.user import *
from app.utils.hash_password import hash_password

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
        is_user = await read_by_email(user.email)
        check_register(is_user)

        user.password = hash_password(user.password)
        created_user = await create(user)

        daily_nutrient = created_user[-4:]
        user_daily_nutrient = map_user_daily_nutrient(
            daily_nutrient, goal_num[created_user.goal]
        )

        await create_user_daily_nutrient(created_user.user_id, user_daily_nutrient)
        return None

    async def get_user_info(self, user_id: int):
        user = await read_by_user_id(user_id=user_id)
        check_user(user)
        return user

    async def edit_user_info(self, user_id: int, update: EditUserInfoRequest):
        user = await read_by_user_id(user_id=user_id)
        check_user(user)
        updated_user = await update_info(user=update, user_id=user_id)

        daily_nutrient = updated_user[-4:]

        user_daily_nutrient = map_user_daily_nutrient(
            daily_nutrient, goal_num[updated_user.goal]
        )

        await update_user_daily_nutrient(user_id, user_daily_nutrient)

        return None

    async def change_password(self, user_id: int, update: ChangePasswordRequest):
        await self.check_password(user_id, update.current_password)
        change_password = hash_password(update.change_password)
        await update_password(password=change_password, user_id=user_id)
        return None

    async def delete_user(self, user_id: int):
        user = await read_by_user_id(user_id=user_id)
        check_user(user)
        await delete(user_id=user_id)
        return None

    async def check_password(self, user_id: int, password: str):
        user = await read_by_user_id(user_id=user_id)
        check_user(user)
        if not bcrypt.checkpw(password.encode("utf-8"), user.password):
            raise NotMatchPasswordException
        return None


def check_user(user: any):
    if not user:
        raise NotFoundUserException
    if user and user.is_deleted:
        raise DeletedEmailException
    return user


def check_register(user):
    if user:
        raise DuplicatedEmailException
    if user and user.is_deleted:
        raise DeletedEmailException
    return True


def map_user_daily_nutrient(daily_nutrient: list, goal: list):
    user_daily_nutrient = [i * j for (i, j) in zip(daily_nutrient, goal)]
    return user_daily_nutrient
