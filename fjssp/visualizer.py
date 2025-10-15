import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import colorsys

def generate_distinct_colors(n):
    """Generate n visually distinct colors using HLS color space."""
    colors = []
    for i in range(n):
        hue = i / n
        lightness = 0.55 + (0.1 if i % 2 == 0 else -0.1)  # alternate brightness
        saturation = 0.75
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append(rgb)
    return colors


def visualize_schedule(schedule, objective_type="makespan", objective_value=None):
    """
    Visualize the FJSSP schedule as a Gantt chart.

    Args:
        schedule (list of dict): Each dict contains:
            {
                "job_id": int,
                "task_name": str,
                "machine": str,
                "start": float,
                "end": float
            }
        objective_type (str): Type of objective function used (e.g., makespan, flow_time, tardiness)
        objective_value (float): Objective function value to display on chart
    """
    if not schedule:
        print("No schedule to visualize.")
        return

    # === Setup ===
    machines = sorted(list(set(op["machine"] for op in schedule)))
    job_ids = sorted(list(set(op["job_id"] for op in schedule)))
    machine_y = {m: i for i, m in enumerate(machines)}

    # === Generate distinct colors for jobs ===
    job_colors = {j: c for j, c in zip(job_ids, generate_distinct_colors(len(job_ids)))}

    fig, ax = plt.subplots(figsize=(10, 6))

    # === Plot each operation ===
    for op in schedule:
        y = machine_y[op["machine"]]
        color = job_colors[op["job_id"]]
        ax.barh(
            y=y,
            width=op["end"] - op["start"],
            left=op["start"],
            height=0.4,
            color=color,
            edgecolor="black",
            linewidth=1
        )
        ax.text(
            (op["start"] + op["end"]) / 2,
            y,
            f"J{op['job_id']}-{op['task_name']}",
            va="center",
            ha="center",
            fontsize=9,
            color="white",
            fontweight="bold"
        )

    # === Axis setup ===
    ax.set_yticks(range(len(machines)))
    ax.set_yticklabels(machines)
    ax.set_xlabel("Time")

    # === Title includes objective type and value ===
    title_text = f"FJSSP Schedule — Objective: {objective_type}"
    if objective_value is not None:
        title_text += f" = {objective_value}"
    ax.set_title(title_text, fontsize=13, pad=15, fontweight="bold")

    ax.grid(True, axis='x', linestyle='--', alpha=0.5)

    # === Legend ===
    legend_patches = [
        mpatches.Patch(color=job_colors[j], label=f"Job {j}") for j in job_ids
    ]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=8, frameon=True)

    plt.tight_layout()
    plt.show()
