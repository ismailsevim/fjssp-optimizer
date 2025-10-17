# 🏭 fjssp-optimizer

A Python-based optimization framework for solving the **Flexible Job Shop Scheduling Problem (FJSSP)** using **Google OR-Tools (CP-SAT solver)**.  
The project integrates data loading, model building, optimization, and visualization into a unified pipeline.

---

## Features

- **Flexible job shop formulation** with machine flexibility and job precedence constraints  
- **CP-SAT optimization** via Google OR-Tools  
- **Multiple objective functions** supported:
  - Makespan minimization
  - Total flow time
  - Total tardiness
- **JSON-based instance input**
- **Integrated test pipeline** with `pytest`
- **Clean modular structure**:
  - `data_loader.py`: Parses and validates input data  
  - `model_builder.py`: Builds CP-SAT model  
  - `solver.py`: Solves the model and extracts schedules  
  - `visualizer.py`: Gantt chart and results visualization  

---

## Dependencies

## Installation

### 1) Clone the repository
```bash
git clone https://github.com/ismailsevim/fjssp-optimizer.git
cd fjssp-optimizer
```

### 2) Create the environment
```bash
conda env create -f environment.yml
conda activate ortools-env
```

## Usage
Run Tests to verify functionality:
```bash
pytest tests/test_pipeline.py -v
```

Run a sample optimization:
```bash
python main.py --instance data/instance_small_makespan.json --objective makespan
```

