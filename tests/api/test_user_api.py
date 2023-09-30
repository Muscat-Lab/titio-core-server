from unittest.mock import Mock

import pytest

from src.api.user import user_me_handler, UserMeResponse
from src.models.model import User
from src.service.user import UserService
from tests.api.api_fixture import default_user


class TestUserAPI:
    @pytest.fixture()
    def mocked_user_service(self):
        return Mock(spec=UserService)

    @pytest.mark.asyncio
    async def test_get_me(
        self,
        mocked_user_service: Mock,
        default_user: User,
    ):
        # happy path
        mocked_user_service.find_user_by_id.return_value = default_user

        me = await user_me_handler(
            user_service=mocked_user_service,
        )

        assert me.id == default_user.id
