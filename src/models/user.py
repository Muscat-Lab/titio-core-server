from datetime import datetime
from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
    )
    username = Column(
        String(256),
        unique=True,
        nullable=True,
        index=True,
    )
    password = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    @classmethod
    def create(cls, email: str, hashed_password: str):
        return cls(
            email=email,
            password=hashed_password,
        )
