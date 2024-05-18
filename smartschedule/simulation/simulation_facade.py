from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)
from smartschedule.simulation.demands import Demands
from smartschedule.simulation.result import Result
from smartschedule.simulation.simulated_capabilities import SimulatedCapabilities
from smartschedule.simulation.simulated_project import SimulatedProject


def which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
    projects_simulations: list[SimulatedProject],
    total_capability: SimulatedCapabilities,
) -> Result:
    capabilities = total_capability.capabilities
    capacities_size = len(capabilities)
    dp = [0] * (capacities_size + 1)
    chosen_items_list: list[list[SimulatedProject]] = [
        [] for _ in range(capacities_size + 1)
    ]
    allocated_capacities_list: list[set[AvailableResourceCapability]] = [
        set() for _ in range(capacities_size + 1)
    ]

    automatically_included_items = [
        sim for sim in projects_simulations if sim.all_demands_satisfied()
    ]
    guaranteed_value = sum(sim.earnings for sim in automatically_included_items)

    all_availabilities = set(capabilities)
    item_to_capacities_map: dict[
        SimulatedProject, set[AvailableResourceCapability]
    ] = {}

    for project in sorted(projects_simulations, key=lambda x: x.earnings, reverse=True):
        chosen_capacities = _match_capacities(
            project.missing_demands, all_availabilities
        )
        all_availabilities.difference_update(chosen_capacities)

        if not chosen_capacities:
            continue

        sum_value = project.earnings
        chosen_capacities_count = len(chosen_capacities)

        for j in range(capacities_size, chosen_capacities_count - 1, -1):
            if dp[j] < (sum_value + dp[j - chosen_capacities_count]):
                dp[j] = sum_value + dp[j - chosen_capacities_count]

                chosen_items_list[j] = [
                    *chosen_items_list[j - chosen_capacities_count],
                    project,
                ]
                allocated_capacities_list[j] |= set(chosen_capacities)

        item_to_capacities_map[project] = set(chosen_capacities)

    chosen_items_list[capacities_size] = [
        *chosen_items_list[capacities_size],
        *automatically_included_items,
    ]
    return Result(
        dp[capacities_size] + guaranteed_value,
        chosen_items_list[capacities_size],
        item_to_capacities_map,
    )


def _match_capacities(
    demands: Demands,
    available_capacities: set[AvailableResourceCapability],
) -> list[AvailableResourceCapability]:
    result: list[AvailableResourceCapability] = []

    for weight_component in demands:
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
