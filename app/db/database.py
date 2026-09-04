import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set. Please check your .env file.")
# Create a SQLAlchemy engine to connect to the PostgreSQL database
# Connecting to the database using the provided DATABASE_URL from the environment variables
engine = create_engine(DATABASE_URL)

# bind the engine to a sessionmaker, which will be used to create database sessions for interacting with the database
# The sessionmaker is configured with the engine and set to not autoflush and not autocommit, meaning that changes will not be automatically flushed to the database and will require explicit commit calls
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass




