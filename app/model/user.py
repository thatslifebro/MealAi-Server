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


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql"))
    password = Column(String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql"))
    gender = Column(String(10).with_variant(VARCHAR(255, charset="utf8"), "mysql"))
    age_group = Column(Integer)
    nickname = Column(String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    goal = Column(String(50).with_variant(VARCHAR(255, charset="utf8"), "mysql"))


class UserDailyNutrient(Base):
    __tablename__ = "UserDailyNutrient"

    user_id = Column(ForeignKey("User.user_id"), primary_key=True)
    kcal = Column(Float(precision=7, decimal_return_scale=2))
    carbohydrate = Column(Float(precision=7, decimal_return_scale=2))
    protein = Column(Float(precision=7, decimal_return_scale=2))
    fat = Column(Float(precision=7, decimal_return_scale=2))


class DailyNutrient(Base):
    __tablename__ = "DailyNutrient"

    gender = Column(
        String(10).with_variant(VARCHAR(255, charset="utf8"), "mysql"), primary_key=True
    )
    age_group = Column(Integer, primary_key=True)
    kcal = Column(Float(precision=7, decimal_return_scale=2))
    carbohydrate = Column(Float(precision=7, decimal_return_scale=2))
    protein = Column(Float(precision=7, decimal_return_scale=2))
    fat = Column(Float(precision=7, decimal_return_scale=2))
