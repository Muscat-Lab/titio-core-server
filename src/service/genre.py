from uuid import UUID

from fastapi import Depends

from src.models.model import Genre
from src.repositories.genre import GenreRepository
from src.repositories.user import UserRepository


class GenreService:
    def __init__(
        self,
        genre_repository: GenreRepository = Depends(GenreRepository),
        user_repository: UserRepository = Depends(UserRepository),
    ):
        self.genre_repository = genre_repository
        self.user_repository = user_repository

    async def get_genre_list(
        self,
        limit: int,
        cursor: str | None = None,
    ) -> list[Genre]:
        return await self.genre_repository.get_genre_list(limit=limit, cursor=cursor)

    async def like_genre(self, genre_id: UUID, user_id: UUID):
        await self.user_repository.like_genres(
            genre_ids=[genre_id],
            user_id=user_id,
        )

    async def unlike_genre(self, genre_id: UUID, user_id: UUID):
        await self.user_repository.unlike_genre(
            genre_id=genre_id,
            user_id=user_id,
        )
