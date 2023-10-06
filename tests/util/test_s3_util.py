from unittest.mock import Mock

import pytest

from src.config import config
from src.utils.s3 import S3Util


class TestImageUtil:
    @pytest.fixture
    def s3_util(
        self,
    ):
        return S3Util(
            config=config,
        )

    @pytest.mark.asyncio
    async def test_upload_image_to_s3(self, s3_util):
        f = open("tests/fixture/images/gopher-idea_512x512.png", "rb")

        image = await s3_util.upload_image_to_s3(
            file=f,
            filename="gopher-idea_512x512.png",
            path="test_files",
            save_name="gopher",
        )

        assert "gopher" in image.path
        assert image.extension == "png"
