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
    created_at = Column(DateTime, default=datetime.now(), description="Create Time")
    updated_at = Column(DateTime, default=datetime.now(), description="Update Time")
