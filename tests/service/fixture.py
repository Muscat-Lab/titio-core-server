from unittest.mock import Mock

import pytest

from src.repositories.performance import PerformanceRepository
from src.repositories.user import UserRepository


@pytest.fixture()
def mocked_performance_repository():
    return Mock(spec=PerformanceRepository)


@pytest.fixture()
def mocked_user_repository():
    return Mock(spec=UserRepository)
