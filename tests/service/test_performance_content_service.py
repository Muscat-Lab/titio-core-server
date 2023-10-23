from unittest.mock import Mock

import pytest

from src.models.model import PerformanceContent
from src.repositories.performance import PerformanceRepository
from src.repositories.performance_content import PerformanceContentRepository
from src.service.performance_content import PerformanceContentService
from tests.fixture.performance import default_performance
from tests.fixture.performance_content import default_performance_content

__all__ = (
    "TestPerformanceContentService",
    "default_performance_content",
    "default_performance",
)


class TestPerformanceContentService:
    @pytest.fixture()
    def mocked_performance_repository(self):
        return Mock(spec=PerformanceRepository)

    @pytest.fixture()
    def mocked_performance_content_repository(self):
        return Mock(spec=PerformanceContentRepository)

    @pytest.fixture()
    def performance_service(
        self, mocked_performance_repository, mocked_performance_content_repository
    ):
        return PerformanceContentService(
            performance_repository=mocked_performance_repository,
            performance_content_repository=mocked_performance_content_repository,
        )

    @pytest.mark.asyncio
    async def test_save_performance_content(
        self,
        mocked_performance_repository: Mock,
        mocked_performance_content_repository: Mock,
        performance_service: PerformanceContentService,
        default_performance_content: PerformanceContent,
    ):
        mocked_performance_repository.find_performance_by_id.return_value = (
            default_performance_content
        )
        mocked_performance_content_repository.save_performance_content.return_value = (
            default_performance_content
        )

        performance_content = await performance_service.save_performance_content(
            default_performance_content
        )

        assert performance_content is not None

    @pytest.mark.asyncio
    async def test_get_performance_content_list(
        self,
        mocked_performance_content_repository: Mock,
        performance_service: PerformanceContentService,
        default_performance_content: PerformanceContent,
    ):
        m = mocked_performance_content_repository

        m.get_performance_content.return_value = default_performance_content

        performance_content = await performance_service.get_performance_content(
            default_performance_content.performance_id
        )

        assert performance_content is not None
