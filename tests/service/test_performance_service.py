import uuid
from unittest.mock import Mock

import pytest

from src.models.model import Performance, UserPerformanceLike
from src.service.performance import PerformanceService
from tests.fixture.performance import default_performance
from tests.service.fixture import mocked_performance_repository

__all__ = (
    "TestPerformanceService",
    "default_performance",
    "mocked_performance_repository",
)


class TestPerformanceService:
    @pytest.fixture()
    def performance_service(self, mocked_performance_repository):
        return PerformanceService(
            performance_repository=mocked_performance_repository,
        )

    @pytest.mark.asyncio
    async def test_get_performance_list(
        self,
        mocked_performance_repository: Mock,
        performance_service: PerformanceService,
        default_performance: Performance,
    ):
        default_performance.id = uuid.uuid4()

        mocked_performance_repository.get_performance_list.return_value = [
            default_performance
        ]

        performances = await performance_service.get_performance_list(
            limit=20,
        )

        assert len(performances) != 0

    @pytest.mark.asyncio
    async def test_get_hot_performance_list(
        self,
        mocked_performance_repository: Mock,
        performance_service: PerformanceService,
        default_performance: Performance,
    ):
        user_id = uuid.uuid4()
        default_performance.id = uuid.uuid4()

        mocked_performance_repository.get_performance_list_by_ids.return_value = [
            default_performance
        ]

        mocked_performance_repository.get_like_list_by_user_id.return_value = [
            UserPerformanceLike(
                user_id=user_id,
                performance_id=default_performance.id,
            )
        ]

        performances = await performance_service.get_hot_performance_list(
            user_id=user_id,
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
