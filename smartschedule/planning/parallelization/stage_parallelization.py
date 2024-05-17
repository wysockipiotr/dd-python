from smartschedule.planning.parallelization.sorted_nodes_to_parallelized_stages import (
    sorted_nodes_to_parallelized_stages,
)
from smartschedule.planning.parallelization.stages_to_nodes import stages_to_nodes
from smartschedule.sorter import graph_topological_sort
from smartschedule.utils.pipe import pipe

stage_parallelization_of = pipe(
    stages_to_nodes,
    graph_topological_sort,
    sorted_nodes_to_parallelized_stages,
)
