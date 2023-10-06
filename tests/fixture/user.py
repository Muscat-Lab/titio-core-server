import uuid

import pytest

from src.models.model import User


@pytest.fixture()
def default_user() -> User:
    return User(
        id=uuid.uuid4(),
        email="default@test.com",
        password="default",
        username="default",
    )
