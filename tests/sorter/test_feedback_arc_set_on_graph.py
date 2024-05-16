from smartschedule.sorter.feedback_arc_set_on_graph import (
    Edge,
    calculate_feedback_arc_set_on_graph,
)
from smartschedule.sorter.node import Node


def test_can_find_minimum_number_of_edges_to_remove_to_make_the_graph_acyclic() -> None:
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4")
    node1 = node1.depends_on(node2)
    node2 = node2.depends_on(node3)
    node4 = node4.depends_on(node3)
    node1 = node1.depends_on(node4)
    node3 = node3.depends_on(node1)

    to_remove = calculate_feedback_arc_set_on_graph([node1, node2, node3, node4])

    assert set(to_remove) == {Edge(3, 1), Edge(4, 3)}


def test_when_graph_is_acyclic_there_is_nothing_to_remove() -> None:
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4")
    node1 = node1.depends_on(node2)
    node2 = node2.depends_on(node3)
    node1 = node1.depends_on(node4)

    to_remove = calculate_feedback_arc_set_on_graph([node1, node2, node3, node4])

    assert to_remove == []
