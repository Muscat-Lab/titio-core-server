import pytest

from src.models.model import User, Performer
from src.repositories.performer import PerformerRepository
from src.repositories.user import UserRepository
from tests.conftest import session
from tests.repository.fixture import new_user, user_repository, performer_repository

__all__ = ("TestUserRepository", "session", "user_repository", "performer_repository")


class TestUserRepository:

    @pytest.fixture()
    def default_user(self, user_repository: UserRepository):
        user = User.create(
            email="default@tito.kr",
            password="default",
            username="default",
        )

        return user

    @pytest.mark.asyncio
    async def test_get_user_list(self, user_repository: UserRepository):
        await new_user(user_repository)

        users = await user_repository.get_user_list()

        assert len(users) != 0

    @pytest.mark.asyncio
    async def test_get_user_by_email(
            self,
            user_repository: UserRepository,
    ):
        user = await new_user(user_repository)

        assert (
                await user_repository.get_user_by_email(email=user.email)
                == user
        )

    @pytest.mark.asyncio
    async def test_get_user_by_kakao_id(
            self,
            user_repository: UserRepository,
    ):
        user = await new_user(user_repository)
        user.kakao_id = "test"
        await user_repository.save_user(user)

        assert (
                await user_repository.get_user_by_kakao_id(kakao_id=user.kakao_id)
                == user
        )

    @pytest.mark.asyncio
    async def test_get_user_by_id(
            self,
            user_repository: UserRepository,
    ):
        user = await new_user(user_repository)

        assert (
                await user_repository.find_user_by_id(user_id=user.id)
                == user
        )

    @pytest.mark.asyncio
    async def test_find_user_by_username(
            self,
            user_repository: UserRepository,
    ):
        user = await new_user(user_repository)

        assert (
                await user_repository.find_user_by_username(username=user.username)
                == user
        )

    @pytest.mark.asyncio
    async def test_like_performers(
            self,
            user_repository: UserRepository,
            performer_repository: PerformerRepository,
    ):
        user = await new_user(user_repository)

        performer = await performer_repository.save_performer(
            performer=Performer.create(
                name="테스트",
                description="테스트",
            )
        )

        await user_repository.like_performers(
            performer_ids=[performer.id],
            user_id=user.id,
        )

        assert (
                (await user_repository.get_like_performance_list(
                    user_id=user.id,
                    performance_ids=[performer.id],
                ))[0].performer_id == performer.id
        )

    @pytest.mark.asyncio
    async def test_find_user_by_email(
            self,
            user_repository: UserRepository,
    ):
        user = await new_user(user_repository)

        assert (
                await user_repository.find_user_by_email(email=user.email)
                == user
        )
