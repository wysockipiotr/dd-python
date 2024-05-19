from typing import Self, override

from attrs import frozen

from smartschedule.optimization import WeightDimension
from smartschedule.shared.time_slot import TimeSlot
from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)
from smartschedule.simulation.capability import Capability


@frozen
class Demand(WeightDimension[AvailableResourceCapability]):
    capability: Capability
    slot: TimeSlot

    @classmethod
    def demand_for(cls, capability: Capability, slot: TimeSlot) -> Self:
        return cls(capability=capability, slot=slot)

    @override
    def is_satisfied_by(
        self, available_capability: AvailableResourceCapability, /
    ) -> bool:
        return available_capability.performs(self.capability) and self.slot.within(
            available_capability.time_slot
        )
