from attrs import frozen

from smartschedule.optimization.total_weight import TotalWeight


@frozen
class Item:
    name: str
    value: float
    total_weight: TotalWeight

    def is_weight_zero(self) -> bool:
        return not self.total_weight.components()
