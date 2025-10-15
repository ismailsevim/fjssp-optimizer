import pytest
from fjssp.data_loader import load_instance
from fjssp.model_builder import build_fjssp_model
from fjssp.solver import solve_model
from fjssp.visualizer import visualize_schedule


@pytest.mark.parametrize("instance_file", [
    "data/instance_small_makespan.json",
    "data/instance_large_tardiness.json"
])
def test_fjssp_pipeline(instance_file):
    """
    Full integration test for the FJSSP optimizer pipeline.
    Covers data loading, model building, solving, and visualization.
    """

    print(f"\n=== Testing instance: {instance_file} ===")

    # --- Load data ---
    data = load_instance(instance_file)
    assert "objective" in data, "Objective key missing in instance JSON."
    objective_type = data["objective"]
    print(f"Objective type: {objective_type}")

    # --- Build model ---
    model, objective_var, all_tasks, obj_type = build_fjssp_model(data)
    assert model is not None, "Model not created."
    assert objective_var is not None, "Objective variable missing."
    assert isinstance(all_tasks, dict), "Tasks should be a dictionary."
    assert obj_type == objective_type, "Objective mismatch between JSON and model."

    # --- Solve model ---
    obj_value, schedule = solve_model(model, objective_var, all_tasks)
    assert obj_value is not None, "Solver did not return an objective value."
    assert isinstance(schedule, list), "Schedule must be a list."
    assert len(schedule) > 0, "Schedule is empty."

    print(f"Solver completed. Objective = {obj_value}")

    # --- Visualize schedule (optional) ---
    # We only call this to ensure it doesn’t crash.
    try:
        visualize_schedule(schedule, objective_type=obj_type, objective_value=obj_value)
    except Exception as e:
        pytest.fail(f"Visualization failed with error: {e}")

    print(f"Full pipeline test passed for {objective_type}.")


if __name__ == "__main__":
    pytest.main(["-v", "tests/test_pipeline.py"])
