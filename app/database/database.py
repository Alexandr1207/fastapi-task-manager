from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/TaskManagerDB"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass