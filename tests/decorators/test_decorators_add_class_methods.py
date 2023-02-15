"""
By default, fixtures have the function scope.
This means that a new instance of the fixture function is created
for each test function that uses it.
"""

from tinypybits.decorators import ElectrolyzerSunfire, ElectrolyzerTK
import pytest


@pytest.fixture()
def distinct_electrolyzers():
    return [ElectrolyzerSunfire(), ElectrolyzerTK()]


@pytest.fixture()
def same_electrolyzers():
    return [ElectrolyzerSunfire(), ElectrolyzerSunfire()]


def test_add_variables_decorator_creates_methods_for_the_eletrolyzer_classes(
    distinct_electrolyzers,
):
    for electrolyzer in distinct_electrolyzers:
        electrolyzer.power_input(t=1)
        electrolyzer.h2_output(t=1)


def test_instances_of_distinct_type_receive_unique_method_ids_on_decorator_application(
    distinct_electrolyzers,
):
    assert id(distinct_electrolyzers[0].power_input) != id(
        distinct_electrolyzers[1].power_input
    )
    assert id(distinct_electrolyzers[0].h2_output) != id(
        distinct_electrolyzers[1].h2_output
    )


def test_instances_of_same_type_receive_unique_method_ids_on_decorator_application(
    same_electrolyzers,
):
    assert id(same_electrolyzers[0].power_input) != id(
        same_electrolyzers[1].power_input
    )
    assert id(same_electrolyzers[0].h2_output) != id(same_electrolyzers[1].h2_output)


def test_instances_receive_unique_method_ids_on_decorator_application_no_fixtures():
    sunfire = ElectrolyzerSunfire()
    tk_first = ElectrolyzerTK()
    tk_second = ElectrolyzerTK()
    assert id(sunfire.power_input) != id(tk_first.power_input)
    assert id(tk_first.power_input) != id(tk_second.power_input)


if __name__ == "__main__":
    test_instances_receive_unique_method_ids_on_decorator_application_no_fixtures()
