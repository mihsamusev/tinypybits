import pyomo.environ as pyo


def make_name(plant_name, variable_name):
    return f"{plant_name}_{variable_name}"


def create_model():
    model = pyo.ConcreteModel()
    model.time = pyo.Set(initialize=range(5))
    model.add_component(
        make_name("electrolyzer", "h2_output"),
        pyo.Var(model.time, domain=pyo.NonNegativeReals),
    )

    return model


def main():
    model = create_model()

    model.component(make_name("electrolyzer", "h2_output"))[model.time.last()] = 5
    model.pprint()


if __name__ == "__main__":
    main()
