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
    async def test_save_performance(
        self,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        # default performance
        performance = await performance_repository.save_performance(default_performance)

        assert performance is not None

        # update

        performance.title = "수정된 공연"

        performance = await performance_repository.save_performance(performance)

        assert performance.title == "수정된 공연"

    @pytest.mark.asyncio
    async def test_get_performance_list(
        self, performance_repository: PerformanceRepository
    ):
        # happy path
        performances = await performance_repository.get_performance_list(
            limit=20,
        )

        assert len(performances) != 0

        # test pre_booking_enabled filter
        await performance_repository.save_performance(
            Performance.create(
                title="사전예약 활성화",
                running_time="150분",
                grade="전체 관람가",
                begin=datetime.datetime.now(),
                end=datetime.datetime.now(),
                pre_booking_enabled=True,
                pre_booking_closed_at=datetime.datetime.now(),
            )
        )

        await performance_repository.save_performance(
            Performance.create(
                title="사전예약 비활성화",
                running_time="150분",
                grade="전체 관람가",
                begin=datetime.datetime.now(),
                end=datetime.datetime.now(),
                pre_booking_enabled=False,
                pre_booking_closed_at=None,
            )
        )

        performances = await performance_repository.get_performance_list(
            limit=20, pre_booking_enabled=True
        )

        assert len(performances) != 0
        for performance in performances:
            assert performance.pre_booking_enabled == True

        performances = await performance_repository.get_performance_list(
            limit=20, pre_booking_enabled=False
        )

        assert len(performances) != 0
        for performance in performances:
            assert performance.pre_booking_enabled == False

    @pytest.mark.asyncio
    async def test_delete_performance(
        self,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        # default performance
        performance = await performance_repository.save_performance(default_performance)

        assert performance is not None

        await performance_repository.delete_performance(performance.id)

        deleted_performance = await performance_repository.find_performance_by_id(
            performance_id=performance.id
        )

        assert deleted_performance is None
