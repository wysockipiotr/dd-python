from smartschedule.sorter.graph_topological_sort import graph_topological_sort
from smartschedule.sorter.node import Node
from smartschedule.sorter.nodes import Nodes


def test_topological_sort_with_simple_dependencies() -> None:
    node_1 = Node("Node1")
    node_2 = Node("Node2")
    node_3 = Node("Node3")
    node_4 = Node("Node4")

    node_2 = node_2.depends_on(node_1)
    node_3 = node_3.depends_on(node_1)
    node_4 = node_4.depends_on(node_2)

    nodes = Nodes([node_1, node_2, node_3, node_4])

    sorted_nodes = graph_topological_sort(nodes)

    assert len(sorted_nodes) == 3

    assert node_1 in sorted_nodes[0]
    assert node_2 in sorted_nodes[1]
    assert node_3 in sorted_nodes[1]
    assert node_4 in sorted_nodes[2]


def test_topological_sort_with_linear_dependencies() -> None:
    node_1 = Node("Node1")
    node_2 = Node("Node2")
    node_3 = Node("Node3")
    node_4 = Node("Node4")
    node_5 = Node("Node5")

    node_2 = node_2.depends_on(node_1)
    node_3 = node_3.depends_on(node_2)
    node_4 = node_4.depends_on(node_3)
    node_5 = node_5.depends_on(node_4)

    nodes = Nodes([node_1, node_2, node_3, node_4, node_5])

    sorted_nodes = graph_topological_sort(nodes)

    assert len(sorted_nodes) == 5

    assert node_5 in sorted_nodes[4]
    assert len(sorted_nodes[4]) == 1

    assert node_4 in sorted_nodes[3]
    assert len(sorted_nodes[3]) == 1

    assert node_3 in sorted_nodes[2]
    assert len(sorted_nodes[2]) == 1

    assert node_2 in sorted_nodes[1]
    assert len(sorted_nodes[1]) == 1

    assert node_1 in sorted_nodes[0]
    assert len(sorted_nodes[0]) == 1


def test_nodes_without_dependencies() -> None:
    node_1 = Node("Node1")
    node_2 = Node("Node2")

    nodes = Nodes([node_1, node_2])

    sorted_nodes = graph_topological_sort(nodes)

    assert len(sorted_nodes) == 1


def test_cyclic_dependency() -> None:
    node_1 = Node("Node1")
    node_2 = Node("Node2")

    node_2 = node_2.depends_on(node_1)
    node_1 = node_1.depends_on(node_2)

    nodes = Nodes([node_1, node_2])

    sorted_nodes = graph_topological_sort(nodes)

    assert len(sorted_nodes) == 0
