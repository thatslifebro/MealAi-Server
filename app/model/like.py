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


class Likes(Base):
    __tablename__ = "Likes"

    feed_id = Column(ForeignKey("Feed.feed_id"), primary_key=True)
    user_id = Column(ForeignKey("User.user_id"), primary_key=True)
