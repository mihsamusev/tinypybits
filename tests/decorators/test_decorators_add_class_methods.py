from tinypybits.decorators import ElectrolyzerSunfire, ElectrolyzerTK
import pytest


@pytest.fixture()
def unique_electrolyzers():
    return [ElectrolyzerSunfire(), ElectrolyzerTK()]

@pytest.fixture()
def same_electrolyzers():
    return [ElectrolyzerSunfire(), ElectrolyzerSunfire()]

def test_add_variables_decorator_creates_methods_for_the_eletrolyzer_classes(
    unique_electrolyzers,
):
    for electrolyzer in unique_electrolyzers:
        electrolyzer.power_input(t=1)
        electrolyzer.h2_output(t=1)


def test_different_classes_with_same_variables_attached_point_to_different_method_ids(
    unique_electrolyzers,
):
    assert id(unique_electrolyzers[0].power_input) != id(unique_electrolyzers[1].power_input)