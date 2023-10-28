import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv


# Load .env file
load_dotenv(".env.local")

engine = create_engine(
    os.getenv('SQLALCHEMY_DATABASE_URL'),
    # connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()