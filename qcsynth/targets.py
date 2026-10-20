"""Built-in named target unitaries (little-endian convention)."""

import numpy as np

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
