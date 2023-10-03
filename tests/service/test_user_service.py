import uuid
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.models.model import User
from src.repositories.user import UserRepository
from src.service.user import UserService
from tests.fixture.user import default_user


class TestUserService:
    @pytest.fixture()
    def mocked_user_repository(self):
        return Mock(spec=UserRepository)

    @pytest.fixture()
    def user_service(self, mocked_user_repository):
        return UserService(user_repository=mocked_user_repository)

    @pytest.mark.asyncio
    async def test_find_by_id(
        self,
        mocked_user_repository: Mock,
        user_service: UserService,
        default_user: User,
    ):
        # happy path
        mocked_user_repository.find_user_by_id.return_value = default_user

        user = await user_service.find_user_by_id(user_id=default_user.id)

        assert user == default_user

        # user not found
        mocked_user_repository.find_user_by_id.return_value = None

        try:
            await user_service.find_user_by_id(user_id=uuid.uuid4())
        except HTTPException as e:
            assert e.status_code == 404
