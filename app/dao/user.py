from app.database.database import engine
from sqlalchemy.sql import text
from app.dto.user.UserRequest import CreateUserRequest


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
