from app.dao.like import get_feed_likes
from app.database.database import engine
from sqlalchemy.sql import text


def get_feed_by_id(feed_id: int):
    with engine.connect() as conn:
        data = {"feed_id": feed_id}
        statement = text("""SELECT * FROM Feed WHERE feed_id = :feed_id""")
        result = conn.execute(statement, data)
        feed_data = result.mappings().first()
        return feed_data


def get_feed_food_by_id(feed_id: int):
    with engine.connect() as conn:
        data = {"feed_id": feed_id}
        statement = text("""SELECT * FROM FeedFood WHERE feed_id = :feed_id""")
        result = conn.execute(statement, data)
        feed_food_data = result.mappings().all()
        return feed_food_data


def get_food_info_by_id(food_id: int):
    with engine.connect() as conn:
        data = {"food_id": food_id}
        statement = text("""SELECT * FROM FoodInfo WHERE food_id = :food_id""")
        result = conn.execute(statement, data)
        food_info = result.mappings().first()
        return food_info


def get_feeds_by_skip_limit(skip: int = 0, limit: int = 10):
    with engine.connect() as conn:
        data = {"skip": skip, "limit": limit}
        statement = text(
            """SELECT * FROM Feed ORDER BY created_at DESC LIMIT :skip, :limit"""
        )
        result = conn.execute(statement, data)
        feeds = result.mappings().all()
        return feeds


def post_feed(post_feed_data, foods_data):
    with engine.connect() as conn:
        statement = text(
            """INSERT INTO Feed VALUES(:feed_id,:user_id,:image_url,:thumbnail_url,:meal_time,:date,:open,:created_at,:updated_at,:is_deleted)"""
        )

        conn.execute(statement, post_feed_data)
        conn.commit()


def get_recent_post_id():
    with engine.connect() as conn:
        statement = text("""SELECT LAST_INSERT_ID()""")
        result = conn.execute(statement)
        feed_id = result.mappings().first()["LAST_INSERT_ID()"]
        return feed_id


def insert_feed_food(feed_id, food_data):
    with engine.connect() as conn:
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


def delete_feed_food(feed_id: int):
    with engine.connect() as conn:
        data = ({"feed_id": feed_id},)

        statement = text("""DELETE FROM FeedFood WHERE feed_id = :feed_id""")
        conn.execute(statement, data)
        conn.commit()


def delete_feed(feed_id: int):
    with engine.connect() as conn:
        data = ({"feed_id": feed_id},)
        statement = text("""DELETE FROM Feed WHERE feed_id = :feed_id""")
        conn.execute(statement, data)
        conn.commit()


def patch_feed(feed_id: int, patch_feed_data):
    with engine.connect() as conn:
        statement = text(
            """UPDATE Feed SET meal_time=:meal_time, date=:date, open=:open WHERE feed_id=feed_id"""
        )
        conn.execute(statement, patch_feed_data)
        conn.commit()
