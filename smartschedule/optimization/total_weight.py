from typing import Self

from attrs import frozen

from smartschedule.optimization.weight_dimension import WeightDimension


@frozen
class TotalWeight:
    _components: tuple[WeightDimension, ...]

    @classmethod
    def zero(cls) -> Self:
        return cls(tuple())

    @classmethod
    def of(cls, *components: WeightDimension) -> Self:
        return cls(tuple(components))

    def components(self) -> tuple[WeightDimension, ...]:
        return self._components[:]
