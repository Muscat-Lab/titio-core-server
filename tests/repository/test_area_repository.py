import random

import pytest

from src.models.model import SeatGrade
from src.models.seat import Seat
from src.repositories.area import AreaRepository
from src.repositories.performance import PerformanceRepository
from src.repositories.seat import SeatRepository
from src.repositories.seat_grade import SeatGradeRepository
from tests.repository.fixture import (
    area_repository,
    new_area,
    new_performance,
    performance_repository,
    seat_grade_repository,
    seat_repository,
)

__all__ = [
    "area_repository",
    "performance_repository",
    "seat_repository",
    "seat_grade_repository",
]


class TestAreaRepository:
    @pytest.mark.asyncio
    async def test_get_area_list(
        self,
        performance_repository: PerformanceRepository,
        area_repository: AreaRepository,
        seat_repository: SeatRepository,
        seat_grade_repository: SeatGradeRepository,
    ):
        performance = await new_performance(performance_repository)

        for _ in range(10):
            await new_area(
                area_repository=area_repository,
                performance_id=performance.id,
            )

        areas = await area_repository.get_area_list(
            performance_id=performance.id,
            limit=20,
        )

        assert len(areas) != 0

        seat_grade = await seat_grade_repository.save_seat_grade(
            SeatGrade.create(
                performance_id=performance.id,
                name="test",
                price=10000,
            )
        )

        areas = await area_repository.get_area_list(
            performance_id=performance.id,
            limit=20,
        )

        accessible_seat_count = 0

        for area in areas:
            i = random.randint(1, 10)

            for _ in range(i):
                await seat_repository.save_seat(
                    Seat.create(
                        area_id=area.id,
                        row=1,
                        col=1,
                        x=1,
                        y=1,
                        name="test",
                        seat_grade_id=seat_grade.id,
                        is_accessible=True,
                    )
                )

                accessible_seat_count += 1

        areas = await area_repository.get_area_list(
            performance_id=performance.id,
            limit=20,
        )

        assert len(areas) != 0

        assert (
            sum([area.accessible_seats_count for area in areas])
            == accessible_seat_count
        )
