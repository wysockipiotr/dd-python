import pytest

from smartschedule.planning import ResourceName, Stage, stage_parallelization_of

pytestmark = pytest.mark.unit

LEON = ResourceName("Leon")
SLAWEK = ResourceName("Sławek")
ERYK = ResourceName("Eric")
KUBA = ResourceName("Kuba")


def test_everything_can_be_done_in_parallel_when_there_are_no_deps() -> None:
    stage_1 = Stage("stage_1")
    stage_2 = Stage("stage_2")

    sorted_stages = stage_parallelization_of({stage_1, stage_2})

    assert len(sorted_stages.all) == 1


def test_simple_deps() -> None:
    stage_1 = Stage("stage_1")
    stage_2 = Stage("stage_2")
    stage_3 = Stage("stage_3")
    stage_4 = Stage("stage_4")
    stage_2 = stage_2.depends_on(stage_1)
    stage_3 = stage_3.depends_on(stage_1)
    stage_4 = stage_4.depends_on(stage_2)

    sorted_stages = stage_parallelization_of({stage_1, stage_2, stage_3, stage_4})

    assert str(sorted_stages) == "stage_1 | stage_2, stage_3 | stage_4"


def test_cannot_be_done_when_there_is_a_cycle() -> None:
    stage_1 = Stage("stage_1")
    stage_2 = Stage("stage_2")
    stage_2 = stage_2.depends_on(stage_1)
    stage_1 = stage_1.depends_on(stage_2)  # making it cyclic

    sorted_stages = stage_parallelization_of({stage_1, stage_2})

    assert len(sorted_stages.all) == 0


def test_takes_into_account_shared_resources() -> None:
    stage_1 = Stage("stage_1").with_chosen_resource_capabilities(LEON)
    stage_2 = Stage("stage_2").with_chosen_resource_capabilities(ERYK, LEON)
    stage_3 = Stage("stage_3").with_chosen_resource_capabilities(SLAWEK)
    stage_4 = Stage("stage_4").with_chosen_resource_capabilities(SLAWEK, KUBA)

    parallel_stages = stage_parallelization_of({stage_1, stage_2, stage_3, stage_4})

    assert str(parallel_stages) in [
        "stage_1, stage_3 | stage_2, stage_4",
        "stage_2, stage_4 | stage_1, stage_3",
    ]
