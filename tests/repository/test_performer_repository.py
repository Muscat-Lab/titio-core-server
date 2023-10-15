import pytest

from src.models.model import Performer, User
from src.repositories.performer import PerformerRepository
from src.repositories.user import UserRepository


class TestPerformerRepository:
    @pytest.fixture
    def performer_repository(self, session):
        return PerformerRepository(session=session)

    @pytest.fixture
    def user_repository(self, session):
        return UserRepository(session=session)

    @pytest.mark.asyncio
    async def test_save_performer(self, performer_repository: PerformerRepository):
        performer = await performer_repository.save_performer(
            performer=Performer.create(
                name="테스트",
                description="테스트",
            )
        )

        assert performer.id is not None

    @pytest.mark.asyncio
    async def test_get_performer_list(self, performer_repository: PerformerRepository):
        performers = await performer_repository.get_performer_list(
            limit=20,
        )

        assert len(performers) != 0

    @pytest.mark.asyncio
    async def test_get_performer_list_with_like_count(
        self, performer_repository: PerformerRepository, user_repository: UserRepository
    ):
        users = [
            (
                await user_repository.save_user(
                    user=User.create(
                        email=f"test_performer_like_test_{i}@tito.com",
                        password="test",
                    )
                )
            )
            for i in range(20)
        ]

        first_performer = await performer_repository.save_performer(
            performer=Performer.create(
                name="테스트",
                description="테스트",
            )
        )

        second_performer = await performer_repository.save_performer(
            performer=Performer.create(
                name="테스트",
                description="테스트",
            )
        )

        for user in users:
            await user_repository.like_performers(
                performer_ids=[first_performer.id],
                user_id=user.id,
            )

        for user in users[:10]:
            await user_repository.like_performers(
                performer_ids=[second_performer.id],
                user_id=user.id,
            )

        performers = await performer_repository.get_performer_list_with_like_count(
            limit=20,
        )

        for performer in performers:
            if performer.id == first_performer.id:
                assert performer.like_count == 20
            elif performer.id == second_performer.id:
                assert performer.like_count == 10
