from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class Likes(Base):
    __tablename__ = "Likes"

    feed_id = Column(Integer, ForeignKey("Feed.feed_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)

    user = relationship("User", back_populates="Likes")
    feed = relationship("Feed", back_populates="Likes")
