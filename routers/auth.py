from typing import Annotated
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Users
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, req: CreateUserRequest):
    user_model = Users(
        email = req.email,
        username = req.username,
        first_name = req.first_name,
        last_name = req.last_name,
        hashed_password = bcrypt_context.hash(req.password),
        role = req.role,
        is_active = True,
    )

    db.add(user_model)
    db.commit()
