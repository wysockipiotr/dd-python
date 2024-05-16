from collections import defaultdict

from attrs import frozen

from smartschedule.sorter.node import Node

type AdjacencyList = defaultdict[int, list[int]]


@frozen
class Edge:
    source: int
    target: int

    def __str__(self) -> str:
        return f"({self.source} -> {self.target})"


def calculate_feedback_arc_set_on_graph(initial_nodes: list[Node[str]]) -> list[Edge]:
    adjacency_list = _create_adjacency_list(initial_nodes)
    feedback_edges: list[Edge] = []
    visited: list[int] = [0] * (len(adjacency_list) + 1)

    for i in adjacency_list:
        neighbours = adjacency_list[i]
        visited[i] = 1
        for neighbour in neighbours:
            if visited[neighbour] == 1:
                feedback_edges.append(Edge(i, neighbour))
            else:
                visited[neighbour] = 1

    return feedback_edges


def _create_adjacency_list(initial_nodes: list[Node[str]]) -> AdjacencyList:
    adjacency_list: AdjacencyList = defaultdict(list)

    for i, node in enumerate(initial_nodes):
        dependencies = [
            initial_nodes.index(dependency) + 1 for dependency in node.dependencies
        ]
        adjacency_list[i + 1] = dependencies

    return adjacency_list
