from sqlalchemy.orm import Session

from app.model import feed, like, user


def get_user(db: Session, user_id: int):
    return db.query(user.User).filter(user.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user.User).offset(skip).limit(limit).all()
