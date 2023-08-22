from pyomo.environ import ConcreteModel, Var, Constraint, Set
from pyomo.core.expr.current import identify_variables, identify_components

def contraint_variables(model):
    for constraint in model.component_objects(ctype=Constraint):
        expression = constraint[model.t.first()].expr
        variables = identify_variables(expr=expression)

        variables_str = [v.getname(fully_qualified=False) for v in variables]
        display_str = f"{constraint.name} -> ({', '.join(variables_str)})"
        print(display_str)


def find_unused_variables(model):
    used_vars = set()

    for constr in model.component_objects(Constraint, active=True):
        for index in constr:
            expr = constr[index].expr
            variables = identify_variables(expr)
            used_vars.update([v.name for v in variables])

    all_vars = set(v.name for v_data in model.component_objects(Var) for v in v_data.values())

    unused_vars = all_vars - used_vars
    return unused_vars


model = ConcreteModel()
model.t = Set(initialize=range(0, 720))
model.x = Var(model.t)
model.y = Var(model.t)
model.z = Var(model.t)
model.c1 = Constraint(model.t, rule=lambda model, t: model.x[t] + model.y[t] == 1)
model.c2 = Constraint(model.t, rule=lambda model, t: model.y[t] == 2)
model.pprint()

print(find_unused_variables(model))
contraint_variables(model)
