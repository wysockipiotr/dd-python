import pytest

from smartschedule.optimization.item import Item
from smartschedule.optimization.optimization_facade import OptimizationFacade
from smartschedule.optimization.total_capacity import TotalCapacity
from smartschedule.optimization.total_weight import TotalWeight
from tests.optimization.capability_capacity_dimension import (
    CapabilityCapacityDimension,
    CapabilityWeightDimension,
)


@pytest.fixture()
def optimization_facade() -> OptimizationFacade:
    return OptimizationFacade()


pytestmark = pytest.mark.unit


def test_nothing_is_chosen_when_no_capacities(
    optimization_facade: OptimizationFacade,
) -> None:
    items = [
        Item(
            "Item1",
            100,
            TotalWeight.of(CapabilityWeightDimension("COMMON SENSE", "Skill")),
        ),
        Item(
            "Item2",
            100,
            TotalWeight.of(CapabilityWeightDimension("THINKING", "Skill")),
        ),
    ]
    result = optimization_facade.calculate(items, TotalCapacity.zero())
    assert result.profit == 0
    assert len(result.chosen_items) == 0


def test_everything_is_chosen_when_all_weights_are_zero(
    optimization_facade: OptimizationFacade,
) -> None:
    items = [
        Item(
            "Item1",
            200,
            TotalWeight.zero(),
        ),
        Item(
            "Item2",
            100,
            TotalWeight.zero(),
        ),
    ]
    result = optimization_facade.calculate(items, TotalCapacity.zero())
    assert result.profit == 300
    assert len(result.chosen_items) == 2


def test_if_enough_capacity_all_items_are_chosen(
    optimization_facade: OptimizationFacade,
) -> None:
    items = [
        Item(
            "Item1",
            100,
            TotalWeight.of(CapabilityWeightDimension("WEB DEVELOPMENT", "Skill")),
        ),
        Item(
            "Item2",
            300,
            TotalWeight.of(CapabilityWeightDimension("WEB DEVELOPMENT", "Skill")),
        ),
    ]
    c_1 = CapabilityCapacityDimension("anna", "WEB DEVELOPMENT", "Skill")
    c_2 = CapabilityCapacityDimension("zbyniu", "WEB DEVELOPMENT", "Skill")

    result = optimization_facade.calculate(items, TotalCapacity.of(c_1, c_2))

    assert result.profit == 400
    assert len(result.chosen_items) == 2


def test_most_valuable_items_are_chosen(
    optimization_facade: OptimizationFacade,
) -> None:
    item_1 = Item(
        "Item1",
        100,
        TotalWeight.of(CapabilityWeightDimension("JAVA", "Skill")),
    )
    item_2 = Item(
        "Item2",
        500,
        TotalWeight.of(CapabilityWeightDimension("JAVA", "Skill")),
    )
    item_3 = Item(
        "Item3",
        300,
        TotalWeight.of(CapabilityWeightDimension("JAVA", "Skill")),
    )
    c_1 = CapabilityCapacityDimension("anna", "JAVA", "Skill")
    c_2 = CapabilityCapacityDimension("zbyniu", "JAVA", "Skill")

    result = optimization_facade.calculate(
        [item_1, item_2, item_3], TotalCapacity.of(c_1, c_2)
    )

    assert result.profit == 800
    assert len(result.chosen_items) == 2

    assert len(result.item_to_capacities[item_3]) == 1
    assert {c_1, c_2} & result.item_to_capacities[item_3]

    assert len(result.item_to_capacities[item_2]) == 1
    assert {c_1, c_2} & result.item_to_capacities[item_2]

    assert item_1 not in result.item_to_capacities
