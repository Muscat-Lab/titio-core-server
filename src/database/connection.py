from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.user import User
from src.core.config import settings

# SQLAlchemy 설정 예시
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:tix2go@tix2go-db:3306/tix2go"
# SQLAlchemy 설정 예시


# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://tix2go:tix2go@tix2go-db:3306/tix2go-db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://tix2go:tix2go@db:3306/tix2go"

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


SessionFactory = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    session = SessionFactory()

    if session is None:
        raise Exception("session is not connected")
    try:
        yield session
    finally:
        session.close()
