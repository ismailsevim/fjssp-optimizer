from fjssp.data_loader import load_instance
from fjssp.model_builder import build_fjssp_model
from fjssp.solver import solve_model
# Optional: import visualize if you want to plot the schedule
from fjssp.visualizer import visualize_schedule

def main():
    # === Load data ===
    data = load_instance("data/instance_large_tardiness.json")

    # === Build model ===
    model, objective_var, all_tasks, objective_type = build_fjssp_model(data)
    print(f"Objective type: {objective_type}")

    # === Solve model ===
    obj_value, schedule = solve_model(model, objective_var, all_tasks)
    
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
        
        # Optional: visualize schedule
        visualize_schedule(schedule, objective_type, obj_value)

if __name__ == "__main__":
    main()
