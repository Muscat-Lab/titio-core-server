import datetime

import pytest

from src.models.model import Performance, Schedule
from src.repositories.performance import PerformanceRepository
from src.repositories.schedule import ScheduleRepository
from tests.fixture.performance import default_performance

__all__ = ("TestScheduleRepository", "default_performance")


async def generate_schedules(
    schedule_repository: ScheduleRepository,
    default_performance: Performance,
    iso_datetime_list: list[str],
):
    await schedule_repository.save_schedule_list(
        schedule_list=[
            Schedule.create(
                performance_id=default_performance.id,
                date=datetime.date.fromisoformat(iso_datetime.split("T")[0]),
                time=datetime.time.fromisoformat(iso_datetime.split("T")[1]),
            )
            for iso_datetime in iso_datetime_list
        ]
    )


class TestScheduleRepository:
    @pytest.fixture
    def schedule_repository(self, session):
        return ScheduleRepository(session=session)

    @pytest.fixture
    def performance_repository(self, session):
        return PerformanceRepository(session=session)

    @pytest.mark.asyncio
    async def test_find_schedule_by_date_n_time(
        self,
        schedule_repository: ScheduleRepository,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        await generate_schedules(
            schedule_repository=schedule_repository,
            default_performance=await performance_repository.save_performance(
                default_performance
            ),
            iso_datetime_list=[
                "2021-01-01T09:00:00",
                "2021-01-01T10:00:00",
                "2021-01-01T11:00:00",
                "2021-01-02T09:00:00",
                "2021-01-02T10:00:00",
                "2021-01-02T11:00:00",
            ],
        )

        schedule = await schedule_repository.find_schedule_by_date_n_time(
            performance_id=default_performance.id,
            _date=datetime.date.fromisoformat("2021-01-01"),
            _time=datetime.time.fromisoformat("09:00:00"),
        )

        assert schedule is not None

        schedule = await schedule_repository.find_schedule_by_date_n_time(
            performance_id=default_performance.id,
            _date=datetime.date.fromisoformat("2021-01-01"),
            _time=datetime.time.fromisoformat("09:01:00"),
        )

        assert schedule is None

    @pytest.mark.asyncio
    async def test_get_date_list(
        self,
        schedule_repository: ScheduleRepository,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        iso_datetime_list = [  # 2021-01-01 ~ 2021-01-03
            "2021-01-01T09:00:00",
            "2021-01-01T10:00:00",
            "2021-01-01T11:00:00",
            "2021-01-02T09:00:00",
            "2021-01-02T10:00:00",
            "2021-01-02T11:00:00",
            "2021-01-03T09:00:00",
            "2021-01-03T10:00:00",
            "2021-01-03T11:00:00",
        ]

        await generate_schedules(
            schedule_repository=schedule_repository,
            default_performance=await performance_repository.save_performance(
                default_performance
            ),
            iso_datetime_list=iso_datetime_list,
        )

        date_list = await schedule_repository.get_date_list(
            performance_id=default_performance.id,
        )

        assert date_list == [
            datetime.date.fromisoformat("2021-01-01"),
            datetime.date.fromisoformat("2021-01-02"),
            datetime.date.fromisoformat("2021-01-03"),
        ]

        date_list = await schedule_repository.get_date_list(
            performance_id=default_performance.id,
            from_date=datetime.date.fromisoformat("2021-01-02"),
        )

        assert date_list == [
            datetime.date.fromisoformat("2021-01-02"),
            datetime.date.fromisoformat("2021-01-03"),
        ]

        date_list = await schedule_repository.get_date_list(
            performance_id=default_performance.id,
            to_date=datetime.date.fromisoformat("2021-01-02"),
        )

        assert date_list == [
            datetime.date.fromisoformat("2021-01-01"),
            datetime.date.fromisoformat("2021-01-02"),
        ]

        date_list = await schedule_repository.get_date_list(
            performance_id=default_performance.id,
            from_date=datetime.date.fromisoformat("2021-01-02"),
            to_date=datetime.date.fromisoformat("2021-01-02"),
        )

        assert date_list == [
            datetime.date.fromisoformat("2021-01-02"),
        ]

        date_list = await schedule_repository.get_date_list(
            performance_id=default_performance.id,
            cursor="2021-01-01",
            limit=1,
        )

        assert date_list == [
            datetime.date.fromisoformat("2021-01-02"),
        ]

        date_list = await schedule_repository.get_date_list(
            performance_id=default_performance.id,
            cursor="2021-01-01",
            limit=2,
        )

        assert date_list == [
            datetime.date.fromisoformat("2021-01-02"),
            datetime.date.fromisoformat("2021-01-03"),
        ]

    @pytest.mark.asyncio
    async def test_get_time_list_by_date(
        self,
        schedule_repository: ScheduleRepository,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        iso_datetime_list = [  # 09:00:00 ~ 11:00:00
            "2021-01-01T09:00:00",
            "2021-01-01T10:00:00",
            "2021-01-01T11:00:00",
            "2021-01-02T09:10:00",
            "2021-01-02T10:10:00",
            "2021-01-02T11:10:00",
            "2021-01-03T09:20:00",
            "2021-01-03T10:20:00",
            "2021-01-03T11:20:00",
        ]

        await generate_schedules(
            schedule_repository=schedule_repository,
            default_performance=await performance_repository.save_performance(
                default_performance
            ),
            iso_datetime_list=iso_datetime_list,
        )

        time_list = await schedule_repository.get_time_list_by_date(
            performance_id=default_performance.id,
            _date=datetime.date.fromisoformat("2021-01-01"),
        )

        assert time_list == [
            datetime.time.fromisoformat("09:00:00"),
            datetime.time.fromisoformat("10:00:00"),
            datetime.time.fromisoformat("11:00:00"),
        ]

        time_list = await schedule_repository.get_time_list_by_date(
            performance_id=default_performance.id,
            _date=datetime.date.fromisoformat("2021-01-01"),
            from_time=datetime.time.fromisoformat("10:00:00"),
        )

        assert time_list == [
            datetime.time.fromisoformat("10:00:00"),
            datetime.time.fromisoformat("11:00:00"),
        ]

        time_list = await schedule_repository.get_time_list_by_date(
            performance_id=default_performance.id,
            _date=datetime.date.fromisoformat("2021-01-01"),
            to_time=datetime.time.fromisoformat("10:00:00"),
        )

        assert time_list == [
            datetime.time.fromisoformat("09:00:00"),
            datetime.time.fromisoformat("10:00:00"),
        ]

        time_list = await schedule_repository.get_time_list_by_date(
            performance_id=default_performance.id,
            _date=datetime.date.fromisoformat("2021-01-01"),
            from_time=datetime.time.fromisoformat("10:00:00"),
            to_time=datetime.time.fromisoformat("10:00:00"),
        )

        assert time_list == [
            datetime.time.fromisoformat("10:00:00"),
        ]

        time_list = await schedule_repository.get_time_list_by_date(
            performance_id=default_performance.id,
            _date=datetime.date.fromisoformat("2021-01-01"),
            cursor="09:00:00",
            limit=1,
        )

        assert time_list == [
            datetime.time.fromisoformat("10:00:00"),
        ]

        time_list = await schedule_repository.get_time_list_by_date(
            performance_id=default_performance.id,
            _date=datetime.date.fromisoformat("2021-01-01"),
            cursor="09:00:00",
            limit=2,
        )

        assert time_list == [
            datetime.time.fromisoformat("10:00:00"),
            datetime.time.fromisoformat("11:00:00"),
        ]
