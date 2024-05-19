from typing import override
from uuid import UUID, uuid4

from attrs import field, frozen

from smartschedule.optimization.capacity_dimension import CapacityDimension
from smartschedule.optimization.weight_dimension import WeightDimension
from smartschedule.shared.time_slot import TimeSlot


@frozen
class CapabilityCapacityDimension(CapacityDimension):
    id: str
    capacity_name: str
    capacity_type: str
    uuid: UUID = field(factory=uuid4)


@frozen
class CapabilityWeightDimension(WeightDimension[CapabilityCapacityDimension]):
    name: str
    type: str

    @override
    def is_satisfied_by(self, capacity_dimension: CapabilityCapacityDimension) -> bool:
        return (
            capacity_dimension.capacity_name == self.name
            and capacity_dimension.capacity_type == self.type
        )


@frozen
class CapabilityTimedCapacityDimension(CapacityDimension):
    id: str
    capacity_name: str
    capacity_type: str
    time_slot: TimeSlot
    uuid: UUID = field(factory=uuid4)


@frozen
class CapabilityTimedWeightDimension(WeightDimension[CapabilityTimedCapacityDimension]):
    name: str
    type: str
    time_slot: TimeSlot

    @override
    def is_satisfied_by(
        self, capacity_timed_dimension: CapabilityTimedCapacityDimension
    ) -> bool:
        return (
            capacity_timed_dimension.capacity_name == self.name
            and capacity_timed_dimension.capacity_type == self.type
            and self.time_slot.within(capacity_timed_dimension.time_slot)
        )
