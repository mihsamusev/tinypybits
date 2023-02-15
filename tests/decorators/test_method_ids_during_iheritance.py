from tinypybits.decorators import PowerInput, H2Output


class Electrolyzer(PowerInput, H2Output):
    def __init__(self, name):
        self.name = name


def modify_name(self, new_name):
    self.name = new_name


def test_basic_inheritance_generates_unique_id_for_methods_of_new_class_instance():
    class Electrolyzer(PowerInput, H2Output):
        def __init__(self, name):
            self.name = name

    def modify_name(self, new_name):
        self.name = new_name

    first = Electrolyzer("Bob")
    first.h2_output(0)
    first.power_input(0)

    second = Electrolyzer("Alice")
    assert id(first.h2_output) != (second.h2_output)
    assert id(first.power_input) != (second.power_input)


def test_adding_method_to_class_after_instances_initialized_produces_unique_method_ids():
    class Electrolyzer(PowerInput, H2Output):
        def __init__(self, name):
            self.name = name

    def modify_name(self, new_name):
        self.name = new_name

    assert getattr(Electrolyzer, "modify_name", None) is None
    first = Electrolyzer("Mads")
    second = Electrolyzer("Lars")
    setattr(Electrolyzer, "modify_name", modify_name)

    first.modify_name("Bob")
    assert first.name == "Bob"
    assert second.name == "Lars"
    assert id(first.modify_name) != id(second.modify_name)


def test_adding_method_to_class_before_instances_initialized_produces_unique_method_ids():
    class Electrolyzer(PowerInput, H2Output):
        def __init__(self, name):
            self.name = name

    def modify_name(self, new_name):
        self.name = new_name

    assert getattr(Electrolyzer, "modify_name", None) is None
    setattr(Electrolyzer, "modify_name", modify_name)
    first = Electrolyzer("Mads")
    second = Electrolyzer("Lars")

    first.modify_name("Bob")
    assert first.name == "Bob"
    assert second.name == "Lars"
    assert id(first.modify_name) != id(second.modify_name)
