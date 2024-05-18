from attrs import frozen

from smartschedule.simulation.demand import Demand
from smartschedule.simulation.project_id import ProjectId


@frozen
class SimulatedProject:
    project_id: ProjectId
    earnings: int
    missing_demands: list[Demand]
