from sqlalchemy import (
    Integer,
    Column,
    String,
    DATETIME,
    Enum,
)
from app.database.database import Base


class RefreshToken(Base):
    __tablename__ = "RefreshToken"

    user_id = Column(Integer, autoincrement=False, primary_key=True)
    refresh_token = Column(String(255), nullable=False)
