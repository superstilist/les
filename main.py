from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str


app = FastAPI(title="Users API")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    db = next(get_db())
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(id=user.id, username=user.username, email=user.email)


@app.get("/users", response_model=list[User])
def list_users() -> list[User]:
    db = next(get_db())
    users = db.query(UserModel).all()
    return [User(id=user.id, username=user.username, email=user.email) for user in users]


@app.post("/create_user", response_model=User)
def create_user(user: User) -> User:
    db = next(get_db())
    db_user = UserModel(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(id=db_user.id, username=db_user.username, email=db_user.email)
