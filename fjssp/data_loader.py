import json
import os

def load_instance(filepath):
    """
    Loads an FJSSP instance from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file.
    
    Returns:
        dict: Dictionary containing instance data.
              Includes keys: 'objective', 'machines', and 'jobs'.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Instance file not found: {filepath}")

    with open(filepath, "r") as f:
        data = json.load(f)

    # ✅ Set default objective if missing
    if "objective" not in data:
        data["objective"] = "makespan"

    # ✅ Basic validation
    if "machines" not in data or "jobs" not in data:
        raise ValueError("Invalid instance format: 'machines' and 'jobs' fields are required.")

    return data
