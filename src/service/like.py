from uuid import UUID

from fastapi import Depends

from src.enums.like import LikeChoiceType
from src.models.model import Genre, Performer
from src.repositories.genre import GenreRepository
from src.repositories.like import LikeRepository
from src.repositories.performance import PerformanceRepository
from src.repositories.performer import PerformerRepository
from src.repositories.user import UserRepository
from src.schema.like import LikeChoiceCreateSchema, LikeChoiceSchema

FETCH_COUNT = 100


class LikeService:
    def __init__(
        self,
        genre_repository: GenreRepository = Depends(GenreRepository),
        performer_repository: PerformerRepository = Depends(PerformerRepository),
        performance_repository: PerformanceRepository = Depends(PerformanceRepository),
        like_repository: LikeRepository = Depends(LikeRepository),
        user_repository: UserRepository = Depends(UserRepository),
    ):
        self.genre_repository = genre_repository
        self.performer_repository = performer_repository
        self.performance_repository = performance_repository
        self.like_repository = like_repository
        self.user_repository = user_repository

    async def get_like_choice_list(
        self, limit: int, cursor: str | None = None
    ) -> list[bytes]:
        like_choice_list = await self.like_repository.get_like_choice_list(
            limit=limit, cursor=cursor or "0"
        )

        if not like_choice_list:
            performer_list = await self._get_all_performers()
            genre_list = await self._get_all_genres()

            performer_key_score: dict[str, int] = {
                LikeChoiceSchema(
                    id=performer.id,
                    type=LikeChoiceType.Performer,
                    name=performer.name,
                    profile_image_url=performer.profile_image_url,
                ).model_dump_json(): performer.like_count
                for performer in performer_list
            }

            genre_key_score: dict[str, int] = {
                LikeChoiceSchema(
                    id=genre.id,
                    type=LikeChoiceType.Genre,
                    name=genre.name,
                    profile_image_url=None,
                ).model_dump_json(): genre.like_count
                for genre in genre_list
            }

            await self.like_repository.create_like_choice(
                key_score={
                    **performer_key_score,
                    **genre_key_score,
                }
            )

            like_choice_list = await self.like_repository.get_like_choice_list(
                limit=limit, cursor=cursor or "0"
            )

        return like_choice_list

    async def _get_all_performers(self) -> list[Performer]:
        fetched_count = FETCH_COUNT
        cursor = None

        all_performers = []

        while fetched_count == FETCH_COUNT:
            performer_list = (
                await self.performer_repository.get_performer_list_with_like_count(
                    limit=FETCH_COUNT, cursor=cursor
                )
            )
            if not performer_list:
                break
            fetched_count = len(performer_list)
            cursor = performer_list[-1].id

            all_performers.extend(performer_list)

        return all_performers

    async def _get_all_genres(self) -> list[Genre]:
        fetched_count = FETCH_COUNT
        cursor = None

        all_genres = []

        while fetched_count == FETCH_COUNT:
            genre_list = await self.genre_repository.get_genre_list_with_like_count(
                limit=FETCH_COUNT, cursor=cursor
            )
            if not genre_list:
                break
            fetched_count = len(genre_list)
            cursor = genre_list[-1].id

            all_genres.extend(genre_list)

        return all_genres

    async def flush_like_choice(self):
        await self.like_repository.flush_like_choice()

    async def bulk_create_like_choice(
        self, choices: list[LikeChoiceCreateSchema], user_id: UUID
    ):
        await self.user_repository.like_performers(
            performer_ids=[
                choice.id
                for choice in choices
                if choice.type == LikeChoiceType.Performer
            ],
            user_id=user_id,
        )

        await self.user_repository.like_genres(
            genre_ids=[
                choice.id for choice in choices if choice.type == LikeChoiceType.Genre
            ],
            user_id=user_id,
        )
