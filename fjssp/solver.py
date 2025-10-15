from ortools.sat.python import cp_model

def solve_model(model, objective_var, all_tasks):
    """
    Solves the CP-SAT model and returns the objective value
    and a structured schedule for visualization.

    Args:
        model: cp_model.CpModel instance
        objective_var: variable representing the objective
        all_tasks: dict with keys (job_id, task_idx) and values
                   {machine: (start, end, dur, is_assigned, interval_var)}

    Returns:
        tuple: (objective_value, schedule_list)
    """
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30
    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)
    schedule = []

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print(f"Solution found! Objective = {solver.Value(objective_var)}")
        for (job_id, t_idx), machine_vars in all_tasks.items():
            for m, (start, end, dur, is_assigned, _) in machine_vars.items():
                if solver.Value(is_assigned):
                    print(f"Job {job_id} - Task {t_idx} on {m}: "
                          f"Start={solver.Value(start)}, End={solver.Value(end)}, Dur={dur}")

                    # Append to schedule for visualization
                    schedule.append({
                        "job_id": job_id,
                        "task_name": f"T{t_idx}",
                        "machine": m,
                        "start": solver.Value(start),
                        "end": solver.Value(end)
                    })
        # Sort by start time for readability
        schedule.sort(key=lambda x: x["start"])
        return solver.Value(objective_var), schedule
    else:
        print("No feasible solution found.")
        return None, []

