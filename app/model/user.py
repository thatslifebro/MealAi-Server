from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Float,
    Enum,
    CheckConstraint,
    text,
)
from sqlalchemy.orm import relationship
from _datetime import datetime
from app.database.database import Base


class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    gender = Column(Enum("M", "F"), nullable=False)
    age_group = Column(
        Integer,
        CheckConstraint("age_group BETWEEN 1 AND 9"),
        nullable=False,
    )
    nickname = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    goal = Column(Enum("balance", "diet", "muscle", "lchf"), nullable=False)


class UserDailyNutrient(Base):
    __tablename__ = "UserDailyNutrient"

    user_id = Column(ForeignKey("User.user_id"), primary_key=True)
    kcal = Column(Float(precision=7, decimal_return_scale=2), nullable=False)
    carbohydrate = Column(Float(precision=7, decimal_return_scale=2), nullable=False)
    protein = Column(Float(precision=7, decimal_return_scale=2), nullable=False)
    fat = Column(Float(precision=7, decimal_return_scale=2), nullable=False)

    user = relationship("User")


class DailyNutrient(Base):
    __tablename__ = "DailyNutrient"

    gender = Column(Enum("M", "F"), primary_key=True)
    age_group = Column(
        Integer, CheckConstraint("age_group BETWEEN 1 AND 9"), primary_key=True
    )
    kcal = Column(Float(precision=7, decimal_return_scale=2), nullable=False)
    carbohydrate = Column(Float(precision=7, decimal_return_scale=2), nullable=False)
    protein = Column(Float(precision=7, decimal_return_scale=2), nullable=False)
    fat = Column(Float(precision=7, decimal_return_scale=2), nullable=False)
