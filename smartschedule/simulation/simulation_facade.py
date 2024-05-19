from smartschedule.optimization import (
    Item,
    OptimizationFacade,
    Result,
    TotalCapacity,
    TotalWeight,
)
from smartschedule.simulation.simulated_capabilities import SimulatedCapabilities
from smartschedule.simulation.simulated_project import SimulatedProject


class SimulationFacade:
    def __init__(self, optimization_facade: OptimizationFacade) -> None:
        self.optimization_facade = optimization_facade

    def which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        self,
        projects_simulations: list[SimulatedProject],
        total_capability: SimulatedCapabilities,
    ) -> Result:
        items = self._to_items(projects_simulations)
        total_capacity = TotalCapacity(total_capability.capabilities)
        return self.optimization_facade.calculate(items, total_capacity)

    @staticmethod
    def _to_items(projects_simulations: list[SimulatedProject]) -> list[Item]:
        return [
            Item(
                name=str(project.project_id),
                value=float(project.earnings),
                total_weight=TotalWeight(project.missing_demands),
            )
            for project in projects_simulations
        ]
