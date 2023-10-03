import uuid
from unittest.mock import Mock

import pytest

from src.api.performance import performance_save_handler, performance_list_handler, PerformanceSaveRequest
from src.models.model import Performance
from src.service.performance import PerformanceService
from tests.fixture.performance import default_performance


class TestPerformanceAPI:
    @pytest.fixture
    def mocked_performance_service(self):
        return Mock(spec=PerformanceService)

    @pytest.mark.asyncio
    async def test_save_performance(self, mocked_performance_service: Mock, default_performance: Performance):
        #happy path
        default_performance.id = uuid.uuid4()

        mocked_performance_service.save_performance.return_value = default_performance

        performance = await performance_save_handler(
            q=PerformanceSaveRequest.model_validate(default_performance, from_attributes=True),
            performance_service=mocked_performance_service,
        )

        assert performance.id == default_performance.id



    @pytest.mark.asyncio
    async def test_get_performance_list(self, mocked_performance_service: Mock, default_performance: Performance):
        #happy path
        default_performance.id = uuid.uuid4()

        mocked_performance_service.get_performance_list.return_value = [
            default_performance,
        ]

        performances = await performance_list_handler(
            performance_service=mocked_performance_service,
        )

        assert len(performances) == 1
