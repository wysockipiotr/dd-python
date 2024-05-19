from abc import ABC, abstractmethod

from smartschedule.optimization.capacity_dimension import CapacityDimension


class WeightDimension[T: CapacityDimension](ABC):
    @abstractmethod
    def is_satisfied_by(self, capacity_dimension: T, /) -> bool: ...
