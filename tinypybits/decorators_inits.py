from typing import List


class ModelObject:
    def display(self):
        print("im model class")


class PowerInput:
    def power_input(self, t: int):
        """
        power_input
        """
        print("im power input")


class H2Output:
    def h2_output(self, t: int):
        """
        h2_output
        """
        print("im h2 output")


def attach_variables(variable_types: List[ModelObject]):
    def decorator_attach(target: ModelObject):
        inherited_types = tuple([target]) + tuple(variable_types)
        fused_type = type("FusedType", inherited_types, {})
        return fused_type

    return decorator_attach


@attach_variables([PowerInput, H2Output])
class Electrolyzer(ModelObject):
    def __init__(self):
        print("elect initialized")


electrolyzer = Electrolyzer()
print(electrolyzer.__class__, electrolyzer.__class__.__bases__)
print(Electrolyzer.__mro__)
electrolyzer.power_input(t=1)
electrolyzer.h2_output(t=1)