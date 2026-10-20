"""Built-in named target unitaries and target input parsing."""

import json

import numpy as np

from .gates import check_unitary, parse_matrix

_I2 = np.eye(2, dtype=np.complex128)

_H = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)
_X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
_Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
_Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
_S = np.array([[1, 0], [0, 1j]], dtype=np.complex128)
_T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=np.complex128)

_CNOT = np.array([[1, 0, 0, 0],
                  [0, 0, 0, 1],
                  [0, 0, 1, 0],
                  [0, 1, 0, 0]], dtype=np.complex128)  # flip qubit 1 if qubit 0 is 1
_CZ = np.array([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, -1]], dtype=np.complex128)
_SWAP = np.array([[1, 0, 0, 0],
                  [0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 1]], dtype=np.complex128)

TARGETS = {
    "i": _I2, "x": _X, "y": _Y, "z": _Z, "h": _H, "s": _S, "t": _T,
    "cnot": _CNOT, "cz": _CZ, "swap": _SWAP,
}


def get_target(name):
    key = name.lower()
    if key not in TARGETS:
        raise ValueError(
            f"Unknown target {name!r}; available: {', '.join(sorted(TARGETS))}")
    return TARGETS[key].copy()


def parse_matrix_spec(text):
    """Parse an inline JSON matrix as a target unitary.

    Elements use the same format as gate-set JSONs: numbers, expression
    strings ("sqrt2/2", "0.5-0.3j") or [re, im] pairs.  Validates that the
    result is a square, unitary 2^n x 2^n matrix.
    """
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Target {text.strip()[:40]!r} is neither a built-in name nor "
            f"valid JSON: {exc}") from exc
    if not isinstance(raw, list) or not (raw and isinstance(raw[0], list)):
        raise ValueError("Inline target must be a JSON array of rows")
    try:
        mat = parse_matrix(raw)
    except ValueError as exc:
        raise ValueError(f"Bad inline target matrix: {exc}") from exc
    n_qubits_of(mat)
    try:
        check_unitary(mat, tol=1e-8, what="inline target")
    except ValueError:
        raise ValueError("Inline target matrix must be unitary "
                         "(the final circuit matrix is unitary)")
    return mat


def resolve_target(text):
    """--matrix value: either a built-in name or an inline JSON matrix.

    Returns (matrix, display label).
    """
    key = text.strip().lower()
    if key in TARGETS:
        return get_target(key), key.upper()
    return parse_matrix_spec(text), "inline matrix"


def n_qubits_of(matrix):
    dim = matrix.shape[0]
    n = dim.bit_length() - 1
    if (1 << n) != dim or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"Target must be 2^n x 2^n square; got {matrix.shape}")
    return n


def load_matrix_file(path):
    """Load a 2^n x 2^n unitary from .npy or text/CSV (complex supported).

    Text files may contain plain numbers, "a+bj" strings, or the
    "(a+bj)" format written by numpy.savetxt.
    """
    if path.lower().endswith(".npy"):
        mat = np.load(path)
    else:
        delim = "," if path.lower().endswith(".csv") else None
        try:
            mat = np.loadtxt(path, delimiter=delim, dtype=complex)
        except ValueError:
            with open(path, encoding="utf-8") as fh:
                raw = fh.read().replace("(", "").replace(")", "")
            from io import StringIO
            mat = np.loadtxt(StringIO(raw), delimiter=delim, dtype=complex)
    return np.asarray(mat, dtype=np.complex128)
