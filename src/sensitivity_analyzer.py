"""
Quantum Circuit Sensitivity Analyzer
Reusable functions for building, simulating, and comparing quantum circuits.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


DEFAULT_SHOTS = 2000


def create_circuit(gate: Optional[str] = None, angle: float = np.pi / 4) -> QuantumCircuit:
    """Create a one-qubit circuit with H followed by an optional perturbation gate."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)

    if gate == "X":
        qc.x(0)
    elif gate == "Y":
        qc.y(0)
    elif gate == "Z":
        qc.z(0)
    elif gate == "S":
        qc.s(0)
    elif gate == "T":
        qc.t(0)
    elif gate == "Phase":
        qc.p(angle, 0)
    elif gate == "RX":
        qc.rx(angle, 0)
    elif gate == "RY":
        qc.ry(angle, 0)
    elif gate == "RZ":
        qc.rz(angle, 0)
    elif gate is not None:
        raise ValueError(f"Unsupported gate: {gate}")

    qc.measure(0, 0)
    return qc


def build_experiments(angle: float = np.pi / 4) -> List[Tuple[str, QuantumCircuit]]:
    """Return the baseline and a set of gate-perturbation experiments."""
    experiments = [
        ("Base", create_circuit()),
        ("H + X", create_circuit("X")),
        ("H + Y", create_circuit("Y")),
        ("H + Z", create_circuit("Z")),
        ("H + S", create_circuit("S")),
        ("H + T", create_circuit("T")),
        ("H + Phase", create_circuit("Phase", angle)),
        ("H + RX", create_circuit("RX", angle)),
        ("H + RY", create_circuit("RY", angle)),
        ("H + RZ", create_circuit("RZ", angle)),
    ]
    return experiments


def run_circuit(
    circuit: QuantumCircuit,
    shots: int = DEFAULT_SHOTS,
    noise_probability: Optional[float] = None,
    seed: int = 42,
) -> Dict[str, int]:
    """Run a circuit on AerSimulator, optionally with depolarizing noise."""
    if noise_probability is None or noise_probability <= 0:
        simulator = AerSimulator()
    else:
        error = depolarizing_error(noise_probability, 1)
        noise_model = NoiseModel()
        noise_model.add_all_qubit_quantum_error(
            error,
            ["h", "x", "y", "z", "s", "t", "p", "rx", "ry", "rz"],
        )
        simulator = AerSimulator(noise_model=noise_model)

    result = simulator.run(
        circuit,
        shots=shots,
        seed_simulator=seed,
    ).result()

    return result.get_counts()


def probabilities(counts: Dict[str, int], shots: int) -> Dict[str, float]:
    """Convert counts into probabilities for 0 and 1."""
    return {
        "0": counts.get("0", 0) / shots,
        "1": counts.get("1", 0) / shots,
    }


def total_variation_distance(
    p: Dict[str, float], q: Dict[str, float]
) -> float:
    """Calculate total variation distance between two discrete distributions."""
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def probability_sensitivity(base_p1: float, modified_p1: float) -> float:
    """Absolute change in probability of measuring |1>."""
    return abs(base_p1 - modified_p1)


def analyze_experiments(
    experiments: Iterable[Tuple[str, QuantumCircuit]],
    shots: int = DEFAULT_SHOTS,
    noise_probability: Optional[float] = None,
    seed: int = 42,
) -> List[dict]:
    """Run experiments and calculate baseline-relative sensitivity metrics."""
    experiments = list(experiments)
    raw = []

    for name, circuit in experiments:
        counts = run_circuit(
            circuit,
            shots=shots,
            noise_probability=noise_probability,
            seed=seed,
        )
        raw.append((name, circuit, counts, probabilities(counts, shots)))

    base_prob = raw[0][3]

    rows = []
    for name, circuit, counts, probs in raw:
        rows.append(
            {
                "circuit": name,
                "p0": probs["0"],
                "p1": probs["1"],
                "probability_sensitivity": probability_sensitivity(
                    base_prob["1"], probs["1"]
                ),
                "distribution_distance": total_variation_distance(
                    base_prob, probs
                ),
                "counts": counts,
                "circuit_object": circuit,
            }
        )

    return rows


def create_noise_levels(
    experiments: Iterable[Tuple[str, QuantumCircuit]],
    levels: Iterable[float],
    shots: int = DEFAULT_SHOTS,
    seed: int = 42,
) -> List[dict]:
    """Evaluate the experiments at several depolarizing-noise levels."""
    records = []
    for level in levels:
        rows = analyze_experiments(
            experiments,
            shots=shots,
            noise_probability=level,
            seed=seed,
        )
        for row in rows:
            row = dict(row)
            row["noise_probability"] = level
            records.append(row)
    return records
