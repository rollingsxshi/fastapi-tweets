from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from passlib.context import CryptContext
from models import Tweet, Users
from db import SessionLocal
from routers.auth import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class UserDetails(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication failed.'
        )

    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, req: UserVerification):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication failed.'
        )

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(req.password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Error on password change.'
        )

    user_model.hashed_password = bcrypt_context.hash(req.new_password)
    db.add(user_model)
    db.commit()

@router.put("/details", status_code=status.HTTP_204_NO_CONTENT)
async def change_details(user: user_dependency, db: db_dependency, req: UserDetails):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication failed.'
        )

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.email = req.email
    user_model.username = req.username
    user_model.first_name = req.first_name
    user_model.last_name = req.last_name
    user_model.phone_number = req.phone_number
    db.add(user_model)
    db.commit()
