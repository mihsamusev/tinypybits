import pytest


def is_parameter(base):
    return issubclass(base, Parameter)


def is_variable(base):
    return issubclass(base, Variable)


class Parameter:
    def __init__(self):
        self.name = None


class Variable:
    def __init__(self):
        self.name = None


class ModelObject:
    def __init__(self):
        self.name = None

    def params(self):
        return self.__component_methods(filter_fn=is_parameter)

    def vars(self):
        return self.__component_methods(filter_fn=is_variable)

    def __component_methods(self, filter_fn):
        names = self.__component_names(filter_fn)
        methods = map(lambda name: getattr(self, name), names)
        return dict(zip(names, methods))

    def __component_names(self, filter_fn):
        component_classes = filter(filter_fn, type(self).__bases__)
        return list(map(lambda p: p().name, component_classes))


class PowerInput(Parameter):
    def __init__(self):
        super().__init__()
        self.name = "power_input"

    def power_input(self, t: int):
        raise NotImplementedError(f"{self.name} not implemented")


class PowerOutput(Parameter):
    def __init__(self):
        super().__init__()
        self.name = "power_output"

    def power_output(self, t: int):
        raise NotImplementedError(f"{self.name} not implemented")


class PowerStation(ModelObject, PowerInput, PowerOutput):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


def test_model_object_parameter_methods_created():
    station = PowerStation(name="gas_station")
    print(station.params())

    for param_fn in station.params().values():
        with pytest.raises(NotImplementedError):
            param_fn(0)


def test_model_object_parameter_methods_have_different_refs():
    station1 = PowerStation(name="gas_station_1")
    print(station1.params())
    station2 = PowerStation(name="gas_station_2")
    print(station2.params())

    assert station1.params().keys() == station2.params().keys()
    assert station1.params().values() != station2.params().values()


if __name__ == "__main__":
    test_model_object_parameter_methods_created()
    test_model_object_parameter_methods_have_different_refs()
