from ortools.sat.python import cp_model
import time
import argparse

from fjssp.data_loader import load_instance
from fjssp.model_builder import build_fjssp_model
from fjssp.solver import solve_model
from fjssp.visualizer import visualize_schedule


def main():
    parser = argparse.ArgumentParser(description="Solve a Flexible Job Shop Scheduling Problem (FJSSP)")
    parser.add_argument("--instance", type=str, required=True, help="Path to JSON instance file")
    parser.add_argument("--objective", type=str, default=None, help="Objective type (makespan, flow_time, tardiness)")
    parser.add_argument("--no_plot", action="store_true", help="Disable Gantt chart visualization")
    args = parser.parse_args()

    print("\n=== Loading Instance ===")
    print(f"Instance file: {args.instance}")

    data = load_instance(args.instance)

    # Inject objective from command-line if provided, otherwise default to makespan
    if args.objective:
        data["objective"] = args.objective.lower()
    else:
        data["objective"] = "makespan"

    print("\n=== Building Model ===")
    model, objective_var, all_tasks, objective_type = build_fjssp_model(data)
    print(f"Objective type: {objective_type}")

    print("\n=== Solving Model ===")
    start_time = time.time()
    obj_value, schedule, status = solve_model(model, objective_var, all_tasks)
    runtime = time.time() - start_time

    # Map numeric solver status to readable form
    status_map = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.MODEL_INVALID: "MODEL_INVALID",
        cp_model.UNKNOWN: "TIME_LIMIT or UNKNOWN",
    }
    readable_status = status_map.get(status, f"Unknown ({status})")

    print("\n=== Solver Summary ===")
    print(f"Status: {readable_status}")
    if obj_value is not None:
        print(f"Objective value ({objective_type}): {obj_value}")
    print(f"Runtime: {runtime:.2f} seconds")

    if schedule:
        print("\nFeasible Schedule:")
        print("{:<5} {:<5} {:<10} {:<10}".format("Job", "Task", "Machine", "Start-End"))
        print("-" * 35)
        for task in schedule:
            print("{:<5} {:<5} {:<10} {:<10}".format(
                task["job_id"],
                task["task_name"],
                task["machine"],
                f"{task['start']}-{task['end']}"
            ))

        # Only show chart if --no_plot is not used
        if not args.no_plot:
            visualize_schedule(schedule, objective_type, obj_value)
        else:
            print("\n(Gantt chart visualization skipped.)")


if __name__ == "__main__":
    main()
