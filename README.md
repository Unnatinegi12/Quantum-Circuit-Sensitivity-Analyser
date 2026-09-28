# Quantum Circuit Sensitivity Analyzer

A Qiskit-based simulation project that studies how controlled changes to quantum gates affect measurement probabilities and output distributions.

## Problem Statement

Quantum circuits can produce different measurement distributions when their gate operations are modified. This project creates a baseline one-qubit circuit, applies controlled gate perturbations, simulates the resulting circuits, and quantifies the change from the baseline.

## What the project does

- Builds a baseline `H`-gate circuit.
- Tests X, Y, Z, S, T, Phase, RX, RY and RZ perturbations.
- Runs reproducible simulations with Qiskit Aer.
- Converts measurement counts into probabilities.
- Calculates sensitivity using the change in `P(1)`.
- Calculates total variation distance between output distributions.
- Adds a depolarizing-noise experiment to study behavior under noisy simulation.
- Produces visualizations for distributions, probabilities and sensitivity.

## Project Structure

```text
quantum-circuit-sensitivity-analyzer/
├── README.md
├── requirements.txt
├── quantum_circuit_sensitivity.ipynb
├── src/
│   └── sensitivity_analyzer.py
├── results/
├── docs/
└── .gitignore
```

## Methodology

```text
Base circuit
     ↓
Gate perturbation
     ↓
Quantum simulation
     ↓
Measurement counts
     ↓
Probability distribution
     ↓
Sensitivity metrics
     ↓
Visualization
```

For the baseline-relative probability metric:

`Sensitivity = |P_base(1) - P_modified(1)|`

The project also calculates total variation distance between the complete baseline and modified output distributions.

## Technologies

- Python
- Qiskit
- Qiskit Aer
- NumPy
- pandas
- Matplotlib
- Jupyter Notebook

## Installation

```bash
git clone <your-repository-url>
cd quantum-circuit-sensitivity-analyzer
pip install -r requirements.txt
```

Then start Jupyter:

```bash
jupyter notebook
```

Open `quantum_circuit_sensitivity.ipynb` and run the cells from top to bottom.

## Reproducibility

The experiments use a fixed simulator seed and a common shot count so that repeated runs are easier to compare.

## Results

The notebook generates:

1. Quantum circuit diagrams
2. Measurement-distribution histograms
3. Probability comparison charts
4. Probability-based sensitivity charts
5. Distribution-distance charts
6. Sensitivity-versus-noise plots

## Limitations

The current implementation uses one-qubit circuits and simulated measurements. The noise experiment is a model-based simulation and should not be interpreted as a direct measurement of a physical quantum processor.

## Future Work

- Extend the analyzer to multi-qubit circuits.
- Compare additional noise models.
- Add parameter sweeps for rotation angles.
- Export experiment results to CSV.
- Add automated experiment configuration.
- Compare ideal simulation, noisy simulation and real quantum-device results when available.

## Author

**Unnati Negi**  
B.Tech CSE – Artificial Intelligence & Machine Learning  
Manipal University Jaipur
