import numpy as np
import pytest

from qcsynth.circuit import (
    circuit_to_diagram,
    circuit_to_qasm,
    parse_circuit,
    parse_qasm,
)
from qcsynth.gates import Gate, load_gate_set
from qcsynth.optimize import optimize_circuit, peephole_pass
from qcsynth.search import Move, run_circuit, verify
from qcsynth.targets import get_target

CLIFFORD = "gates/clifford_t.json"


def test_parse_circuit_formats():
    # Comma-separated bracket format
    ops, n = parse_circuit("H[0], CNOT[0,1], H[0]")
    assert len(ops) == 3
    assert n == 2
    assert ops[0].gate.name == "H" and ops[0].placement == (0,)
    assert ops[1].gate.name == "CNOT" and ops[1].placement == (0, 1)

    # Space notation
    ops2, n2 = parse_circuit("h 0; cx 0 1; h 0")
    assert len(ops2) == 3
    assert n2 == 2

    # Empty
    ops3, n3 = parse_circuit("")
    assert len(ops3) == 0


def test_parse_and_export_qasm():
    qasm_code = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0], q[1];
h q[0];
"""
    ops, n = parse_qasm(qasm_code)
    assert len(ops) == 3
    assert n == 2
    exported = circuit_to_qasm(ops, n)
    assert "OPENQASM 2.0;" in exported
    assert "h q[0];" in exported
    assert "cx q[0], q[1];" in exported


def test_circuit_to_diagram():
    ops, n = parse_circuit("H[0], CNOT[0,1], H[0]")
    diag = circuit_to_diagram(ops, n)
    assert "q0:" in diag and "q1:" in diag
    assert "[H]" in diag
    assert "■" in diag and "X" in diag


def test_peephole_cancellation():
    _, flat, _ = load_gate_set(CLIFFORD)
    # H[0] followed by H[0] cancels to identity
    ops, n = parse_circuit("H[0], H[0]")
    reduced = peephole_pass(ops, flat, n)
    assert len(reduced) == 0

    # H[0], CNOT[0,1], CNOT[0,1], H[0] -> all cancel
    ops2, n2 = parse_circuit("H[0], CNOT[0,1], CNOT[0,1], H[0]")
    reduced2 = peephole_pass(ops2, flat, n2)
    assert len(reduced2) == 0


def test_peephole_gate_merging():
    _, flat, _ = load_gate_set(CLIFFORD)
    # T[0], T[0] -> merges into S[0]
    ops, n = parse_circuit("T[0], T[0]")
    reduced = peephole_pass(ops, flat, n)
    assert len(reduced) == 1
    assert reduced[0].gate.name == "S"
    assert reduced[0].placement == (0,)


def test_optimize_circuit_resynthesis():
    # 7-gate SWAP implementation optimized to 3 CNOTs
    ops, n = parse_circuit("CNOT[0,1], H[0], H[1], CNOT[0,1], H[0], H[1], CNOT[0,1]")
    cnot = Gate("CNOT", get_target("cnot"))
    opt_ops, stats = optimize_circuit(ops, [cnot], n, max_depth=5)
    assert len(opt_ops) == 3
    assert stats.optimized_gates == 3
    assert stats.original_gates == 7
    assert stats.gates_saved == 4
    assert stats.similarity > 1 - 1e-9


def test_optimize_already_optimal():
    # 3 CNOT SWAP is already minimal
    ops, n = parse_circuit("CNOT[0,1], CNOT[1,0], CNOT[0,1]")
    cnot = Gate("CNOT", get_target("cnot"))
    opt_ops, stats = optimize_circuit(ops, [cnot], n, max_depth=3)
    assert len(opt_ops) == 3
    assert stats.gates_saved == 0
    assert stats.similarity > 1 - 1e-9
