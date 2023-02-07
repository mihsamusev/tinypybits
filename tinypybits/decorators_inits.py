from typing import List

class ModelObject:
    def print(self):
        print("im base class")

class PowerInput:
    def power_input(self, t: int):
        print("im power input")

class H2Output:
    def h2_output(self, t: int):
        print("im h2 output")


def attach_variables(target: ModelObject, variable_types: List[ModelObject]):
    def decorator_attach():
        inherited_types = [target] + variable_types
        fused_type = type("FusedType", (inherited_types), {})
        fused_class = fused_type()
        return fused_class

    return decorator_attach

def attach_all(target: ModelObject):
    def inner():
        fused_type = type("FusedType", (target, H2Output, PowerInput), {})
        fused_class = fused_type()
        return fused_class
    return inner

#attach_variables([PowerInput, H2Output])
@attach_all
class Electrolyzer(ModelObject):
    def __init__(self):
        print("elect initialized")

print(Electrolyzer.__class__, Electrolyzer.__class__.__bases__)
electrolyzer = Electrolyzer()
electrolyzer.h2_output(t=1)
electrolyzer.power_input(t=2)



