from attrs import frozen

from smartschedule.optimization.capacity_dimension import CapacityDimension
from smartschedule.optimization.item import Item


@frozen
class Result:
    profit: float
    chosen_items: list[Item]
    item_to_capacities: dict[Item, set[CapacityDimension]]
