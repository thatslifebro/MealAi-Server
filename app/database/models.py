from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Date,
    Enum,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
import datetime
from .database import Base


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True)
    email = Column(
        String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb")
    )
    password = Column(
        String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb")
    )
    gender = Column(
        String(10).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb")
    )
    age_group = Column(Integer)
    nickname = Column(
        String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb")
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    goal = Column(
        String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb")
    )


class Feed(Base):
    __tablename__ = "Feed"

    feed_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("User.user_id"))
    image_url = Column(
        String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb")
    )
    thumbnail_url = Column(
        String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb")
    )
    meal_time = Column(
        String(10).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb")
    )
    date = Column(Date)
    open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)


class Likes(Base):
    __tablename__ = "Likes"

    feed_id = Column(ForeignKey("Feed.feed_id"), primary_key=True)
    user_id = Column(ForeignKey("User.user_id"), primary_key=True)


# Class UserDailyNutrient(Base):
#     __tablename__ = "UserDailyNutrient"
