from typing import Self, cast

from attrs import field, mutable

from smartschedule.simulation.demand import Demand
from smartschedule.simulation.project_id import ProjectId
from smartschedule.simulation.simulated_project import SimulatedProject


@mutable
class SimulatedProjectsBuilder:
    _current_id: ProjectId | None = None
    _simulated_projects: list[ProjectId] = field(factory=list)
    _simulated_demands: dict[ProjectId, list[Demand]] = field(factory=dict)
    _simulated_earnings: dict[ProjectId, int] = field(factory=dict)

    def with_project(self, project_id: ProjectId) -> Self:
        self._current_id = project_id
        self._simulated_projects.append(project_id)
        return self

    def that_requires(self, *demands: Demand) -> Self:
        self._simulated_demands[cast(ProjectId, self._current_id)] = list(demands)
        return self

    def that_can_earn(self, earnings: int) -> Self:
        self._simulated_earnings[cast(ProjectId, self._current_id)] = earnings
        return self

    def build(self) -> list[SimulatedProject]:
        return [
            SimulatedProject(
                project_id=project_id,
                missing_demands=self._simulated_demands[project_id],
                earnings=self._simulated_earnings[project_id],
            )
            for project_id in self._simulated_projects
        ]
