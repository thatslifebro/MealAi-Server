from sqlalchemy.sql import text

from app.database.database import engine
from app.dto.user.UserRequest import *


async def create(user: CreateUserRequest):
    with engine.connect() as conn:
        statement = text(
            """
            INSERT INTO User (email, password, gender, age_group, nickname, goal) 
            VALUES (:email, :password, :gender, :age_group, :nickname, :goal)
            """
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
        conn.commit()

        statement = text(
            """
            SELECT * FROM User AS U
            LEFT JOIN DailyNutrient DN 
            on U.age_group = DN.age_group
            WHERE email = :email AND
            DN.gender = :gender;
            """
        )
        res = conn.execute(
            statement, {"email": user.email, "gender": user.gender.value}
        )
        user = res.fetchone()
        return user


async def read_by_email(email: str):
    with engine.connect() as conn:
        statement = text("""SELECT * FROM User WHERE email = :email""")
        res = conn.execute(statement, {"email": email})
        user = res.fetchone()
        return user


async def read_by_user_id(user_id: int):
    with engine.connect() as conn:
        statement = text("""SELECT * FROM User WHERE user_id = :user_id""")
        res = conn.execute(statement, {"user_id": user_id})
        user = res.fetchone()
        return user


async def read_by_gender_age(gender: str, age_group: int):
    with engine.connect() as conn:
        statement = text(
            """ SELECT * FROM DailyNutrient WHERE gender = :gender AND age_group = :age_group"""
        )
        res = conn.execute(statement, {"gender": gender, "age_group": age_group})
        nutrient = res.fetchone()
        return list(nutrient[2:])


async def get_user_daily_nutrient(user_id: int):
    with engine.connect() as conn:
        statement = text(
            """SELECT kcal, carbohydrate, protein, fat FROM UserDailyNutrient WHERE user_id=:user_id"""
        )

        values = {
            "user_id": user_id,
        }

        user = conn.execute(statement, values).mappings().first()

        return user


async def create_user_daily_nutrient(user_id: int, nutrient: list):
    with engine.connect() as conn:
        statement = text(
            """INSERT INTO UserDailyNutrient (user_id, kcal, carbohydrate, protein, fat) VALUES (:user_id, :kcal, :carbohydrate, :protein, :fat)"""
        )

        values = {
            "user_id": user_id,
            "kcal": nutrient[0],
            "carbohydrate": nutrient[1],
            "protein": nutrient[2],
            "fat": nutrient[3],
        }

        conn.execute(statement, values)
        conn.commit()
        return None


async def update_user_daily_nutrient(user_id: int, nutrient: list):
    with engine.connect() as conn:
        statement = text(
            """UPDATE UserDailyNutrient SET user_id=:user_id, kcal=:kcal, carbohydrate=:carbohydrate, protein=:protein, fat=:fat WHERE user_id=:user_id"""
        )

        values = {
            "user_id": user_id,
            "kcal": nutrient[0],
            "carbohydrate": nutrient[1],
            "protein": nutrient[2],
            "fat": nutrient[3],
        }

        conn.execute(statement, values)
        conn.commit()
        return None


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
        conn.commit()

        statement = text(
            """
            SELECT * FROM User AS U
            LEFT JOIN DailyNutrient DN 
            on U.age_group = DN.age_group
            WHERE user_id = :user_id AND
            DN.gender = :gender;
            """
        )
        res = conn.execute(statement, {"user_id": user_id, "gender": user.gender.value})
        user = res.fetchone()

        return user


async def update_password(password: bytes, user_id: int):
    with engine.connect() as conn:
        statement = text(
            """UPDATE User SET password=:password WHERE user_id = :user_id"""
        )

        values = {"user_id": user_id, "password": password}

        conn.execute(statement, values)
        conn.commit()
        return None


async def delete(user_id: int):
    with engine.connect() as conn:
        statement = text("""UPDATE User SET is_deleted=1 WHERE user_id = :user_id""")

        values = {"user_id": user_id}

        conn.execute(statement, values)
        conn.commit()
        return None
