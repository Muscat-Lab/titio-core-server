from uuid import UUID

from fastapi import Depends, HTTPException

from src.models.model import User
from src.database.connection import get_db
from src.repositories.user import UserRepository


class UserService:
    def __init__(
        self,
        session=Depends(get_db),
        user_repository: UserRepository = Depends(UserRepository),
    ):
        self.session = session
        self.user_repository = user_repository

    async def get_user_list(self) -> list[User]:
        return self.user_repository.get_user_list()

    async def find_user_by_id(self, user_id: UUID) -> User:
        user = self.user_repository.find_user_by_id(user_id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def find_user_by_username(self, username: str) -> User:
        user = self.user_repository.find_user_by_username(username=username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
