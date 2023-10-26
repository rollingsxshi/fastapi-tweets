from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models import Tweet
from db import SessionLocal


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Depends - dependency injection
db_dependency = Annotated[Session, Depends(get_db)]


class TweetRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=300)
    hashtag: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=0, lt=5)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Tweet).all()


@router.get("/tweet/{tweet_id}", status_code=status.HTTP_200_OK)
async def read_tweet(db: db_dependency, tweet_id: int = Path(gt=0)): # validate path param gt=0
    tweet_model = db.query(Tweet).filter(Tweet.id == tweet_id).first()

    if tweet_model is not None:
        return tweet_model

    raise HTTPException(status_code=404, detail='Tweet not found.')


@router.post("/tweet", status_code=status.HTTP_201_CREATED)
async def create_tweet(db: db_dependency, req: TweetRequest):
    tweet_model = Tweet(**req.dict())

    db.add(tweet_model)
    db.commit()


@router.put("/tweet/{tweet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_tweet(
    db: db_dependency,
    req: TweetRequest,
    tweet_id: int = Path(gt=0)
):
    tweet_model = db.query(Tweet).filter(Tweet.id == tweet_id).first()

    if tweet_model is None:
        raise HTTPException(status_code=404, detail='Tweet not found.')

    tweet_model.title = req.title
    tweet_model.description = req.description
    tweet_model.hashtag = req.hashtag
    tweet_model.priority = req.priority

    db.add(tweet_model)
    db.commit()


@router.delete("/tweet/{tweet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tweet(db: db_dependency, tweet_id: int = Path(gt=0)):
    tweet_model = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if tweet_model is None:
        raise HTTPException(status_code=404, detail='Tweet not found.')

    db.query(Tweet).filter(Tweet.id == tweet_id).delete()
    db.commit()
