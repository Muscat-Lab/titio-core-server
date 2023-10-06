import pytest

from src.models.model import User
from src.repositories.user import UserRepository
from tests.conftest import session


class TestUserRepository:
    @pytest.fixture()
    def user_repository(self, session):
        return UserRepository(session=session)

    @pytest.fixture()
    def default_user(self, user_repository: UserRepository):
        user = User.create(
            email="default@tito.kr",
            password="default",
            username="default",
        )

        return user

    @pytest.mark.asyncio
    async def test_get_user_by_id(
        self,
        user_repository: UserRepository,
        default_user: User,
    ):
        await user_repository.save_user(user=default_user)

        assert user_repository.find_user_by_id(user_id=default_user.id) == default_user
