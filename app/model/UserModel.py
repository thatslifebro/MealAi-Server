from sqlalchemy import Boolean, Column, Date, Enum, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "ouser"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    gender = Column(Enum("M", "F"), nullable=False)
    age_group = Column(Integer, nullable=False)
    nickname = Column(String(255), nullable=False)
    created_at = Column(Date, default=func.now(), nullable=True)
    updated_at = Column(Date, default=None, onupdate=func.now(), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=True)
    goal = Column(Enum("balance", "diet", "muscle", "lchf"), nullable=False)
