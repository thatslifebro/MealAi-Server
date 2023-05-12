from app.database.database import engine
from sqlalchemy.sql import text


async def upsert_refresh_token(user_id: int, refresh_token: str):
    with engine.connect() as conn:
        statement = text(
            """INSERT INTO RefreshToken (user_id, refresh_token) VALUES (:user_id, :refresh_token) ON DUPLICATE KEY UPDATE refresh_token=:refresh_token"""
        )

        values = {
            "user_id": user_id,
            "refresh_token": refresh_token,
        }

        conn.execute(statement, values)
        conn.commit()
        return None


async def read_refresh_token_by_user_id(user_id: int):
    with engine.connect() as conn:
        statement = text("""SELECT * FROM RefreshToken WHERE user_id=:user_id""")

        values = {
            "user_id": user_id,
        }

        res = conn.execute(statement, values)
        user = res.fetchone()
        return user


async def delete_refresh_token(user_id: int):
    with engine.connect() as conn:
        statement = text("""DELETE FROM RefreshToken WHERE user_id=:user_id""")

        values = {
            "user_id": user_id,
        }

        conn.execute(statement, values)
        conn.commit()

        return None
