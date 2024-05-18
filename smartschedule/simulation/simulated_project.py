from attrs import frozen

from smartschedule.simulation.demands import Demands
from smartschedule.simulation.project_id import ProjectId


@frozen
class SimulatedProject:
    project_id: ProjectId
    earnings: int
    missing_demands: Demands

    def all_demands_satisfied(self) -> bool:
        return not self.missing_demands
