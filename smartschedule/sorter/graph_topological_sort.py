from graphlib import CycleError, TopologicalSorter

from smartschedule.sorter.nodes import Nodes
from smartschedule.sorter.sorted_nodes import SortedNodes


def graph_topological_sort[T](nodes: Nodes[T]) -> SortedNodes[T]:
    sorted_nodes = SortedNodes.empty()

    sorter = TopologicalSorter(graph={node: node.dependencies for node in nodes})

    try:
        sorter.prepare()
    except CycleError:
        return sorted_nodes

    while sorter.is_active():
        group = sorter.get_ready()
        sorted_nodes = sorted_nodes.add(Nodes(group))
        sorter.done(*group)

    return sorted_nodes
