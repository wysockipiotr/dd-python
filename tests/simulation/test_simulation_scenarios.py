import uuid
from typing import Final

import pytest

from smartschedule.optimization.optimization_facade import OptimizationFacade
from smartschedule.shared.time_slot import TimeSlot
from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)
from smartschedule.simulation.capability import Capability
from smartschedule.simulation.demand import Demand
from smartschedule.simulation.project_id import project_id
from smartschedule.simulation.simulation_facade import (
    SimulationFacade,
)
from tests.simulation.available_capabilities_builder import AvailableCapacitiesBuilder
from tests.simulation.simulated_projects_builder import SimulatedProjectsBuilder

demand_for = Demand.demand_for
skill = Capability.skill

JAN_1: Final = TimeSlot.create_daily_time_slot_at_utc(2021, 1, 1)
PROJECT_1: Final = project_id()
PROJECT_2: Final = project_id()
PROJECT_3: Final = project_id()
STASZEK: Final = uuid.uuid4()
LEON: Final = uuid.uuid4()


@pytest.fixture()
def simulation() -> SimulationFacade:
    optimization_facade = OptimizationFacade()
    return SimulationFacade(optimization_facade)


pytestmark = pytest.mark.unit


def test_picks_optimal_project_based_on_earnings(
    simulated_projects_builder: SimulatedProjectsBuilder,
    available_capacities_builder: AvailableCapacitiesBuilder,
    simulation: SimulationFacade,
) -> None:
    simulated_projects = (
        simulated_projects_builder.with_project(PROJECT_1)
        .that_requires(demand_for(skill("JAVA-MID"), JAN_1))
        .that_can_earn(9)
        .with_project(PROJECT_2)
        .that_requires(demand_for(skill("JAVA-MID"), JAN_1))
        .that_can_earn(99)
        .with_project(PROJECT_3)
        .that_requires(demand_for(skill("JAVA-MID"), JAN_1))
        .that_can_earn(2)
        .build()
    )

    simulated_availability = (
        available_capacities_builder.with_employee(STASZEK)
        .that_brings(skill("JAVA-MID"))
        .that_is_available_at(JAN_1)
        .with_employee(LEON)
        .that_brings(skill("JAVA-MID"))
        .that_is_available_at(JAN_1)
        .build()
    )

    result = simulation.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        simulated_projects,
        simulated_availability,
    )

    assert result.profit == 108
    assert len(result.chosen_items) == 2


def test_picks_all_when_enough_capabilities(
    simulated_projects_builder: SimulatedProjectsBuilder,
    available_capacities_builder: AvailableCapacitiesBuilder,
    simulation: SimulationFacade,
) -> None:
    simulated_projects = (
        simulated_projects_builder.with_project(PROJECT_1)
        .that_requires(demand_for(skill("JAVA-MID"), JAN_1))
        .that_can_earn(99)
        .build()
    )

    simulated_availability = (
        available_capacities_builder.with_employee(STASZEK)
        .that_brings(skill("JAVA-MID"))
        .that_is_available_at(JAN_1)
        .with_employee(LEON)
        .that_brings(skill("JAVA-MID"))
        .that_is_available_at(JAN_1)
        .build()
    )

    result = simulation.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        simulated_projects,
        simulated_availability,
    )

    assert result.profit == 99
    assert len(result.chosen_items) == 1


def test_can_simulate_having_extra_resources(
    simulated_projects_builder: SimulatedProjectsBuilder,
    available_capacities_builder: AvailableCapacitiesBuilder,
    simulation: SimulationFacade,
) -> None:
    simulated_projects = (
        simulated_projects_builder.with_project(PROJECT_1)
        .that_requires(demand_for(skill("YT DRAMA COMMENTS"), JAN_1))
        .that_can_earn(9)
        .with_project(PROJECT_2)
        .that_requires(demand_for(skill("YT DRAMA COMMENTS"), JAN_1))
        .that_can_earn(99)
        .build()
    )

    simulated_availability = (
        available_capacities_builder.with_employee(STASZEK)
        .that_brings(skill("YT DRAMA COMMENTS"))
        .that_is_available_at(JAN_1)
        .build()
    )

    extra_capability = AvailableResourceCapability(
        uuid.uuid4(),
        skill("YT DRAMA COMMENTS"),
        JAN_1,
    )

    result_without_extra_resource = simulation.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        simulated_projects,
        simulated_availability,
    )

    result_with_extra_resource = simulation.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        simulated_projects,
        simulated_availability.add(extra_capability),
    )

    assert result_without_extra_resource.profit == 99
    assert result_with_extra_resource.profit == 108


def test_picks_optimal_project_based_on_reputation(
    simulation: SimulationFacade,
    simulated_projects_builder: SimulatedProjectsBuilder,
    available_capacities_builder: AvailableCapacitiesBuilder,
) -> None:
    simulated_projects = (
        simulated_projects_builder.with_project(PROJECT_1)
        .that_requires(demand_for(skill("JAVA-MID"), JAN_1))
        .that_can_generate_reputation_loss(100)
        .with_project(PROJECT_2)
        .that_requires(demand_for(skill("JAVA-MID"), JAN_1))
        .that_can_generate_reputation_loss(40)
        .build()
    )
    simulated_availability = (
        available_capacities_builder.with_employee(STASZEK)
        .that_brings(skill("JAVA-MID"))
        .that_is_available_at(JAN_1)
        .build()
    )

    result = simulation.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        simulated_projects,
        simulated_availability,
    )

    assert result.chosen_items[0].name == str(PROJECT_1)
