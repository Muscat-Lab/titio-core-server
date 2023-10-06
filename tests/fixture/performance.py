import datetime

import pytest

from src.models.model import Performance


@pytest.fixture
def default_performance() -> Performance:
    return Performance.create(
        title="test",
        running_time="150분",
        grade="전체 관람가",
        begin=datetime.date.today(),
        end=datetime.date.today(),
        pre_booking_enabled=True,
        pre_booking_closed_at=datetime.datetime.now(),
    )
