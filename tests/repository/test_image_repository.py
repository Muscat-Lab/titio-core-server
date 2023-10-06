import pytest

from src.models.model import Image
from src.repositories.image import ImageRepository


class TestImageRepository:
    @pytest.fixture
    def image_repository(self, session):
        return ImageRepository(session=session)

    @pytest.mark.asyncio
    async def test_save_image(self, image_repository: ImageRepository):
        image = await image_repository.save_image(
            image=Image(
                path="test",
                extension="png",
            )
        )

        assert image.id is not None
