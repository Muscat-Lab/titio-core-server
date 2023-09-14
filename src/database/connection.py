from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings


DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    session = SessionFactory()
    if session is None:
        raise Exception("session is not connected")
    try:
        yield session
    finally:
        session.close()
