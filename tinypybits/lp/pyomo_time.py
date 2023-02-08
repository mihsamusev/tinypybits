import pyomo.environ as pyo
import random

random.seed(42)


class PowerSource:
    def __init__(self, output_capacity):
        self.output_capacity = output_capacity

    def get_random_power_available(self):
        return random.random() * self.output_capacity

    def get_n_random_power_available(self, n):
        return {i + 1: random.random() * self.output_capacity for i in range(n)}


class Electrolyzer:
    power_input_capacity = 400
    h2_ouptut_capacity = 7.681
    efficiency_curve_slope = 52.21
    efficiency_curve_offset = -1.02


class H2Consumer:
    h2_input_capacity = 500


def build_model_without_time():
    model = pyo.ConcreteModel()
    model.power_available = pyo.Param(
        initialize=PowerSource(output_capacity=700).get_random_power_available(),
        domain=pyo.NonNegativeReals,
    )

    model.electrolyzer_power_input = pyo.Var(
        bounds=(0, Electrolyzer.power_input_capacity),
        domain=pyo.NonNegativeReals,
    )

    model.electrolyzer_h2_output = pyo.Var(
        bounds=(0, Electrolyzer.h2_ouptut_capacity), domain=pyo.NonNegativeReals
    )

    model.h2_consumer_h2_input = pyo.Var(
        bounds=(0, H2Consumer.h2_input_capacity), domain=pyo.NonNegativeReals
    )

    model.add_component(
        "electrolyzer power input cant be more than poweer source power",
        pyo.Constraint(expr=model.electrolyzer_power_input <= model.power_available),
    )
    model.add_component(
        "electrolyzer sends h2 to consumer without losses",
        pyo.Constraint(expr=model.electrolyzer_h2_output == model.h2_consumer_h2_input),
    )

    model.add_component(
        "linear conversion between produced h2 and consumed power",
        pyo.Constraint(
            expr=model.electrolyzer_power_input
            == Electrolyzer().efficiency_curve_slope * model.electrolyzer_h2_output
            + Electrolyzer.efficiency_curve_offset
        ),
    )
    model.objective = pyo.Objective(expr=model.h2_consumer_h2_input, sense=pyo.maximize)

    return model


def build_model_with_time(horizon_hours):
    model = pyo.ConcreteModel()
    model.time = pyo.RangeSet(horizon_hours)  # 1 based
    model.power_available = pyo.Param(
        model.time,
        initialize=PowerSource(output_capacity=700).get_n_random_power_available(
            horizon_hours
        ),
        domain=pyo.NonNegativeReals,
    )

    model.electrolyzer_power_input = pyo.Var(
        model.time,
        bounds=(0, Electrolyzer.power_input_capacity),
        domain=pyo.NonNegativeReals,
    )

    model.electrolyzer_h2_output = pyo.Var(
        model.time,
        bounds=(0, Electrolyzer.h2_ouptut_capacity),
        domain=pyo.NonNegativeReals,
    )

    model.h2_consumer_h2_input = pyo.Var(
        model.time,
        bounds=(0, H2Consumer.h2_input_capacity),
        domain=pyo.NonNegativeReals,
    )

    model.add_component(
        "electrolyzer power input cant be more than power",
        pyo.Constraint(
            model.time,
            rule=lambda model, t: model.electrolyzer_power_input[t]
            <= model.power_available[t],
        ),
    )
    model.add_component(
        "electrolyzer sends h2 to consumer without losses",
        pyo.Constraint(
            model.time,
            rule=lambda model, t: model.electrolyzer_h2_output[t]
            == model.h2_consumer_h2_input[t],
        ),
    )

    model.add_component(
        "linear conversion between produced h2 and consumed power",
        pyo.Constraint(  
            model.time,
            rule=lambda model, t: model.electrolyzer_power_input[t]
            == Electrolyzer().efficiency_curve_slope * model.electrolyzer_h2_output[t]
            + Electrolyzer.efficiency_curve_offset,
        ),
    )


    def h2_consumer_h2_input():
        return (model.h2_consumer_h2_input[t] for t in model.time)

    model.objective = pyo.Objective(expr=pyo.quicksum(h2_consumer_h2_input()), sense=pyo.maximize)
#    model.objective = pyo.Objective(
#        expr=pyo.quicksum(model.h2_consumer_h2_input[:]), sense=pyo.maximize
#    )

    return model


def display_results(model):
    results = []
    for name, var in model.component_map(ctype=[pyo.Var, pyo.Param]).items():
        result = f"{name} -> {var.extract_values()}"
        results.append(result)

    print("\n".join(results))


def main(solver_name):
    horizon_hours = 3
    model = build_model_with_time(horizon_hours)
    # model = build_model_without_time()

    # model.pprint(open("model_internals_before.txt", "w"))

    solver = pyo.SolverFactory(solver_name)
    solver.solve(model)
    display_results(model)
    # model.pprint(open("model_internals_after.txt", "w"))


if __name__ == "__main__":
    main(solver_name="glpk")
