import pytest

from src.models.model import Performance, PerformanceContent
from tests.fixture.performance import default_performance

__all__ = ("default_performance",)


@pytest.fixture
def default_performance_content(default_performance: Performance) -> PerformanceContent:
    return PerformanceContent.create(
        performance_id=default_performance.id,
        notice="공지사항",
        introduction=None,
    )
