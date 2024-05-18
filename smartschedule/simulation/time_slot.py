from datetime import datetime, timedelta
from typing import Self

import pendulum
from attrs import frozen


@frozen
class TimeSlot:
    start: datetime
    end: datetime

    def within(self, other: Self) -> bool:
        return self.start >= other.start and self.end <= other.end

    def duration(self) -> timedelta:
        return self.end - self.start

    @classmethod
    def create_daily_time_slot_at_utc(cls, year: int, month: int, day: int) -> Self:
        instant = datetime(year, month, day)
        return cls(start=instant, end=instant + timedelta(days=1))

    @classmethod
    def create_monthly_time_slot_at_utc(cls, year: int, month: int) -> Self:
        instant = pendulum.datetime(year, month, 1)
        return cls(start=instant, end=instant.add(months=1))
