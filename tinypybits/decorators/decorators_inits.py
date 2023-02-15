from typing import List
import inspect
from copy import deepcopy


def record_call():
    with open("how_many_imports.log", "a") as fout:
        fout.write("im imported again!\n")


class Variable:
    pass


class ModelObject:
    def display(self):
        print("im model class")


class PowerInput(Variable):
    def power_input(self, t: int):
        print(
            f"im power input at time t={t} of object {self.__class__.__name__}:{id(self)}"
        )


class H2Output(Variable):
    def h2_output(self, t: int):
        print(
            f"im h2 output at time t={t} of object {self.__class__.__name__}:{id(self)}"
        )


def add_mixins(variables: List[Variable]):
    """
    Generates new type with target class methods and methods from given variable classes
    """

    def inner(target_class: ModelObject):
        inherited_types = tuple([target_class]) + tuple(variables)
        fused_type = type(target_class.__class__.__name__, inherited_types, {})
        return fused_type

    return inner


def add_variables(variables: List[Variable]):
    """
    Reuses target class but sets new methods from given variable classes
    """

    def inner(target_class: ModelObject):
        for variable in variables:
            public_methods = inspect.getmembers(variable, predicate=inspect.isfunction)
            for method_name, method_callable in public_methods:
                setattr(target_class, method_name, method_callable)
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


def example():
    electrolyzer = ElectrolyzerTK()
    print(electrolyzer.__class__, electrolyzer.__class__.__bases__)
    electrolyzer.power_input(t=1)
    electrolyzer.h2_output(t=1)

    sunfire = ElectrolyzerSunfire()
    print(sunfire.__class__, sunfire.__class__.__bases__)
    sunfire.power_input(t=1)
    sunfire.h2_output(t=1)

    another_sunfire = ElectrolyzerSunfire()

    print(id(electrolyzer.power_input), id(sunfire.power_input))
    assert id(electrolyzer.power_input) != id(sunfire.power_input)
    assert id(electrolyzer.h2_output) != id(sunfire.h2_output)
    assert id(sunfire.h2_output) != id(another_sunfire.h2_output)


if __name__ == "__main__":
    example()
