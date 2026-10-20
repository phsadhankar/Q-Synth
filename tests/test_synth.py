import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from qcsynth.gates import Gate, _instantiate, load_gate_set  # noqa: E402
from qcsynth.search import (  # noqa: E402
    beam_search,
    embed_gate,
    enumerate_moves,
    run_circuit,
    verify,
)
from qcsynth.targets import get_target  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
CLIFFORD = os.path.join(ROOT, "gates", "clifford_t.json")
UNIVERSAL = os.path.join(ROOT, "gates", "universal_rxy.json")


# ---------------------------------------------------------------- embedding

def test_embed_cnot_q0_q1_is_standard():
    cnot = Gate("CNOT", get_target("cnot"))
    assert np.allclose(embed_gate(cnot, 2, (0, 1)), get_target("cnot"))


def test_embed_cnot_reversed_swaps_control_and_target():
    cnot = Gate("CNOT", get_target("cnot"))
    # placement (1,0): control wire -> global qubit 1, target wire -> qubit 0,
    # i.e. flip qubit 0 when qubit 1 is 1
    expected = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
                        dtype=complex)
    assert np.allclose(embed_gate(cnot, 2, (1, 0)), expected)


def test_embed_h_on_qubit1_of_two():
    h = Gate("H", get_target("h"))
    full = embed_gate(h, 2, (1,))
    expect = np.kron(get_target("h"), np.eye(2))  # qubit 1 = most significant = left
    assert np.allclose(full, expect)


# ---------------------------------------------------------------- gate JSON

def test_load_clifford_preset():
    gates, flat, doc = load_gate_set(CLIFFORD)
    assert {"x", "y", "z", "h", "s", "t", "cnot", "cz"} == {k.lower() for k in gates}
    assert doc.get("name")
    assert all(np.allclose(g.matrix.conj().T @ g.matrix, np.eye(g.matrix.shape[0]),
                           atol=1e-9) for g in flat)


def test_gate_name_filter():
    gates, flat, _ = load_gate_set(CLIFFORD, names=["cnot"])
    assert {k.lower() for k in gates} == {"cnot"}
    assert len(flat) == 1


def test_parameterized_gate_instances_and_labels():
    rx = [g for pg in [{"name": "RX", "qubits": 1,
                        "matrix": [["cos(theta/2)", "-I*sin(theta/2)"],
                                   ["-I*sin(theta/2)", "cos(theta/2)"]],
                        "params": {"theta": ["pi/2", "-pi"]}}]
          for g in _instantiate(pg)]
    assert len(rx) == 2
    labels = {g.name for g in rx}
    assert labels == {"RX(pi/2)", "RX(-pi)"}
    want = np.sqrt(0.5) * np.array([[1, -1j], [-1j, 1]], dtype=complex)
    got = [g.matrix for g in rx if g.name == "RX(pi/2)"][0]
    assert np.allclose(got, want)


def test_non_unitary_gate_rejected():
    with pytest.raises(ValueError):
        _instantiate({"name": "Bad", "qubits": 1,
                      "matrix": [[1, 2], [3, 4]]})


# ---------------------------------------------------------------- search

def synthesize(target, gates, max_depth, beam=2000):
    n = target.shape[0].bit_length() - 1
    moves = enumerate_moves(gates, n)
    state, found, _ = beam_search(target, moves, max_depth=max_depth,
                                  beam_width=beam)
    return state, found


def test_swap_from_three_cnots():
    state, found = synthesize(get_target("swap"), [Gate("CNOT", get_target("cnot"))],
                              max_depth=3)
    assert found
    assert len(state.ops) == 3
    ops = {op.placement for op in state.ops}
    assert ops == {(0, 1), (1, 0)}
    v = verify(state.ops, get_target("swap"), 2)
    assert v["s"] > 1 - 1e-9 and v["err"] < 1e-9


def test_swap_from_clifford_preset():
    _, flat, _ = load_gate_set(CLIFFORD)
    state, found = synthesize(get_target("swap"), flat, max_depth=4)
    assert found
    assert len(state.ops) <= 3  # search must not find something longer
    v = verify(state.ops, get_target("swap"), 2)
    assert v["s"] > 1 - 1e-9


def test_hadamard_from_discrete_rotations():
    _, flat, _ = load_gate_set(UNIVERSAL)
    state, found = synthesize(get_target("h"), flat, max_depth=3)
    assert found
    v = verify(state.ops, get_target("h"), 1)
    assert v["s"] > 1 - 1e-9 and v["err"] < 1e-9


def test_cz_from_h_and_cnot():
    """CZ = (I x H) CNOT (I x H); only CNOT and H allowed so it is non-trivial."""
    _, flat, _ = load_gate_set(CLIFFORD, names=["cnot", "h"])
    state, found = synthesize(get_target("cz"), flat, max_depth=3)
    assert found
    v = verify(state.ops, get_target("cz"), 2)
    assert v["s"] > 1 - 1e-9 and v["err"] < 1e-9


def test_run_circuit_matches_search_matrix():
    _, flat, _ = load_gate_set(CLIFFORD)
    state, found = synthesize(get_target("swap"), flat, max_depth=4)
    assert found
    mat = run_circuit(state.ops, 2)
    assert np.allclose(mat, state.matrix)


def test_verify_handles_global_phase():
    from qcsynth.search import Move

    h = Gate("H", get_target("h"))
    target = np.exp(1j * 0.7) * get_target("h")  # H with extra phase
    rep = verify((Move(h, (0,)),), target, 1)
    assert rep["s"] > 1 - 1e-12
    assert abs(rep["phi"] - 0.7) < 1e-12 or abs(rep["phi"] - 0.7 - 2 * math.pi) < 1e-12
    assert rep["err"] < 1e-12
