from datetime import timedelta
from typing import Self

from attrs import evolve, field, frozen


@frozen
class ResourceName:
    name: str


@frozen
class Stage:
    name: str
    dependencies: set["Stage"] = field(factory=set, eq=False)
    resources: set[ResourceName] = field(factory=set, eq=False)
    duration: timedelta = field(default=timedelta.min, eq=False)

    def depends_on(self, stage: Self) -> Self:
        return evolve(self, dependencies={*self.dependencies, stage})

    def with_chosen_resource_capabilities(self, *resources: ResourceName) -> Self:
        return evolve(self, resources={*self.resources, *resources})
