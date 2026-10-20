"""Gate definitions and gate-set JSON parsing.

A gate set is described by a JSON file:

    {
      "name": "preset display name",
      "gates": [
        {"name": "H", "qubits": 1,
         "matrix": [[0.5, 0.5], [0.5, -0.5]]},
        {"name": "RX", "qubits": 1,
         "matrix": [["cos(theta/2)", "-I*sin(theta/2)"],
                    ["-I*sin(theta/2)", "cos(theta/2)"]],
         "params": {"theta": ["pi/2", "pi", "-pi/2", "-pi"]}}
      ]
    }

Each matrix element may be
  * a JSON number       (imaginary part 0),
  * a JSON string       (short expression, e.g. "sqrt2/2" or "1-0.5j";
                         "^" is accepted for "**"),
  * a two-element array ([real, imag]).

A gate whose "matrix" contains parameter names must also list "params":
for every combination of allowed parameter values one concrete gate is
generated (e.g. RX(pi/4), RX(pi/2), ...).  This keeps the search space
finite.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass

import numpy as np

from .expr import evaluate, evaluate_real


@dataclass(frozen=True)
class Gate:
    """A concrete (fully instantiated) quantum gate."""

    name: str
    matrix: np.ndarray

    @property
    def qubits(self):
        n = self.matrix.shape[0]
        return n.bit_length() - 1  # n == 2**qubits

    def label(self, placement=None, n_qubits=None):
        """Human-readable label; includes qubit placement when ambiguous."""
        if placement is not None and n_qubits is not None:
            if n_qubits > 1 or self.qubits > 1:
                qs = ",".join(str(q) for q in placement)
                return f"{self.name}[{qs}]"
        return self.name


def _parse_element(el, extra_vars=None):
    if isinstance(el, (list, tuple)) and len(el) == 2:
        return complex(evaluate_real(el[0], extra_vars),
                       evaluate_real(el[1], extra_vars))
    return evaluate(el, extra_vars)


def parse_matrix(raw, extra_vars=None):
    rows = len(raw)
    for row in raw:
        if len(row) != rows:
            raise ValueError("Gate matrix must be square")
    mat = np.empty((rows, rows), dtype=np.complex128)
    for i, row in enumerate(raw):
        for j, el in enumerate(row):
            mat[i, j] = _parse_element(el, extra_vars)
    return mat


def check_unitary(mat, tol=1e-9, what="gate"):
    dim = mat.shape[0]
    if not np.allclose(mat.conj().T @ mat, np.eye(dim), rtol=0, atol=tol):
        raise ValueError(f"{what} is not unitary")


def _fmt_angle(theta):
    """Render an angle nicely when it is a small multiple of pi/8."""
    names = ["0", "pi/8", "pi/4", "3*pi/8", "pi/2",
             "5*pi/8", "3*pi/4", "7*pi/8", "pi"]
    k = round(theta / (math.pi / 8))
    if abs(theta - k * (math.pi / 8)) < 1e-9 and -8 <= k <= 8:
        sign = "" if k >= 0 else "-"
        return sign + names[abs(k)]
    return f"{theta:.6f}"


def _instantiate(gate_def):
    """Turn one JSON gate definition into a list of concrete Gates."""
    name = gate_def["name"]
    dim = int(gate_def["qubits"])
    if (1 << dim) != len(gate_def["matrix"]):
        raise ValueError(f"Gate {name!r}: 'qubits' does not match matrix size")
    params = gate_def.get("params")
    if not params:
        mat = parse_matrix(gate_def["matrix"])
        check_unitary(mat, what=f"gate {name!r}")
        return [Gate(name, mat)]
    # Parameterized gate: build every (param -> value) combination.
    pnames = list(params)
    values = [[evaluate_real(v) for v in params[p]] for p in pnames]
    gates = []
    for combo in itertools.product(*values):
        env = dict(zip(pnames, combo))
        mat = parse_matrix(gate_def["matrix"], env)
        if len(pnames) == 1:
            suffix = _fmt_angle(combo[0])
        else:
            suffix = ",".join(f"{p}={_fmt_angle(v)}" for p, v in zip(pnames, combo))
        check_unitary(mat, what=f"gate {name}({suffix})")
        gates.append(Gate(f"{name}({suffix})", mat))
    if not gates:
        raise ValueError(f"Gate {name!r}: no parameter values were provided")
    return gates


def load_gate_set(path, names=None):
    """Load a gate-set JSON file.

    names: optional iterable of gate base names to keep (case-insensitive).
    Returns (gate dict base_name -> list[Gate], flat list of Gates, document).
    """
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    gates = {}
    for gate_def in doc.get("gates", []):
        base = gate_def["name"]
        if base in gates:
            raise ValueError(f"Duplicate gate name {base!r} in gate set")
        if names is not None and base.lower() not in {n.lower() for n in names}:
            continue
        gates[base] = _instantiate(gate_def)
    if not gates:
        avail = ", ".join(g["name"] for g in doc.get("gates", []))
        raise ValueError(f"No gates matched the requested names (available: {avail})")
    flat = [g for lst in gates.values() for g in lst]
    return gates, flat, doc
