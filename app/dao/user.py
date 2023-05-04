from app.database.database import engine
from sqlalchemy.sql import text
from app.dto.user.UserRequest import *
from app.dto.user.UserResponse import *


async def create(user: CreateUserRequest):
    with engine.connect() as conn:
        statement = text(
            """INSERT INTO User (email, password, gender, age_group, nickname, goal) VALUES (:email, :password, :gender, :age_group, :nickname, :goal)"""
        )

        values = {
            "email": user.email,
            "password": user.password,
            "gender": user.gender.value,
            "age_group": user.age_group,
            "nickname": user.nickname,
            "goal": user.goal.value,
        }

        conn.execute(statement, values)
        return None


async def read_by_email(email: str):
    with engine.connect() as conn:
        statement = text("""SELECT * FROM User WHERE email = :email""")
        res = conn.execute(statement, {"email": email})
        user = res.fetchone()
        if not user:
            return None
        return user


async def read_by_user_id(user_id: int):
    with engine.connect() as conn:
        statement = text("""SELECT * FROM User WHERE user_id = :user_id""")
        res = conn.execute(statement, {"user_id": user_id})
        user = res.fetchone()
        if not user:
            return None
        return user


async def update_info(user: EditUserInfoRequest, user_id):
    with engine.connect() as conn:
        statement = text(
            """UPDATE User SET gender=:gender, age_group=:age_group, nickname=:nickname, goal=:goal WHERE user_id = :user_id"""
        )

        values = {
            "user_id": user_id,
            "gender": user.gender.value,
            "age_group": user.age_group,
            "nickname": user.nickname,
            "goal": user.goal.value,
        }

        conn.execute(statement, values)
        return None


async def update_password(password: bytes, user_id: int):
    with engine.connect() as conn:
        statement = text(
            """UPDATE User SET password=:password WHERE user_id = :user_id"""
        )

        values = {"user_id": user_id, "password": password}

        conn.execute(statement, values)
        return None


async def delete(user_id: int):
    with engine.connect() as conn:
        statement = text("""UPDATE User SET is_deleted=1 WHERE user_id = :user_id""")

        values = {"user_id": user_id}

        conn.execute(statement, values)
        return None
