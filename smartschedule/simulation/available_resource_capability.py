from uuid import UUID

from attrs import frozen

from smartschedule.optimization.capacity_dimension import CapacityDimension
from smartschedule.shared import TimeSlot
from smartschedule.simulation.capability import Capability


@frozen
class AvailableResourceCapability(CapacityDimension):
    resource_id: UUID
    capability: Capability
    time_slot: TimeSlot

    def performs(self, capability: Capability) -> bool:
        return self.capability == capability
