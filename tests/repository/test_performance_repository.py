import datetime

import pytest

from src.models.model import Performance
from src.repositories.performance import PerformanceRepository
from tests.fixture.performance import default_performance
from tests.conftest import session

class TestPerformanceRepository:
    @pytest.fixture
    def performance_repository(self, session):
        return PerformanceRepository(session=session)

    @pytest.mark.asyncio
    async def test_save_performance(self, performance_repository: PerformanceRepository, default_performance: Performance):
        performance = await performance_repository.save_performance(default_performance)

        assert performance is not None

    @pytest.mark.asyncio
    async def test_get_performance_list(self, performance_repository: PerformanceRepository):
        performances = await performance_repository.get_performance_list()

        assert len(performances) != 0


