from typing import Self
from uuid import UUID

from attrs import field, mutable

from smartschedule.shared.time_slot import TimeSlot
from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)
from smartschedule.simulation.capability import Capability
from smartschedule.simulation.simulated_capabilities import SimulatedCapabilities


@mutable
class AvailableCapacitiesBuilder:
    _current_resource_id: UUID | None = None
    _capability: Capability | None = None
    _time_slot: TimeSlot | None = None
    _availabilities: list[AvailableResourceCapability] = field(factory=list)

    def with_employee(self, resource_id: UUID) -> Self:
        if self._current_resource_id and self._capability and self._time_slot:
            self._availabilities.append(
                AvailableResourceCapability(
                    resource_id=self._current_resource_id,
                    capability=self._capability,
                    time_slot=self._time_slot,
                )
            )
        self._current_resource_id = resource_id
        return self

    def that_brings(self, capability: Capability) -> Self:
        self._capability = capability
        return self

    def that_is_available_at(self, time_slot: TimeSlot) -> Self:
        self._time_slot = time_slot
        return self

    def build(self) -> SimulatedCapabilities:
        if self._current_resource_id and self._capability and self._time_slot:
            self._availabilities.append(
                AvailableResourceCapability(
                    resource_id=self._current_resource_id,
                    capability=self._capability,
                    time_slot=self._time_slot,
                )
            )
        return SimulatedCapabilities(self._availabilities)
