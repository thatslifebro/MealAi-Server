from app.database.database import engine
from sqlalchemy.sql import text


def get_feed(feed_id: int):
    with engine.connect() as conn:
        data = ({"feed_id": feed_id},)
        statement = text("""SELECT * FROM Feed WHERE feed_id = :feed_id""")
        result = conn.execute(statement, data)
        feed_data = result.mappings().first()

        statement = text("""SELECT * FROM FeedFood WHERE feed_id = :feed_id""")
        result = conn.execute(statement, data)
        feed_food_data = result.mappings().all()

        return feed_data, feed_food_data


def get_feeds(skip: int = 0, limit: int = 10):
    with engine.connect() as conn:
        data = {"skip": skip, "limit": limit}
        statement = text(
            """SELECT * FROM Feed ORDER BY created_at DESC LIMIT :skip, :limit"""
        )
        result = conn.execute(statement, data)
        res = result.mappings().all()
        return res


def post_feed(post_feed_data, foods_data):
    with engine.connect() as conn:
        statement = text(
            """INSERT INTO Feed VALUES(:feed_id,:user_id,:image_url,:thumbnail_url,:meal_time,:date,:open,:created_at,:updated_at,:is_deleted)"""
        )

        conn.execute(statement, post_feed_data)
        conn.commit()

        # 최근 insert 한 row 의 id 가져오기.
        statement = text("""SELECT LAST_INSERT_ID()""")
        result = conn.execute(statement)
        feed_id = result.mappings().first()["LAST_INSERT_ID()"]

        for food_data in foods_data:
            post_food_data = {
                "food_id": food_data.food_id,
                "image_url": food_data.image_url,
                "weight": food_data.weight,
                "is_deleted": 0,
                "feed_id": feed_id,
            }
            statement = text(
                """INSERT INTO FeedFood VALUES(:feed_id,:image_url,:food_id,:weight,:is_deleted)"""
            )

            conn.execute(statement, post_food_data)
            conn.commit()

        return "ok"


def delete_feed(feed_id: int):
    with engine.connect() as conn:
        data = ({"feed_id": feed_id},)
        statement = text("""DELETE FROM Feed WHERE feed_id = :feed_id""")
        conn.execute(statement, data)
        conn.commit()

        statement = text("""DELETE FROM FeedFood WHERE feed_id = :feed_id""")
        conn.execute(statement, data)
        conn.commit()

        return "ok"


def patch_feed(feed_id: int, patch_feed_data, foods_data):
    with engine.connect() as conn:
        data = ({"feed_id": feed_id},)
        statement = text(
            """UPDATE Feed SET meal_time=:meal_time, date=:date, open=:open WHERE feed_id=feed_id"""
        )
        conn.execute(statement, patch_feed_data)
        conn.commit()

        statement = text("""DELETE FROM FeedFood WHERE feed_id = :feed_id""")
        conn.execute(statement, data)
        conn.commit()

        for food_data in foods_data:
            post_food_data = {
                "food_id": food_data.food_id,
                "image_url": food_data.image_url,
                "weight": food_data.weight,
                "is_deleted": 0,
                "feed_id": feed_id,
            }
            statement = text(
                """INSERT INTO FeedFood VALUES(:feed_id,:image_url,:food_id,:weight,:is_deleted)"""
            )

            conn.execute(statement, post_food_data)
            conn.commit()

        return "ok"
