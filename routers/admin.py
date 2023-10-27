from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models import Tweet
from db import SessionLocal
from routers.auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication failed'
        )
    return db.query(Tweet).all()

@router.delete("/tweet/{tweet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tweet(
    user: user_dependency,
    db: db_dependency,
    tweet_id: int = Path(gt=0)
):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication failed'
        )

    tweet_model = db.query(Tweet).filter(Tweet.id == tweet_id).first()

    if tweet_model is None:
        raise HTTPException(status_code=404, detail='Tweet not found.')

    db.query(Tweet).filter(Tweet.id == tweet_id).delete()
    db.commit()