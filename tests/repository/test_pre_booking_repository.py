import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.area import Area
from src.models.model import Performance, Schedule, SeatGrade, User
from src.models.pre_booking import PreBooking
from src.models.seat import Seat
from src.repositories.area import AreaRepository
from src.repositories.pre_booking import PreBookingRepository
from src.repositories.schedule import ScheduleRepository
from src.repositories.seat import SeatRepository
from src.repositories.seat_grade import SeatGradeRepository
from tests.repository.fixture import (
    area_repository,
    default_performance,
    default_user,
    pre_booking_repository,
    schedule_repository,
    seat_repository,
)

__all__ = [
    "default_performance",
    "pre_booking_repository",
    "default_user",
    "schedule_repository",
    "area_repository",
    "seat_repository",
]


async def new_pre_booking(session: AsyncSession, performance: Performance, user: User):
    new_schedule = (
        await ScheduleRepository(session=session).save_schedule_list(
            [
                Schedule.create(
                    performance_id=performance.id,
                    date=datetime.date.today(),
                    time=datetime.time(hour=12, minute=30),
                )
            ]
        )
    )[0]

    new_seat_grade = await SeatGradeRepository(session=session).save_seat_grade(
        SeatGrade.create(
            performance_id=performance.id,
            name="test",
            price=10000,
        )
    )

    new_area = await AreaRepository(session=session).save_area(
        Area.create(
            performance_id=performance.id,
            title="test",
            accessible_seats_info="test",
        )
    )

    new_seat_a = await SeatRepository(session=session).save_seat(
        Seat.create(
            area_id=new_area.id,
            x=1.0,
            y=1.0,
            row=1,
            col=1,
            name="A1",
            seat_grade_id=new_seat_grade.id,
            is_accessible=True,
            distance_from_stage=50,
        )
    )

    new_seat_b = await SeatRepository(session=session).save_seat(
        Seat.create(
            area_id=new_area.id,
            x=2.0,
            y=2.0,
            row=2,
            col=2,
            name="B1",
            seat_grade_id=new_seat_grade.id,
            is_accessible=True,
            distance_from_stage=50,
        )
    )

    pre_booking = PreBooking.create(
        user_id=user.id,
        performance_id=performance.id,
        schedule_id=new_schedule.id,
    )

    pre_booking.seats = [new_seat_a, new_seat_b]

    return pre_booking


class TestPreBookingRepository:
    @pytest.mark.asyncio
    async def test_save_pre_booking(
        self,
        session: AsyncSession,
        pre_booking_repository: PreBookingRepository,
        default_performance: Performance,
        default_user: User,
    ):
        pre_booking = await new_pre_booking(
            session=session,
            performance=default_performance,
            user=default_user,
        )

        pre_booking = await pre_booking_repository.save_pre_booking(
            pre_booking=pre_booking
        )

        assert pre_booking is not None

    @pytest.mark.asyncio
    async def test_get_pre_booking_list_by_user_id(
        self,
        pre_booking_repository: PreBookingRepository,
        default_performance: Performance,
        default_user: User,
    ):
        pre_booking = await new_pre_booking(
            session=pre_booking_repository.session,
            performance=default_performance,
            user=default_user,
        )

        await pre_booking_repository.save_pre_booking(pre_booking=pre_booking)

        pre_bookings = await pre_booking_repository.get_pre_booking_list(
            user_id=default_user.id,
            limit=20,
        )

        assert len(pre_bookings) != 0
