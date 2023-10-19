import pytest

from src.models.model import User
from src.repositories.performance import PerformanceRepository
from src.repositories.user import UserRepository
from tests.test_utils import generate_random_email


@pytest.fixture
def performance_repository(session):
    return PerformanceRepository(session=session)


@pytest.fixture
def user_repository(session):
    return UserRepository(session=session)


async def new_user(user_repository):
    return await user_repository.save_user(
        User.create(
            email=generate_random_email(),
            password="password",
            username="username",
        )
    )
