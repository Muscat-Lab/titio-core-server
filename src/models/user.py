from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
    )
    username = mapped_column(
        String(256),
        unique=True,
        nullable=True,
        index=True,
    )
    password = mapped_column(String(256), nullable=False)

    @classmethod
    def create(cls, email: str, hashed_password: str):
        return cls(
            email=email,
            password=hashed_password,
        )
