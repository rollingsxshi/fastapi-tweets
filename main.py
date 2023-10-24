from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
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

@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Tweet).all()