from attrs import frozen

from smartschedule.planning.parallelization.stage import Stage


@frozen
class ParallelStages:
    stages: set[Stage]

    def __str__(self) -> str:
        return ", ".join(sorted(stage.name for stage in self.stages))
