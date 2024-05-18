from itertools import chain

from attrs import frozen

from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)


@frozen
class SimulatedCapabilities:
    capabilities: list[AvailableResourceCapability]

    def add(
        self, *new_capabilities: AvailableResourceCapability
    ) -> "SimulatedCapabilities":
        return SimulatedCapabilities(list(chain(self.capabilities, new_capabilities)))
