from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import config

engine = create_engine(config.DB_URI, echo=True)

SessionFactory = sessionmaker(
    autoflush=False, autocommit=False, expire_on_commit=False, bind=engine
)


def get_db():
    session = SessionFactory()

    if session is None:
        raise Exception("session is not connected")
    try:
        yield session
    finally:
        session.close()
