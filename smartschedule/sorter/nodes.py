from typing import Collection

from smartschedule.sorter.node import Node


class Nodes[T]:
    def __init__(self, nodes: Collection[Node[T]]) -> None:
        self._nodes = nodes if isinstance(nodes, set) else set(nodes)

    def __iter__(self):
        return iter(self._nodes)

    def __contains__(self, item):
        return item in self._nodes

    def __len__(self):
        return len(self._nodes)
