from db import Base
from sqlalchemy import Column, Integer, String


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    hashtag = Column(String)
    priority = Column(Integer, default=0)