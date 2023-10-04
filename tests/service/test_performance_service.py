from unittest.mock import Mock

import pytest

from src.models.model import Performance
from src.repositories.performance import PerformanceRepository
from src.service.performance import PerformanceService
from tests.fixture.performance import default_performance


class TestPerformanceService:
    @pytest.fixture()
    def mocked_performance_repository(self):
        return Mock(spec=PerformanceRepository)

    @pytest.fixture()
    def performance_service(self, mocked_performance_repository):
        return PerformanceService(performance_repository=mocked_performance_repository)

    @pytest.mark.asyncio
    async def test_get_performance_list(
        self,
        mocked_performance_repository: Mock,
        performance_service: PerformanceService,
        default_performance: Performance,
    ):
        mocked_performance_repository.get_performance_list.return_value = [
            default_performance
        ]

        performances = await performance_service.get_performance_list(
            limit=20,
        )

        assert len(performances) != 0

    @pytest.mark.asyncio
    async def test_save_performance(
        self,
        mocked_performance_repository: Mock,
        performance_service: PerformanceService,
        default_performance: Performance,
    ):
        mocked_performance_repository.save_performance.return_value = (
            default_performance
        )

        performance = await performance_service.save_performance(default_performance)

        assert performance is not None

    @pytest.mark.asyncio
    async def test_delete_performance(
        self,
        mocked_performance_repository: Mock,
        performance_service: PerformanceService,
        default_performance: Performance,
    ):
        mocked_performance_repository.delete_performance.return_value = (
            default_performance
        )

        performance = await performance_service.delete_performance(
            default_performance.id
        )

        assert performance is not None
