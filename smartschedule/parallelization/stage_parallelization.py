from graphlib import TopologicalSorter, CycleError

from smartschedule.parallelization.parallel_stages import ParallelStages
from smartschedule.parallelization.parallel_stages_list import ParallelStagesList
from smartschedule.parallelization.stage import Stage


class StageParallelization:
    @staticmethod
    def of(stages: set[Stage]) -> ParallelStagesList:
        parallel_stages_list = ParallelStagesList()
        sorter = TopologicalSorter(
            graph={stage: stage.dependencies for stage in stages}
        )

        try:
            sorter.prepare()
        except CycleError:
            return parallel_stages_list

        while sorter.is_active():
            group = sorter.get_ready()
            parallel_stages = ParallelStages(set(group))
            parallel_stages_list = parallel_stages_list.add(parallel_stages)
            sorter.done(*group)

        return parallel_stages_list
