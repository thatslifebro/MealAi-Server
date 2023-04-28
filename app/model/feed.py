from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Date,
    Integer,
    String,
    DateTime,
    Float,
)
from sqlalchemy.dialects.mysql import VARCHAR
import datetime
from app.database.database import Base


class Feed(Base):
    __tablename__ = "Feed"

    feed_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("User.user_id"))
    image_url = Column(String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql"))
    thumbnail_url = Column(
        String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql")
    )
    meal_time = Column(String(10).with_variant(VARCHAR(255, charset="utf8"), "mysql"))
    date = Column(Date)
    open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)


class FoodInfo(Base):
    __tablename__ = "FoodInfo"

    food_id = Column(Integer, primary_key=True)
    name = Column(String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql"))
    weight = Column(Float(precision=7, decimal_return_scale=2))
    kca = Column(Float(precision=7, decimal_return_scale=2))
    carbohydrate = Column(Float(precision=7, decimal_return_scale=2))
    protein = Column(Float(precision=7, decimal_return_scale=2))
    fat = Column(Float(precision=7, decimal_return_scale=2))


class FeedFoods(Base):
    __tablename__ = "FeedFoods"

    feed_id = Column(ForeignKey("Feed.feed_id"), primary_key=True)
    image_url = Column(String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql"))
    food_id = Column(ForeignKey("FoodInfo.food_id"), primary_key=True)
    weight = Column(Float(precision=7, decimal_return_scale=2))
    is_deleted = Column(Boolean, default=False)
