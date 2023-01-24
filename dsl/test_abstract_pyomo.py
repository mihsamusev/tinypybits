def test_model_wrapper_example():
    model = PyomoModelWrapper(horizon_hours=3)
    electrolyzer = electrolyzers.Electrolyzer("E2")
    model.add(electrolyzer)

    model_variables = model.get_pyomo().component_map(ctype=pyo.Var)
    assert len(next(model_variables.values()).extract_values()) == 3

    
    model.add_constraint(
        "Cannot produce more than capacity",
        electrolyzer.h2_output() <= 100
    )
    # has to translate to 
    # lambda t: model.electrolyzer_h2_output[t] <= 100

    model_constraints = model.get_pyomo().component_map(ctype=pyo.Constraint)
    assert len(model_constraints) == 1