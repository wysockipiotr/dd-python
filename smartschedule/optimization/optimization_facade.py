from collections.abc import Collection

from smartschedule.optimization.capacity_dimension import CapacityDimension
from smartschedule.optimization.item import Item
from smartschedule.optimization.result import Result
from smartschedule.optimization.total_capacity import TotalCapacity
from smartschedule.optimization.total_weight import TotalWeight


class OptimizationFacade:
    def calculate(self, items: list[Item], total_capacity: TotalCapacity) -> Result:
        capacities_size: int = len(total_capacity)
        dp: list[float] = [0.0] * (capacities_size + 1)
        chosen_items_list: list[list[Item]] = [[] for _ in range(capacities_size + 1)]
        allocated_capacities_list: list[set[CapacityDimension]] = [
            set() for _ in range(capacities_size + 1)
        ]

        automatically_included_items = [item for item in items if item.is_weight_zero()]
        guaranteed_value = sum(item.value for item in automatically_included_items)

        all_capacities = total_capacity.capacities()
        item_to_capacities_map: dict[Item, set[CapacityDimension]] = {}

        for item in sorted(items, key=lambda x: x.value, reverse=True):
            chosen_capacities = self._match_capacities(
                item.total_weight, all_capacities
            )
            all_capacities = [c for c in all_capacities if c not in chosen_capacities]

            if not chosen_capacities:
                continue

            sum_value = item.value
            chosen_capacities_count = len(chosen_capacities)

            for j in range(capacities_size, chosen_capacities_count - 1, -1):
                if dp[j] < (sum_value + dp[j - chosen_capacities_count]):
                    dp[j] = sum_value + dp[j - chosen_capacities_count]

                    chosen_items_list[j] = [
                        *chosen_items_list[j - chosen_capacities_count],
                        item,
                    ]
                    allocated_capacities_list[j] |= set(chosen_capacities)

            item_to_capacities_map[item] = set(chosen_capacities)

        chosen_items_list[capacities_size] = [
            *chosen_items_list[capacities_size],
            *automatically_included_items,
        ]
        return Result(
            profit=dp[capacities_size] + guaranteed_value,
            chosen_items=chosen_items_list[capacities_size],
            item_to_capacities=item_to_capacities_map,
        )

    @staticmethod
    def _match_capacities(
        total_weight: TotalWeight,
        available_capacities: Collection[CapacityDimension],
    ) -> list[CapacityDimension]:
        result: list[CapacityDimension] = []

        for weight_component in total_weight.components():
            try:
                matching_capacity = next(
                    capacity
                    for capacity in available_capacities
                    if weight_component.is_satisfied_by(capacity)
                )
            except StopIteration:
                return []
            result.append(matching_capacity)

        return result
