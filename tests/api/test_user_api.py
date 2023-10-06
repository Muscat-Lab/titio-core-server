from unittest.mock import Mock

import pytest
from fastapi import File

from src.api.user import UserMeResponse, user_avatar_image_handler, user_me_handler
from src.models.model import Image, User
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

    @pytest.mark.asyncio
    async def test_user_avatar_image_handler(
        self,
        mocked_user_service: Mock,
        default_user: User,
    ):
        # happy path
        default_user.avatar_image = Image(
            path="test",
            extension="png",
        )
        mocked_user_service.upload_avatar_image.return_value = "http://s3/gopher.png"

        f = open("tests/fixture/images/gopher-idea_512x512.png", "rb")

        avatar_image = File()
        avatar_image.file = f

        user = await user_avatar_image_handler(
            avatar_image=avatar_image,
            user_service=mocked_user_service,
            auth=default_user.id,
        )

        assert user.avatar_image_url == "http://s3/gopher.png"
