import pytest

from tests.simulation.available_capabilities_builder import AvailableCapacitiesBuilder
from tests.simulation.simulated_projects_builder import SimulatedProjectsBuilder


@pytest.fixture()
def available_capacities_builder():
    return AvailableCapacitiesBuilder()


@pytest.fixture()
def simulated_projects_builder():
    return SimulatedProjectsBuilder()
