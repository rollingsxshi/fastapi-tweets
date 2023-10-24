from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Path, status
from models import Tweet
import models
from db import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Depends - dependency injection
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Tweet).all()


@app.get("/tweet/{tweet_id}", status_code=status.HTTP_200_OK)
async def read_tweet(db: db_dependency, tweet_id: int = Path(gt=0)): # validate path param gt=0
    tweet_model = db.query(Tweet).filter(Tweet.id == tweet_id).first()

    if tweet_model is not None:
        return tweet_model

    raise HTTPException(status_code=404, detail='Tweet not found.')
