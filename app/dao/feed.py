from sqlalchemy.orm import Session
from app.database.database import engine
from sqlalchemy.sql import text

from app.dto.feed.FeedRequest import PostFeed
from app.model import feed, like, user


def get_feed(feed_id: int):
    with engine.connect() as conn:
        data = ({"feed_id": feed_id},)
        statement = text("""SELECT * FROM Feed WHERE feed_id = :feed_id""")
        result = conn.execute(statement, data)
        res = result.mappings().all()
        return res


def get_feeds(skip: int = 0, limit: int = 10):
    with engine.connect() as conn:
        data = {"skip": skip, "limit": limit}
        statement = text(
            """SELECT * FROM Feed ORDER BY created_at DESC LIMIT :skip, :limit"""
        )
        result = conn.execute(statement, data)
        res = result.mappings().all()
        return res


def post_feed(req: PostFeed):
    with engine.connect() as conn:
        data = {
            "image_url": req.image_url,
            "meal_time": req.meal_time,
            "date": req.date,
            "open": req.open,
            "feed_id": "null",
            "user_id": "1",
            "thumbnail_url": "abc",
            "created_at": "1234-01-20 01:01:01",
            "updated_at": "1234-01-20 01:01:01",
            "is_deleted": 1,
        }

        statement = text(
            """INSERT INTO Feed VALUES(:feed_id,:user_id,:image_url,:thumbnail_url,:meal_time,:date,:open,:created_at,:updated_at,:is_deleted)"""
        )

        conn.execute(statement, data)
        conn.commit()
        return "ok"
