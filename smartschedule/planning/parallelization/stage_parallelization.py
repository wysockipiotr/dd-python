from smartschedule.planning.parallelization.parallel_stages_list import (
    ParallelStagesList,
)
from smartschedule.planning.parallelization.sorted_nodes_to_parallelized_stages import (
    sorted_nodes_to_parallelized_stages,
)
from smartschedule.planning.parallelization.stage import Stage
from smartschedule.planning.parallelization.stages_to_nodes import stages_to_nodes
from smartschedule.sorter import graph_topological_sort


def stage_parallelization_of(stages: set[Stage]) -> ParallelStagesList:
    nodes = stages_to_nodes(stages)
    sorted_nodes = graph_topological_sort(nodes)
    return sorted_nodes_to_parallelized_stages(sorted_nodes)
