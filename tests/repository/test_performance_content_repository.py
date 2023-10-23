import pytest

from src.models.model import Performance, PerformanceContent
from src.repositories.performance import PerformanceRepository
from src.repositories.performance_content import PerformanceContentRepository
from tests.fixture.performance import default_performance

__all__ = (
    "TestPerformanceContentRepository",
    "default_performance",
)


@pytest.fixture
def performance_content_repository(session):
    return PerformanceContentRepository(session=session)


@pytest.fixture
def performance_repository(session):
    return PerformanceRepository(session=session)


class TestPerformanceContentRepository:
    @pytest.mark.asyncio
    async def test_save_performance_content(
        self,
        performance_content_repository: PerformanceContentRepository,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        # default performance
        performance = await performance_repository.save_performance(default_performance)

        assert performance is not None

        performance_content = (
            await performance_content_repository.save_performance_content(
                performance_content=PerformanceContent.create(
                    performance_id=performance.id,
                    notice="공지사항",
                    introduction=None,
                )
            )
        )

        assert performance_content.id is not None

    @pytest.mark.asyncio
    async def test_get_performance_content_list(
        self,
        performance_content_repository: PerformanceContentRepository,
        performance_repository: PerformanceRepository,
        default_performance: Performance,
    ):
        # default performance
        performance = await performance_repository.save_performance(default_performance)

        assert performance is not None

        performance_content = (
            await performance_content_repository.save_performance_content(
                performance_content=PerformanceContent.create(
                    performance_id=performance.id,
                    notice="공지사항",
                    introduction=None,
                )
            )
        )

        assert performance_content.id is not None

        performance_id = performance.id

        performance_content = (
            await performance_content_repository.get_performance_content(
                performance_id=performance_id
            )
        )

        assert performance_content is not None
