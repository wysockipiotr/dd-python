from collections.abc import Collection
from typing import Self

from smartschedule.optimization.capacity_dimension import CapacityDimension


class TotalCapacity:
    def __init__(self, capacities: Collection[CapacityDimension]):
        self._capacities = tuple(capacities)

    @classmethod
    def zero(cls) -> Self:
        return cls(tuple())

    @classmethod
    def of(cls, *capacities: CapacityDimension) -> Self:
        return cls(tuple(capacities))

    def capacities(self) -> tuple[CapacityDimension, ...]:
        return self._capacities[:]

    def __len__(self) -> int:
        return len(self._capacities)
