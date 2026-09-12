from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
import crud

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


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    db = SessionLocal()
    try:
        user = crud.get_user(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        db.close()


@app.get("/users", response_model=list[User])
def list_users() -> list[User]:
    db = SessionLocal()
    try:
        return crud.get_users(db)
    finally:
        db.close()


@app.post("/create_user", response_model=User)
def create_user(user: User) -> User:
    db = SessionLocal()
    try:
        return crud.create_user(db, user)
    finally:
        db.close()
