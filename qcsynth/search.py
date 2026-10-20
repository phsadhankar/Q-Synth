"""Beam search engine for quantum circuit synthesis.

Conventions
-----------
* Little-endian qubit ordering: global qubit 0 is the least significant bit
  of a basis index (same as Qiskit).
* The circuit applies gates one by one; the accumulated matrix is
  V = G_k @ ... @ G_2 @ G_1.
* Success means V equals the target U up to a global phase, measured by the
  similarity  s = |Tr(U^dagger V)| / 2^n  (s = 1  <=>  U ~ V).
"""

from __future__ import annotations

import itertools
import time
from dataclasses import dataclass, field
from functools import reduce

import numpy as np

from .gates import Gate

_QUANT_SCALE = 1e9  # matrix rounding grid for deduplication


@dataclass(frozen=True)
class Move:
    """A gate together with its placement on the global qubits."""

    gate: Gate
    placement: tuple


def embed_gate(gate, n_qubits, placement):
    """Embed a 2^k x 2^k gate acting on k wires into the n-qubit space.

    placement[w] is the global qubit index that gate wire w acts on.
    Untouched qubits act as identity (a Kronecker-style expansion).
    """
    k = gate.qubits
    if k != len(placement):
        raise ValueError("placement length does not match gate size")
    dim = 1 << n_qubits
    placed = placement
    free_qubits = [q for q in range(n_qubits) if q not in placed]
    full = np.zeros((dim, dim), dtype=np.complex128)
    for col in range(dim):
        gcol = sum(((col >> placement[w]) & 1) << w for w in range(k))
        for row in range(dim):
            if any(((row ^ col) >> q) & 1 for q in free_qubits):
                continue  # identity on untouched qubits: bits must agree
            grow = sum(((row >> placement[w]) & 1) << w for w in range(k))
            full[row, col] = gate.matrix[grow, gcol]
    return full


def enumerate_moves(gates, n_qubits):
    """All (gate, placement) pairs: a gate of arity k on any ordered k of n qubits."""
    moves = []
    for gate in gates:
        for placement in itertools.permutations(range(n_qubits), gate.qubits):
            moves.append(Move(gate, placement))
    return moves


@dataclass
class State:
    """A candidate circuit: ops applied in order, matrix, and similarity."""

    ops: list = field(default_factory=list)
    matrix: np.ndarray = None
    score: float = 0.0


def similarity(target, v):
    dim = target.shape[0]
    return abs(np.trace(target.conj().T @ v)) / dim


def quant_key(matrix):
    """Hash key: real and imaginary parts snapped to a fine rounding grid."""
    scale = _QUANT_SCALE
    out = np.empty(matrix.shape + (2,), dtype=np.int64)
    out[..., 0] = np.round(matrix.real * scale)
    out[..., 1] = np.round(matrix.imag * scale)
    return out.astype(np.int64).tobytes()


def beam_search(target, moves, max_depth=8, beam_width=2000, tol=1e-9,
                on_level=None, time_limit=None):
    """Search for a gate sequence reproducing `target` up to global phase.

    Returns (best State, found flag, stats dict).
    """
    dim = target.shape[0]
    n_qubits = dim.bit_length() - 1
    target_h = target.conj().T
    precomputed = [(m, embed_gate(m.gate, n_qubits, m.placement)) for m in moves]
    start = State(matrix=np.eye(dim, dtype=np.complex128),
                  score=similarity(target, np.eye(dim)))
    best, found = start, False
    beam, n_expanded = [start], 0
    t_started = time.perf_counter()
    for depth in range(1, max_depth + 1):
        candidates, seen = [], set()
        for st in beam:
            base = st.matrix
            for move, full in precomputed:
                mat = full @ base
                n_expanded += 1
                s = similarity(target, mat)
                if s >= 1.0 - tol:
                    win = State(st.ops + [move], mat, s)
                    return win, True, _stats(depth, n_expanded, t_started, best)
                key = quant_key(mat)
                if key in seen:
                    continue
                seen.add(key)
                candidates.append(State(st.ops + [move], mat, s))
        candidates.sort(key=lambda c: c.score, reverse=True)
        beam = candidates[:beam_width]
        if beam and best.score < beam[0].score:
            best = beam[0]
        if on_level:
            on_level(depth, best.score, len(candidates))
        if time_limit and time.perf_counter() - t_started > time_limit:
            break
        if not beam:
            break
    return best, found, _stats(0, n_expanded, t_started, best)


def _stats(depth, n_expanded, t_started, best):
    elapsed = time.perf_counter() - t_started
    return {"depth": depth, "expanded": n_expanded,
            "elapsed": elapsed, "best_score": best.score}


def run_circuit(ops, n_qubits):
    """Multiply out the full matrix of a list of Moves."""
    dim = 1 << n_qubits
    return reduce(lambda v, m: embed_gate(m.gate, n_qubits, m.placement) @ v,
                  ops, np.eye(dim, dtype=np.complex128))


def verify(circuit_ops, target, n_qubits):
    """Verify a synthesis result.

    Returns dict with similarity s, global phase phi (so that
    e^{i*phi} * V matches U), and max element error after phase correction.
    """
    v = run_circuit(circuit_ops, n_qubits)
    dim = target.shape[0]
    tr = np.trace(target.conj().T @ v)
    phi = -np.angle(tr)  # target U = e^{i*phi} * V
    s = abs(tr) / dim
    u_adj = np.exp(1j * phi) * v
    err = np.max(np.abs(target - u_adj))
    return {"s": s, "phi": phi, "err": err}
