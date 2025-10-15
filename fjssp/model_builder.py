from ortools.sat.python import cp_model

def build_fjssp_model(data):
    """
    Builds a CP-SAT model for FJSSP with selectable objective function.
    Supports objectives: makespan, flow_time, tardiness.
    """

    model = cp_model.CpModel()

    machines = data["machines"]
    jobs = data["jobs"]
    objective_type = data.get("objective", "makespan")  # Default to makespan

    horizon = sum(
        max(task["machines"].values())
        for job in jobs
        for task in job["tasks"]
    )

    all_tasks = {}
    job_end_times = {}
    machine_to_intervals = {m: [] for m in machines}

    # --- Build Variables ---
    for job in jobs:
        job_id = job["job_id"]
        previous_end = None

        for t_idx, task in enumerate(job["tasks"]):
            machine_vars = {}

            for m, dur in task["machines"].items():
                start = model.NewIntVar(0, horizon, f"start_j{job_id}_t{t_idx}_{m}")
                end = model.NewIntVar(0, horizon, f"end_j{job_id}_t{t_idx}_{m}")
                is_assigned = model.NewBoolVar(f"is_j{job_id}_t{t_idx}_{m}")
                interval = model.NewOptionalIntervalVar(start, dur, end, is_assigned, f"int_j{job_id}_t{t_idx}_{m}")

                machine_vars[m] = (start, end, dur, is_assigned, interval)
                machine_to_intervals[m].append(interval)

            all_tasks[(job_id, t_idx)] = machine_vars

            # Each task must be assigned to exactly one machine
            model.Add(sum(is_assigned for (_, _, _, is_assigned, _) in machine_vars.values()) == 1)

            # Precedence: current task starts after previous ends
            if previous_end is not None:
                for m, (start, _, _, is_assigned, _) in machine_vars.items():
                    model.Add(start >= previous_end).OnlyEnforceIf(is_assigned)

            # Define end variable for chaining
            previous_end = model.NewIntVar(0, horizon, f"job{job_id}_task{t_idx}_end")
            model.AddMaxEquality(previous_end, [end for (_, end, _, _, _) in machine_vars.values()])

        job_end_times[job_id] = previous_end

    # --- Machine no-overlap constraints ---
    for m, intervals in machine_to_intervals.items():
        model.AddNoOverlap(intervals)

    # --- Objective selection ---
    if objective_type == "makespan":
        makespan = model.NewIntVar(0, horizon, "makespan")
        model.AddMaxEquality(makespan, list(job_end_times.values()))
        model.Minimize(makespan)
        objective_var = makespan

    elif objective_type == "flow_time":
        total_flow_time = model.NewIntVar(0, horizon * len(jobs), "total_flow_time")
        model.Add(total_flow_time == sum(job_end_times.values()))
        model.Minimize(total_flow_time)
        objective_var = total_flow_time

    elif objective_type == "tardiness":
        tardiness_vars = []
        for job in jobs:
            job_id = job["job_id"]
            due_date = job.get("due_date", horizon)
            tardiness = model.NewIntVar(0, horizon, f"tardiness_{job_id}")
            model.Add(tardiness >= job_end_times[job_id] - due_date)
            tardiness_vars.append(tardiness)
        total_tardiness = model.NewIntVar(0, horizon * len(jobs), "total_tardiness")
        model.Add(total_tardiness == sum(tardiness_vars))
        model.Minimize(total_tardiness)
        objective_var = total_tardiness

    else:
        raise ValueError(f"Unknown objective type: {objective_type}")

    return model, objective_var, all_tasks, objective_type
