from app.database.database import engine
from sqlalchemy.sql import text
from .like import get_feed_likes
from .feed import get_feed_food_by_id, get_food_info_by_id


def get_feeds_of_latest_week(user_id: int):
    with engine.connect() as conn:
        data = {"user_id": user_id}
        statement = text(
            """SELECT MAX(WEEK(date,1)) FROM Feed WHERE user_id=:user_id"""
        )
        latest_week = conn.execute(statement, data).scalar()
        return latest_week


def get_previous_week(user_id: int, search_week: int):
    with engine.connect() as conn:
        data = {"user_id": user_id, "search_week": search_week}
        statement = text(
            """SELECT MAX(WEEK(date,1)) FROM Feed WHERE user_id=:user_id AND WEEK(date,1)<:search_week"""
        )
        previous_week = conn.execute(statement, data).scalar()
        return previous_week


def get_feeds_by_week(user_id: int, search_week: int):
    with engine.connect() as conn:
        data = {"user_id": user_id, "search_week": search_week}
        statement = text(
            """SELECT * FROM Feed WHERE user_id = :user_id AND WEEK(date,1) = :search_week ORDER BY date"""
        )
        result = conn.execute(statement, data)
        feeds = result.mappings().all()
        return feeds
