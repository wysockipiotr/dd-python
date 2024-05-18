from attrs import frozen

from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)
from smartschedule.simulation.simulated_project import SimulatedProject


@frozen
class Result:
    profit: int
    chosen_items: list[SimulatedProject]
    item_to_capacities: dict[SimulatedProject, set[AvailableResourceCapability]]

    def __str__(self) -> str:
        return f"Result({self.profit=},{self.chosen_items=})"
