import uuid
from datetime import date, time
from unittest.mock import Mock

import pytest

from src.models.model import Performance, Schedule
from src.repositories.performance import PerformanceRepository
from src.repositories.schedule import ScheduleRepository
from src.service.schedule import ScheduleService
from tests.fixture.performance import default_performance

__all__ = ("TestScheduleService", "default_performance")


class TestScheduleService:
    @pytest.fixture
    def mocked_performance_repository(self):
        return Mock(spec=PerformanceRepository)

    @pytest.fixture
    def mocked_schedule_repository(self):
        return Mock(spec=ScheduleRepository)

    @pytest.fixture
    def schedule_service(
        self,
        mocked_performance_repository: Mock,
        mocked_schedule_repository: Mock,
    ):
        return ScheduleService(
            performance_repository=mocked_performance_repository,
            schedule_repository=mocked_schedule_repository,
        )

    @pytest.mark.asyncio
    async def test_get_date_list(
        self,
        schedule_service: ScheduleService,
        mocked_performance_repository: Mock,
        mocked_schedule_repository: Mock,
        default_performance: Performance,
    ):
        default_performance.id = uuid.uuid4()

        mocked_performance_repository.find_performance_by_id.return_value = (
            default_performance
        )

        mocked_schedule_repository.get_date_list.return_value = [
            date(2021, 1, 1),
            date(2021, 1, 2),
            date(2021, 1, 3),
        ]

        date_list = await schedule_service.get_date_list(
            performance_id=default_performance.id
        )

        assert date_list == [
            date(2021, 1, 1),
            date(2021, 1, 2),
            date(2021, 1, 3),
        ]

    @pytest.mark.asyncio
    async def test_get_time_list_by_date(
        self,
        schedule_service: ScheduleService,
        mocked_performance_repository: Mock,
        mocked_schedule_repository: Mock,
        default_performance: Performance,
    ):
        default_performance.id = uuid.uuid4()

        mocked_performance_repository.find_performance_by_id.return_value = (
            default_performance
        )

        mocked_schedule_repository.get_time_list_by_date.return_value = [
            time(1, 1, 1),
            time(2, 2, 2),
            time(3, 3, 3),
        ]

        time_list = await schedule_service.get_time_list_by_date(
            performance_id=default_performance.id, _date=date(2021, 1, 1)
        )

        assert time_list == [
            time(1, 1, 1),
            time(2, 2, 2),
            time(3, 3, 3),
        ]

    @pytest.mark.asyncio
    async def test_find_schedule_by_date_n_time(
        self,
        schedule_service: ScheduleService,
        mocked_performance_repository: Mock,
        mocked_schedule_repository: Mock,
        default_performance: Performance,
    ):
        default_performance.id = uuid.uuid4()

        mocked_performance_repository.find_performance_by_id.return_value = (
            default_performance
        )

        schedule_id = uuid.uuid4()

        mocked_schedule_repository.find_schedule_by_date_n_time.return_value = Schedule(
            id=schedule_id,
            performance_id=default_performance.id,
            date=date(2021, 1, 1),
            time=time(1, 1, 1),
        )

        schedule = await schedule_service.find_schedule_by_date_n_time(
            performance_id=default_performance.id,
            _date=date(2021, 1, 1),
            _time=time(1, 1, 1),
        )

        assert schedule.id == schedule_id
