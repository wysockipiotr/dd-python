from datetime import datetime

import pendulum
import pytest

from smartschedule.shared.time_slot import TimeSlot

pytestmark = pytest.mark.unit


def test_creating_monthly_time_slot_at_utc() -> None:
    january_2023 = TimeSlot.create_monthly_time_slot_at_utc(2023, 1)
    assert january_2023.start == pendulum.datetime(2023, 1, 1)
    assert january_2023.end == pendulum.datetime(2023, 2, 1)


def test_one_slot_within_another() -> None:
    slot_1 = TimeSlot(
        datetime.fromisoformat("2023-01-02T00:00:00Z"),
        datetime.fromisoformat("2023-01-02T23:59:59Z"),
    )
    slot_2 = TimeSlot(
        datetime.fromisoformat("2023-01-01T00:00:00Z"),
        datetime.fromisoformat("2023-01-03T00:00:00Z"),
    )

    assert slot_1.within(slot_2)
    assert not slot_2.within(slot_1)


@pytest.mark.parametrize(
    ("slot_1", "slot_2"),
    [
        (
            TimeSlot(
                datetime.fromisoformat("2023-01-01T00:00:00Z"),
                datetime.fromisoformat("2023-01-02T23:59:59Z"),
            ),
            TimeSlot(
                datetime.fromisoformat("2023-01-02T00:00:00Z"),
                datetime.fromisoformat("2023-01-03T00:00:00Z"),
            ),
        ),
        (
            TimeSlot(
                datetime.fromisoformat("2023-01-02T00:00:00Z"),
                datetime.fromisoformat("2023-01-03T23:59:59Z"),
            ),
            TimeSlot(
                datetime.fromisoformat("2023-01-01T00:00:00Z"),
                datetime.fromisoformat("2023-01-02T23:59:59Z"),
            ),
        ),
    ],
)
def test_one_slot_is_not_within_another_if_they_just_overlap(
    slot_1: TimeSlot, slot_2: TimeSlot
) -> None:
    assert not slot_1.within(slot_2)
    assert not slot_2.within(slot_1)


def test_slot_is_not_within_another_when_they_are_completely_outside() -> None:
    slot_1 = TimeSlot(
        datetime.fromisoformat("2023-01-01T00:00:00Z"),
        datetime.fromisoformat("2023-01-01T23:59:59Z"),
    )
    slot_2 = TimeSlot(
        datetime.fromisoformat("2023-01-02T00:00:00Z"),
        datetime.fromisoformat("2023-01-03T00:00:00Z"),
    )
    assert not slot_1.within(slot_2)


def test_slot_is_not_within_itself() -> None:
    slot_1 = TimeSlot(
        datetime.fromisoformat("2023-01-01T00:00:00Z"),
        datetime.fromisoformat("2023-01-01T23:59:59Z"),
    )
    assert slot_1.within(slot_1)
