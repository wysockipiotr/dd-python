from smartschedule.parallelization.parallel_stages_list import ParallelStagesList
from smartschedule.parallelization.stage import Stage


class StageParallelization:
    @staticmethod
    def of(stages: set[Stage]) -> ParallelStagesList:
        return ParallelStagesList()
