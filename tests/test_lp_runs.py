from tinypybits.lp.pyomo_time import main


def test_lp_runs():
    main(solver_name="glpk")
    main(solver_name="scip")
    main(solver_name="ipopt")