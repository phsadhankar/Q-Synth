"""Circuit optimization engine: peephole rewriting and synthesizer-based resynthesis.

This module reduces a user-given circuit to fewer gates using a specified
set of allowed gates.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

from .gates import Gate
from .search import Move, beam_search, embed_gate, enumerate_moves, run_circuit, similarity, verify


@dataclass
class OptimizationStats:
    """Statistics about an optimization run."""

    original_gates: int
    optimized_gates: int
    gates_saved: int
    reduction_pct: float
    elapsed_seconds: float
    similarity: float
    global_phase: float
    max_error: float
    passes_run: list[str] = field(default_factory=list)


def gates_commute(
    op1: Move, op2: Move, n_qubits: int, precomputed: dict | None = None
) -> bool:
    """Return True if op1 and op2 commute in the n-qubit space."""
    p1 = set(op1.placement)
    p2 = set(op2.placement)
    if p1.isdisjoint(p2):
        return True

    # Check via matrix product
    if precomputed is not None and (op1, n_qubits) in precomputed:
        m1 = precomputed[(op1, n_qubits)]
    else:
        m1 = embed_gate(op1.gate, n_qubits, op1.placement)

    if precomputed is not None and (op2, n_qubits) in precomputed:
        m2 = precomputed[(op2, n_qubits)]
    else:
        m2 = embed_gate(op2.gate, n_qubits, op2.placement)

    diff = m1 @ m2 - m2 @ m1
    return bool(np.max(np.abs(diff)) < 1e-9)


def _is_identity(mat: np.ndarray, tol: float = 1e-9) -> bool:
    """Return True if mat is equal to identity up to global phase."""
    dim = mat.shape[0]
    tr = np.trace(mat)
    s = abs(tr) / dim
    return bool(s >= 1.0 - tol)


def peephole_pass(
    ops: list[Move],
    allowed_gates: Sequence[Gate],
    n_qubits: int,
    tol: float = 1e-9,
) -> list[Move]:
    """Apply rule-based cancellations and gate merging across commuting gates."""
    current = list(ops)
    precomputed: dict = {}

    def get_mat(op: Move) -> np.ndarray:
        k = (op, n_qubits)
        if k not in precomputed:
            precomputed[k] = embed_gate(op.gate, n_qubits, op.placement)
        return precomputed[k]

    changed = True
    while changed:
        changed = False

        # 1. Eliminate any identity operations
        filtered = []
        for op in current:
            if _is_identity(get_mat(op), tol=tol):
                changed = True
            else:
                filtered.append(op)
        current = filtered
        if not current:
            break

        # 2. Look for pairs (i, j) that can commute adjacent and cancel or merge
        n_ops = len(current)
        pair_to_remove = None
        pair_to_merge = None

        for i in range(n_ops):
            m_i = current[i]
            mat_i = get_mat(m_i)

            # Look forward at j > i
            can_commute = True
            for j in range(i + 1, n_ops):
                m_j = current[j]
                if not gates_commute(m_i, m_j, n_qubits, precomputed):
                    # Check if they share the same placement or overlap
                    # Product of m_j @ m_i
                    mat_j = get_mat(m_j)
                    prod = mat_j @ mat_i
                    if _is_identity(prod, tol=tol):
                        pair_to_remove = (i, j)
                        break

                    # Check if they can merge into a single allowed gate
                    for cand in allowed_gates:
                        if cand.qubits == m_i.gate.qubits and m_i.placement == m_j.placement:
                            m_cand = embed_gate(cand, n_qubits, m_i.placement)
                            tr = np.trace(m_cand.conj().T @ prod)
                            if (abs(tr) / (1 << n_qubits)) >= 1.0 - tol:
                                pair_to_merge = (i, j, Move(cand, m_i.placement))
                                break
                    if pair_to_merge is not None:
                        break

                    can_commute = False
                    break

                # If m_j commutes past all intermediate gates, check if m_j and m_i cancel
                mat_j = get_mat(m_j)
                prod = mat_j @ mat_i
                if _is_identity(prod, tol=tol):
                    pair_to_remove = (i, j)
                    break

                # Check if m_j and m_i can merge into a single allowed gate
                if m_i.placement == m_j.placement:
                    for cand in allowed_gates:
                        if cand.qubits == m_i.gate.qubits:
                            m_cand = embed_gate(cand, n_qubits, m_i.placement)
                            tr = np.trace(m_cand.conj().T @ prod)
                            if (abs(tr) / (1 << n_qubits)) >= 1.0 - tol:
                                pair_to_merge = (i, j, Move(cand, m_i.placement))
                                break
                    if pair_to_merge is not None:
                        break

            if pair_to_remove is not None or pair_to_merge is not None:
                break

        if pair_to_remove is not None:
            i, j = pair_to_remove
            current = [op for idx, op in enumerate(current) if idx not in (i, j)]
            changed = True
            continue

        if pair_to_merge is not None:
            i, j, new_move = pair_to_merge
            new_ops = []
            for idx, op in enumerate(current):
                if idx == i:
                    new_ops.append(new_move)
                elif idx == j:
                    continue
                else:
                    new_ops.append(op)
            current = new_ops
            changed = True
            continue

    return current


def optimize_circuit(
    ops: Sequence[Move],
    allowed_gates: Sequence[Gate],
    n_qubits: int,
    max_depth: int = 8,
    beam_width: int = 2000,
    tol: float = 1e-9,
    window_size: int = 4,
    time_limit: float | None = None,
) -> tuple[list[Move], OptimizationStats]:
    """Optimize a quantum circuit to fewer gates using allowed gates.

    Uses:
    1. Commutation-aware algebraic peephole reduction (cancellation and merging).
    2. Global beam-search resynthesis if circuit is short enough.
    3. Sliding-window block resynthesis for longer circuits.
    4. Full matrix verification against the original unitary.

    Returns (optimized_ops, stats).
    """
    t_start = time.perf_counter()
    original_ops = list(ops)
    n_orig = len(original_ops)

    if n_qubits == 0 or n_orig == 0:
        stats = OptimizationStats(
            original_gates=0,
            optimized_gates=0,
            gates_saved=0,
            reduction_pct=0.0,
            elapsed_seconds=time.perf_counter() - t_start,
            similarity=1.0,
            global_phase=0.0,
            max_error=0.0,
            passes_run=["trivial"],
        )
        return [], stats

    target_unitary = run_circuit(original_ops, n_qubits)
    passes_run = []

    # Pass 1: Peephole reduction
    current = peephole_pass(original_ops, allowed_gates, n_qubits, tol=tol)
    if len(current) < n_orig:
        passes_run.append(f"peephole ({n_orig} -> {len(current)})")

    # If already reduced to 0 gates (identity circuit)
    if not current:
        v = verify(current, target_unitary, n_qubits)
        stats = OptimizationStats(
            original_gates=n_orig,
            optimized_gates=0,
            gates_saved=n_orig,
            reduction_pct=100.0,
            elapsed_seconds=time.perf_counter() - t_start,
            similarity=v["s"],
            global_phase=v["phi"],
            max_error=v["err"],
            passes_run=passes_run,
        )
        return [], stats

    # Generate moves for allowed gates
    moves = enumerate_moves(allowed_gates, n_qubits)

    # Pass 2: Global beam-search resynthesis
    # If current circuit is within reach of search depth, try full synthesis
    cur_len = len(current)
    search_depth = min(max_depth, cur_len - 1 if cur_len > 1 else max_depth)

    # Even if cur_len <= 1, check if 0 or 1 gate reproduces target
    rem_time = (time_limit - (time.perf_counter() - t_start)) if time_limit else None
    if search_depth >= 0:
        res_state, found, _ = beam_search(
            target_unitary,
            moves,
            max_depth=search_depth,
            beam_width=beam_width,
            tol=tol,
            time_limit=rem_time,
        )
        if found and len(res_state.ops) < cur_len:
            passes_run.append(f"global_resynthesis ({cur_len} -> {len(res_state.ops)})")
            current = list(res_state.ops)
            cur_len = len(current)

    # Pass 3: Sliding window resynthesis if current circuit length > 2
    cur_len = len(current)
    if cur_len > 2 and window_size >= 2:
        max_w = min(window_size, cur_len)
        changed_win = True
        while changed_win:
            changed_win = False
            cur_len = len(current)
            for w in range(max_w, 1, -1):
                if w >= cur_len:
                    continue
                for i in range(cur_len - w + 1):
                    sub_slice = current[i : i + w]
                    # Compute sub-circuit unitary on n_qubits
                    sub_u = run_circuit(sub_slice, n_qubits)

                    rem_t = (
                        (time_limit - (time.perf_counter() - t_start)) if time_limit else None
                    )
                    if rem_t is not None and rem_t <= 0:
                        break

                    sub_state, sub_found, _ = beam_search(
                        sub_u,
                        moves,
                        max_depth=w - 1,
                        beam_width=beam_width,
                        tol=tol,
                        time_limit=rem_t,
                    )
                    if sub_found and len(sub_state.ops) < w:
                        passes_run.append(
                            f"window_resynthesis[w={w}] ({w} -> {len(sub_state.ops)})"
                        )
                        current = current[:i] + list(sub_state.ops) + current[i + w :]
                        # Re-run peephole on the updated circuit
                        current = peephole_pass(current, allowed_gates, n_qubits, tol=tol)
                        changed_win = True
                        break
                if changed_win:
                    break

    # Verification against original target unitary
    v = verify(current, target_unitary, n_qubits)
    n_opt = len(current)
    saved = n_orig - n_opt
    pct = (saved / n_orig * 100.0) if n_orig > 0 else 0.0

    stats = OptimizationStats(
        original_gates=n_orig,
        optimized_gates=n_opt,
        gates_saved=saved,
        reduction_pct=pct,
        elapsed_seconds=time.perf_counter() - t_start,
        similarity=v["s"],
        global_phase=v["phi"],
        max_error=v["err"],
        passes_run=passes_run,
    )

    return current, stats
