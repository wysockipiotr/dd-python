from attrs import field, frozen

from smartschedule.planning.parallelization.parallel_stages import ParallelStages


@frozen
class ParallelStagesList:
    all: list[ParallelStages] = field(factory=list)

    def __str__(self) -> str:
        return " | ".join(str(parallel_stages) for parallel_stages in self.all)

    def add(self, new_parallel_stages: ParallelStages) -> "ParallelStagesList":
        result = [*self.all, new_parallel_stages]
        return ParallelStagesList(all=result)
