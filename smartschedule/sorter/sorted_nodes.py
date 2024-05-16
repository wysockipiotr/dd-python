from typing import Self

from attrs import evolve, field, frozen

from smartschedule.sorter.nodes import Nodes


@frozen
class SortedNodes[T]:
    _groups: list[Nodes[T]] = field(converter=lambda x: list(x))

    def add(self, nodes: Nodes[T], /) -> Self:
        return evolve(self, groups=[*self._groups, nodes])

    def __iter__(self):
        return iter(self._groups)

    def __len__(self) -> int:
        return len(self._groups)

    def __getitem__(self, item):
        return self._groups[item]

    @classmethod
    def empty(cls) -> Self:
        return cls([])
