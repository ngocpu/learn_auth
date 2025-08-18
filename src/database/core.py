from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
import psycopg2
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from src.setting import settings

DATABASE_URL=f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def get_conn():
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
    )
    try:
        yield conn
    finally:
        conn.close()

DbConn = Annotated[psycopg2.extensions.connection, Depends(get_conn)]
DbSession = Annotated[Session, Depends(get_db)]

