from tinypybits.linear_programming.example_problem import build_model
from pyomo.environ import SolverFactory, SolverStatus


def test_lp_runs():
    solver_names = ["glpk", "scip"]
    for solver_name in solver_names:
        solver = SolverFactory(solver_name)
        result = solver.solve(build_model())
        assert result.solver.status == SolverStatus.ok
