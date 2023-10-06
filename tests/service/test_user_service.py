import uuid
from unittest.mock import Mock

import pytest
from fastapi import HTTPException, UploadFile

from src.models.model import Image, User
from src.repositories.image import ImageRepository
from src.repositories.user import UserRepository
from src.service.user import UserService
from src.utils.s3 import S3Util
from tests.fixture.user import default_user


class TestUserService:
    @pytest.fixture()
    def mocked_s3_util(self):
        return Mock(spec=S3Util)

    @pytest.fixture()
    def mocked_user_repository(self):
        return Mock(spec=UserRepository)

    @pytest.fixture()
    def mocked_image_repository(self):
        return Mock(spec=ImageRepository)

    @pytest.fixture()
    def user_service(
        self, mocked_s3_util, mocked_user_repository, mocked_image_repository
    ):
        return UserService(
            s3_util=mocked_s3_util,
            user_repository=mocked_user_repository,
            image_repository=mocked_image_repository,
        )

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

    @pytest.mark.asyncio
    async def test_upload_avatar_image(
        self,
        user_service: UserService,
        mocked_user_repository: Mock,
        mocked_s3_util: Mock,
    ):
        # happy path
        mocked_user_repository.find_user_by_id.return_value = default_user
        mocked_s3_util.upload_image_to_s3.return_value = Image(
            path="avatars/1",
            extension="png",
        )

        f = open("tests/fixture/images/gopher-idea_512x512.png", "rb")

        upload_file = UploadFile(
            filename="gopher-idea_512x512.png",
            file=f,
        )

        uploaded_url = await user_service.upload_avatar_image(
            user_id=uuid.uuid4(),
            file=upload_file,
        )

        assert uploaded_url is not None
