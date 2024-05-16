from collections.abc import Collection
from itertools import islice

from smartschedule.planning.parallelization.stage import Stage
from smartschedule.sorter import Node, Nodes

type StageName = str
type NodesByName = dict[StageName, Node[Stage]]


def stages_to_nodes(stages: Collection[Stage]) -> Nodes[Stage]:
    nodes = {stage.name: Node(name=stage.name, content=stage) for stage in stages}

    for n, stage in enumerate(stages):
        _explicit_dependencies(stage, nodes)
        _shared_resources(stage, list(islice(stages, n + 1, None)), nodes)

    return Nodes(nodes.values())


def _explicit_dependencies(stage: Stage, nodes: NodesByName) -> NodesByName:
    for other in stage.dependencies:
        nodes[stage.name] = nodes[stage.name].depends_on(nodes[other.name])

    return nodes


def _shared_resources(
    stage: Stage, with_stages: Collection[Stage], nodes: NodesByName
) -> NodesByName:
    for other in with_stages:
        if stage.name == other.name:
            continue

        # No shared resources.
        if stage.resources.isdisjoint(other.resources):
            continue

        if len(other.resources) > len(stage.resources):
            nodes[stage.name] = nodes[stage.name].depends_on(nodes[other.name])
        else:
            nodes[other.name] = nodes[other.name].depends_on(nodes[stage.name])

    return nodes
