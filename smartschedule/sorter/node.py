from itertools import chain
from typing import Self

from attrs import field, frozen


@frozen
class Node[T]:
    name: str
    dependencies: set["Node[T]"] = field(factory=set, eq=False)
    content: T | None = field(eq=False, default=None)

    def depends_on(self, node: Self) -> "Node[T]":
        return Node(self.name, set(chain(self.dependencies, {node})), self.content)

    def __str__(self) -> str:
        return self.name
