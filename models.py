from db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    hashtag = Column(String)
    priority = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("users.id"))
