from typing import Annotated
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

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


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return True


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


@router.post("/token")
async def access_token_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'
    return 'Successful Authentication'
