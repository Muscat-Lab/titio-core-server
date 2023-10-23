import datetime

import pytest

from src.models.model import Performance
from src.repositories.performance import PerformanceRepository
from src.repositories.user import UserRepository
from tests.conftest import session
from tests.fixture.performance import default_performance
from tests.fixture.user import default_user
from tests.repository.fixture import new_user, performance_repository, user_repository

__all__ = (
    "performance_repository",
    "user_repository",
    "TestPerformanceRepository",
    "default_performance",
    "default_user",
    "session",
)


class TestPerformanceRepository:
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
        self,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        performance = await performance_repository.save_performance(default_performance)

        assert performance is not None

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

        second = await performance_repository.save_performance(
            Performance.create(
                title="사전예약 비활성화",
                running_time="150분",
                grade="전체 관람가",
                begin=datetime.datetime.now(),
                end=datetime.datetime.now(),
                pre_booking_enabled=False,
                pre_booking_closed_at=None,
                genre_idents=["test"],
            )
        )

        performances = await performance_repository.get_performance_list(
            limit=20, pre_booking_enabled=True
        )

        assert len(performances) != 0
        for performance in performances:
            assert performance.pre_booking_enabled is True

        performances = await performance_repository.get_performance_list(
            limit=20, pre_booking_enabled=False
        )

        assert len(performances) != 0
        for performance in performances:
            assert performance.pre_booking_enabled is False

        performances = await performance_repository.get_performance_list(
            limit=20, pre_booking_enabled=False, genre_ident="test"
        )

        assert len(performances) != 0
        for performance in performances:
            assert performance.genre_idents == ["test"]

        performances = await performance_repository.get_performance_list(
            limit=1, cursor=str(second.snowflake_id)
        )

        assert len(performances) != 0
        for performance in performances:
            assert performance.created_at < second.created_at

    @pytest.mark.asyncio
    async def test_get_performance_list_by_ids(
        self,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        performance = await performance_repository.save_performance(default_performance)

        assert performance is not None

        performances = await performance_repository.get_performance_list_by_ids(
            performance_ids=[performance.id]
        )

        assert len(performances) != 0

    @pytest.mark.asyncio
    async def test_get_like_list_by_user_id(
        self,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
        user_repository: UserRepository,
    ):
        _performance = await performance_repository.save_performance(
            default_performance
        )

        assert _performance is not None

        user = await new_user(user_repository)

        performance = await performance_repository.find_performance_by_id(
            performance_id=_performance.id
        )

        performance.like_users.append(user)

        await performance_repository.save_performance(performance)

        like_list = await performance_repository.get_like_list_by_user_id(
            user_id=user.id, performance_ids=[performance.id]
        )

        assert len(like_list) != 0

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

    @pytest.mark.asyncio
    async def test_like_performance(
        self,
        user_repository: UserRepository,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        user = await new_user(user_repository)

        default_performance.like_users.append(user)

        await performance_repository.save_performance(default_performance)

        performance = await performance_repository.find_performance_by_id(
            default_performance.id
        )

        if performance is None:
            raise AssertionError

        assert performance.like_users[0].id == user.id

        performance.like_users.remove(user)

        await performance_repository.save_performance(performance)

        performance = await performance_repository.find_performance_by_id(
            default_performance.id
        )

        if performance is None:
            raise AssertionError

        assert len(performance.like_users) == 0

    @pytest.mark.asyncio
    async def test_hot_performance(
        self,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        performance = await performance_repository.save_performance(default_performance)

        assert performance is not None

        await performance_repository.create_hot_performance(performance.id)

        hot_performances = await performance_repository.get_hot_performance_list()

        assert performance.id == hot_performances[0].performance_id

        await performance_repository.delete_hot_performance(performance.id)

        hot_performances = await performance_repository.get_hot_performance_list()

        assert len(hot_performances) == 0
