# fjssp-optimizer

A Python-based optimization framework for solving the **Flexible Job Shop Scheduling Problem (FJSSP)** using **Google OR-Tools (CP-SAT solver)**.  
The project integrates data loading, model building, optimization, and visualization into a unified pipeline.

---

## Features

- **Flexible job shop formulation** with machine flexibility and job precedence constraints  
- **CP-SAT optimization** via Google OR-Tools  
- **Multiple objective functions** supported:
  - Makespan minimization: To find a schedule that completes all operations and jobs in the shortest possible time, measured from the start of the first operation to the completion of the last one.
  - Total flow time: To find a schedule that minimizes the sum of the flow times for all jobs, where a job's flow time is the difference between its completion time and its release time.
  - Total tardiness: To find a schedule that minimizes the sum of the tardiness values for all jobs, where a job's tardiness is the maximum of zero or the difference between its completion time and its due date.
- **JSON-based instance input**
- **Integrated test pipeline** with `pytest`
- **Clean modular structure**:
  - `data_loader.py`: Parses and validates input data  
  - `model_builder.py`: Builds CP-SAT model  
  - `solver.py`: Solves the model and extracts schedules  
  - `visualizer.py`: Gantt chart and results visualization  

---

## Installation and Dependencies
This project uses Conda to manage the required dependencies. The complete environment is defined in the `environment.yml` file.

### Clone the repository
```bash
git clone https://github.com/ismailsevim/fjssp-optimizer.git
cd fjssp-optimizer
```

### Quick setup
You can create and activate the required Conda environment, named fjssp-optimizer-env, using a single command:
```bash
conda env create -f environment.yml
conda activate fjssp-optimizer-env
```

### Key Dependencies

The environment includes all necessary packages for running the Flexible Job Shop Scheduling Problem (FJSSP) optimizer:
- `Python==3.11`
- `numpy`, `pandas`, and `matplotlib` for data handling and result visualization.
- `ortools==9.14.6206`: The core constraint programming solver library.
- `pytest==8.4.2`: Used for running the automated test suite.

## Usage
Run Tests to verify functionality:
```bash
pytest tests/test_pipeline.py -v
```

Run a sample optimization:
```bash
python main.py --instance data/instance_medium.json --objective makespan
```

Different objective functions:
```bash
python main.py --instance data/instance_medium.json --objective makespan
python main.py --instance data/instance_medium.json --objective flow_time
python main.py --instance data/instance_medium.json --objective tardiness
```

### Display
The commands for different objective functions generate and display a Gantt Chart. An example output is shown below:

To skip the generation and display of the Gantt chart (useful for running tests, batch processing, or on environments without a display), use the `--no_plot` flag. The solution metrics will still be printed to the console. Example:
```bash
python main.py --instance data/instance_medium.json --objective makespan --no_plot
```






