from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Date,
    Integer,
    String,
    DateTime,
    Numeric,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
import datetime
from app.database.database import Base, engine
from app.dto.feed.FeedRequest import MealTimeEnum


class Feed(Base):
    __tablename__ = "Feed"

    feed_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    image_url = Column(
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql"), nullable=True
    )
    thumbnail_url = Column(
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql"), nullable=True
    )
    meal_time = Column(Enum(MealTimeEnum))
    date = Column(Date, default=datetime.datetime.today(), nullable=False)
    open = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    user = relationship("User")


class FoodInfo(Base):
    __tablename__ = "FoodInfo"

    food_id = Column(Integer, primary_key=True)
    name = Column(
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql"), nullable=False
    )
    weight = Column(Numeric(precision=7, scale=2), nullable=False)
    kcal = Column(Numeric(precision=7, scale=2), nullable=False)
    carbohydrate = Column(Numeric(precision=7, scale=2), nullable=False)
    protein = Column(Numeric(precision=7, scale=2), nullable=False)
    fat = Column(Numeric(precision=7, scale=2), nullable=False)


class FeedFood(Base):
    __tablename__ = "FeedFood"

    feed_id = Column(Integer, ForeignKey("Feed.feed_id"), primary_key=True)
    image_url = Column(
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql"), nullable=True
    )
    food_id = Column(Integer, ForeignKey("FoodInfo.food_id"), primary_key=True)
    weight = Column(Numeric(precision=7, scale=2))
    is_deleted = Column(Boolean, default=0)

    food = relationship("FoodInfo")
    feed = relationship("Feed", cascade="delete")

