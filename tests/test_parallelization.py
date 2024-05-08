from smartschedule.parallelization.stage import Stage
from smartschedule.parallelization.stage_parallelization import StageParallelization


def test_everything_can_be_done_in_parallel_when_there_are_no_deps() -> None:
    stage_1 = Stage("stage_1")
    stage_2 = Stage("stage_2")

    sorted_stages = StageParallelization.of({stage_1, stage_2})

    assert len(sorted_stages.all) == 1


def test_simple_deps() -> None:
    stage_1 = Stage("stage_1")
    stage_2 = Stage("stage_2")
    stage_3 = Stage("stage_3")
    stage_4 = Stage("stage_4")
    stage_2.depends_on(stage_1)
    stage_3.depends_on(stage_1)
    stage_4.depends_on(stage_2)

    sorted_stages = StageParallelization.of({stage_1, stage_2, stage_3, stage_4})

    assert str(sorted_stages) == "stage_1 | stage_2, stage_3 | stage_4"


def test_cannot_be_done_when_there_is_a_cycle() -> None:
    stage_1 = Stage("stage_1")
    stage_2 = Stage("stage_2")
    stage_2.depends_on(stage_1)
    stage_1.depends_on(stage_2)  # making it cyclic

    sorted_stages = StageParallelization.of({stage_1, stage_2})

    assert len(sorted_stages.all) == 0
