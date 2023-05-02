from app.database.database import engine
from sqlalchemy.sql import text


def patch_likes(feed_id: int, user_id: int):
    with engine.connect() as conn:
        data = {"feed_id": feed_id, "user_id": user_id}
        statement = text(
            """SELECT COUNT(*) FROM Likes WHERE feed_id = :feed_id AND user_id = :user_id"""
        )
        result = conn.execute(statement, data).scalar()

        if result == 1:
            statement = text(
                """DELETE FROM Likes WHERE feed_id = :feed_id AND user_id = :user_id"""
            )
            conn.execute(statement, data)
            conn.commit()
        else:
            statement = text("""INSERT INTO FeedFood VALUES(:feed_id,:user_id)""")
            conn.execute(statement, data)
            conn.commit()

        return "ok"


def get_my_likes(user_id: int):
    with engine.connect() as conn:
        data = {"user_id": user_id}
        statement = text(
            """SELECT * FROM Feed AS F LEFT OUTER JOIN Likes AS L ON F.feed_id = L.feed_id WHERE L.user_id = :user_id"""
        )
        result = conn.execute(statement, data)
        res = result.mappings().all()
        return res
