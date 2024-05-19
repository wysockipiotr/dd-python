import pytest

from smartschedule.optimization.item import Item
from smartschedule.optimization.optimization_facade import OptimizationFacade
from smartschedule.optimization.total_capacity import TotalCapacity
from smartschedule.optimization.total_weight import TotalWeight
from smartschedule.shared.time_slot import TimeSlot
from tests.optimization.capability_capacity_dimension import (
    CapabilityTimedCapacityDimension,
    CapabilityTimedWeightDimension,
)


@pytest.fixture()
def optimization_facade() -> OptimizationFacade:
    return OptimizationFacade()


pytestmark = pytest.mark.unit


def test_nothing_is_chosen_when_no_capacities_in_time_slot(
    optimization_facade: OptimizationFacade,
) -> None:
    june = TimeSlot.create_monthly_time_slot_at_utc(2020, 6)
    october = TimeSlot.create_monthly_time_slot_at_utc(2020, 10)
    items = [
        Item(
            "Item1",
            100,
            TotalWeight.of(
                CapabilityTimedWeightDimension("COMMON SENSE", "Skill", june)
            ),
        ),
        Item(
            "Item2",
            100,
            TotalWeight.of(CapabilityTimedWeightDimension("THINKING", "Skill", june)),
        ),
    ]

    result = optimization_facade.calculate(
        items,
        TotalCapacity.of(
            CapabilityTimedCapacityDimension("anna", "COMMON SENSE", "Skill", october)
        ),
    )

    assert result.profit == 0
    assert len(result.chosen_items) == 0


def test_most_profitable_item_is_chosen(
    optimization_facade: OptimizationFacade,
) -> None:
    june = TimeSlot.create_monthly_time_slot_at_utc(2020, 6)

    items = [
        Item(
            "Item1",
            200,
            TotalWeight.of(
                CapabilityTimedWeightDimension("COMMON SENSE", "Skill", june)
            ),
        ),
        Item(
            "Item2",
            100,
            TotalWeight.of(CapabilityTimedWeightDimension("THINKING", "Skill", june)),
        ),
    ]

    result = optimization_facade.calculate(
        items,
        TotalCapacity.of(
            CapabilityTimedCapacityDimension("anna", "COMMON SENSE", "Skill", june)
        ),
    )

    assert result.profit == 200
    assert len(result.chosen_items) == 1
