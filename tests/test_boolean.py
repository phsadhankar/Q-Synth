import numpy as np
import pytest

from qcsynth.boolean import (
    bool_expr_to_truth_table,
    format_truth_table,
    parse_bool_expr,
    parse_truth_table,
    truth_table_to_oracle,
)
from qcsynth.gates import Gate, load_gate_set
from qcsynth.search import beam_search, enumerate_moves, verify
from qcsynth.targets import get_target


def test_parse_bool_expr_inference():
    fn, vars_found = parse_bool_expr("x0 and x1")
    assert vars_found == ["x0", "x1"]
    assert fn({"x0": 0, "x1": 0}) == 0
    assert fn({"x0": 1, "x1": 0}) == 0
    assert fn({"x0": 1, "x1": 1}) == 1

    fn2, vars2 = parse_bool_expr("b or not a")
    assert vars2 == ["a", "b"]
    assert fn2({"a": 1, "b": 0}) == 0
    assert fn2({"a": 0, "b": 0}) == 1


def test_bool_expr_syntax_validation():
    with pytest.raises(ValueError, match="syntax"):
        parse_bool_expr("x0 and")
    with pytest.raises(ValueError, match="empty"):
        parse_bool_expr("  ")
    with pytest.raises(ValueError, match="Unsupported syntax"):
        parse_bool_expr("__import__('os')")


def test_bool_expr_to_truth_table():
    # XOR: x0 ^ x1
    tt, vars_found = bool_expr_to_truth_table("x0 ^ x1")
    assert vars_found == ["x0", "x1"]
    # Little-endian rows:
    # k=0: x0=0, x1=0 -> 0
    # k=1: x0=1, x1=0 -> 1
    # k=2: x0=0, x1=1 -> 1
    # k=3: x0=1, x1=1 -> 0
    assert list(tt) == [0, 1, 1, 0]


def test_parse_truth_table_formats():
    # Bitstring
    tt1, vars1 = parse_truth_table("0110")
    assert list(tt1) == [0, 1, 1, 0]
    assert vars1 == ["x0", "x1"]

    # Comma-separated
    tt2, _ = parse_truth_table("0, 1, 1, 0")
    assert list(tt2) == [0, 1, 1, 0]

    # Dict
    tt3, _ = parse_truth_table({"00": 0, "01": 1, "10": 1, "11": 0})
    assert list(tt3) == [0, 1, 1, 0]

    # Reversible mapping
    tt4, _ = parse_truth_table("0->1, 1->0, 2->3, 3->2")
    assert list(tt4) == [1, 0, 3, 2]


def test_truth_table_rejects_invalid():
    with pytest.raises(ValueError, match="power of 2"):
        parse_truth_table("011")  # length 3
    with pytest.raises(ValueError):
        parse_truth_table("")


def test_truth_table_to_bitflip_oracle():
    # Identity f(x0) = x0 -> bitflip oracle is CNOT[0, 1]
    mat, n_qubits = truth_table_to_oracle([0, 1], oracle_mode="bitflip")
    assert n_qubits == 2
    assert np.allclose(mat, get_target("cnot"))


def test_truth_table_to_phase_oracle():
    # f(x0) = x0 -> phase oracle is Z
    mat, n_qubits = truth_table_to_oracle([0, 1], oracle_mode="phase")
    assert n_qubits == 1
    assert np.allclose(mat, get_target("z"))

    # f(x0, x1) = x0 & x1 -> phase oracle is CZ
    mat2, n2 = truth_table_to_oracle([0, 0, 0, 1], oracle_mode="phase")
    assert n2 == 2
    assert np.allclose(mat2, get_target("cz"))


def test_truth_table_permutation_oracle():
    # Swap elements 1 and 2
    mat, n = truth_table_to_oracle([0, 2, 1, 3], oracle_mode="permutation")
    assert n == 2
    assert np.allclose(mat @ mat, np.eye(4))


def test_format_truth_table():
    formatted = format_truth_table(np.array([0, 1, 1, 0]), ["x0", "x1"])
    assert "x1" in formatted and "x0" in formatted and "f" in formatted
    assert "0   0 |  0" in formatted
    assert "0   1 |  1" in formatted


def test_synthesize_boolean_xor():
    tt, _ = bool_expr_to_truth_table("x0 ^ x1")
    target, n = truth_table_to_oracle(tt, oracle_mode="bitflip")
    cnot = Gate("CNOT", get_target("cnot"))
    moves = enumerate_moves([cnot], n)
    state, found, _ = beam_search(target, moves, max_depth=3)
    assert found
    assert len(state.ops) == 2
    v = verify(state.ops, target, n)
    assert v["s"] > 1 - 1e-9
