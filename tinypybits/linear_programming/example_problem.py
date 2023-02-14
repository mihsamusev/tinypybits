"""
https://jckantor.github.io/CBE30338/06.04-Linear-Production-Model-in-Pyomo.html
x, y = rates of production in units per week
maximize: 40x + 30y
subject_to:
    x>0
    y>0
    x <= 40 demand constraint
    x + y <= 80 labor A constraints
    2x + y <= 100 labor b constraits
"""

from pyomo.environ import (
    ConcreteModel,
    Var,
    Constraint,
    Objective,
    maximize,
    NonNegativeReals,
)


def build_model():
    model = ConcreteModel()

    # variables
    model.x = Var(domain=NonNegativeReals)
    model.y = Var(domain=NonNegativeReals)

    # constraints
    model.demand = Constraint(expr=model.x <= 40)
    model.laborA = Constraint(expr=model.x + model.y <= 80)
    model.laborB = Constraint(expr=2 * model.x + model.y <= 100)

    # objective
    model.objective = Objective(expr=40 * model.x + 30 * model.y, sense=maximize)

    return model
