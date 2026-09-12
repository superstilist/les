from sqlalchemy.orm import Session
from typing import Optional

from base import User as UserSchema


def get_user(db: Session, user_id: int) -> Optional[UserSchema]:
    from main import UserModel
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        return None
    return UserSchema(id=user.id, username=user.username, email=user.email)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserSchema]:
    from main import UserModel
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return [UserSchema(id=user.id, username=user.username, email=user.email) for user in users]


def create_user(db: Session, user: UserSchema) -> UserSchema:
    from main import UserModel

    db_user = UserModel(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserSchema(id=db_user.id, username=db_user.username, email=db_user.email)


def update_user(db: Session, user_id: int, user_data: UserSchema) -> Optional[UserSchema]:
    from main import UserModel
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        return None
    user.username = user_data.username
    user.email = user_data.email
    db.commit()
    db.refresh(user)
    return UserSchema(id=user.id, username=user.username, email=user.email)


def delete_user(db: Session, user_id: int) -> bool:
    from main import UserModel
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True
