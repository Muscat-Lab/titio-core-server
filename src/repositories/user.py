from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.connection import get_db
from src.models.user import User


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_user_list(self) -> list[User]:
        return list(
            (
                self.session.scalars(
                    select(User).order_by(User.created_at.desc()).limit(10)
                )
            ).all()
        )

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def save_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()  # db save
        self.session.refresh(instance=user)
        return user
