from datetime import timedelta
from attrs import frozen, field


@frozen
class ResourceName:
    name: str


@frozen
class Stage:
    stage_name: str
    dependencies: set["Stage"] = field(factory=set, hash=False)
    resources: set[ResourceName] = field(factory=set, hash=False)
    duration: timedelta = field(default=timedelta.min, hash=False)

    def depends_on(self, stage: "Stage") -> "Stage":
        self.dependencies.add(stage)
        return self

    @property
    def name(self):
        return self.stage_name
