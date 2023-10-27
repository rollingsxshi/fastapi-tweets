from fastapi import FastAPI
import models
from db import engine
from routers import auth, tweets, admin


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(tweets.router)
app.include_router(admin.router)
