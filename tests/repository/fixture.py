import datetime
from uuid import UUID

import pytest
import pytest_asyncio

from src.models.model import Area, Performance, User
from src.repositories.area import AreaRepository
from src.repositories.performance import PerformanceRepository
from src.repositories.performer import PerformerRepository
from src.repositories.pre_booking import PreBookingRepository
from src.repositories.schedule import ScheduleRepository
from src.repositories.seat import SeatRepository
from src.repositories.seat_grade import SeatGradeRepository
from src.repositories.user import UserRepository
from tests.test_utils import generate_random_email


@pytest.fixture
def performance_repository(session):
    return PerformanceRepository(session=session)


@pytest.fixture
def user_repository(session):
    return UserRepository(session=session)


@pytest.fixture
def performer_repository(session):
    return PerformerRepository(session=session)


@pytest.fixture
def schedule_repository(session):
    return ScheduleRepository(session=session)


@pytest.fixture
def seat_repository(session):
    return SeatRepository(session=session)


@pytest.fixture
def seat_grade_repository(session):
    return SeatGradeRepository(session=session)


@pytest.fixture
def area_repository(session):
    return AreaRepository(session=session)


@pytest.fixture
def pre_booking_repository(session):
    return PreBookingRepository(session=session)


@pytest_asyncio.fixture
async def default_performance(session):
    performance = Performance.create(
        title="performance",
        running_time="150분",
        grade="전체 관람가",
        begin=datetime.date.today(),
        end=datetime.date.today(),
        pre_booking_enabled=True,
        pre_booking_closed_at=datetime.datetime.now(),
        genre_idents=["genre"],
    )

    return await PerformanceRepository(session=session).save_performance(
        performance=performance,
    )


@pytest_asyncio.fixture
async def default_user(session):
    user = User.create(
        email=generate_random_email(),
        password="password",
        username="username",
    )

    return await UserRepository(session=session).save_user(
        user=user,
    )


async def new_performance(performance_repository: PerformanceRepository):
    return await performance_repository.save_performance(
        Performance.create(
            title="performance",
            running_time="150분",
            grade="전체 관람가",
            begin=datetime.date.today(),
            end=datetime.date.today(),
            pre_booking_enabled=True,
            pre_booking_closed_at=datetime.datetime.now(),
            genre_idents=["genre"],
        )
    )


async def new_user(user_repository: UserRepository):
    return await user_repository.save_user(
        User.create(
            email=generate_random_email(),
            password="password",
            username="username",
        )
    )


async def new_area(area_repository: AreaRepository, performance_id: UUID):
    return await area_repository.save_area(
        Area.create(
            performance_id=performance_id,
            title="area title",
            accessible_seats_info=None,
        )
    )
