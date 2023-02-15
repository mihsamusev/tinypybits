from typing import List
import inspect
from copy import deepcopy


class Variable:
    pass


class ModelObject:
    def display(self):
        print("im model class")


class PowerInput(Variable):
    def power_input(self, t: int):
        print(f"im power input at time t={t}")


class H2Output(Variable):
    def h2_output(self, t: int):
        print(f"im h2 output at time t={t}")


def add_mixins(variable_types: List[Variable]):
    def inner(target_class: ModelObject):
        inherited_types = tuple([target_class]) + tuple(variable_types)
        fused_type = type(target_class.__class__.__name__, inherited_types, {})
        return fused_type

    return inner


def add_variables(variables: List[Variable]):
    def inner(target_class: ModelObject):
        for variable in variables:
            public_functions = inspect.getmembers(
                variable, predicate=inspect.isfunction
            )
            for name, callable in public_functions:
                setattr(target_class, name, callable)
        return target_class

    return inner


@add_variables([PowerInput, H2Output])
class ElectrolyzerTK(ModelObject):
    def __init__(self):
        print("elect initialized")


@add_variables([PowerInput, H2Output])
class ElectrolyzerSunfire(ModelObject):
    def __init__(self):
        print("Im sunfire")


if __name__ == "__main__":
    electrolyzer = ElectrolyzerTK()
    print(electrolyzer.__class__, electrolyzer.__class__.__bases__)
    electrolyzer.power_input(t=1)
    electrolyzer.h2_output(t=1)

    sunfire = ElectrolyzerSunfire()
    print(sunfire.__class__, sunfire.__class__.__bases__)
    sunfire.power_input(t=1)
    sunfire.h2_output(t=1)

    assert id(electrolyzer.power_input) != id(sunfire.power_input)
