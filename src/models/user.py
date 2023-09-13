from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), nullable=False)
    username = Column(String(256), nullable=True)
    password = Column(String(256), nullable=False)


