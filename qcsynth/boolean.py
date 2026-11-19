"""Boolean function and truth table parsing and quantum oracle generation.

Conventions
-----------
* Little-endian qubit ordering: qubit 0 is the least significant bit (LSB).
  In truth table rows, variable x0 corresponds to bit 0, x1 to bit 1, etc.
* Oracle modes:
  - 'bitflip': standard quantum oracle |x>|y> -> |x>|y ^ f(x)>, requiring n+1 qubits
    (inputs x on qubits 0..n-1, target y on qubit n).
  - 'phase': diagonal oracle |x> -> (-1)^f(x) |x>, requiring n qubits.
  - 'permutation': reversible truth table / permutation |x> -> |f(x)>, requiring n qubits.
"""

from __future__ import annotations

import ast
import json
import math
import re
from typing import Callable, Iterable

import numpy as np

from .gates import check_unitary

_SAFE_NODES = (
    ast.Expression,
    ast.Name,
    ast.Constant,
    ast.UnaryOp,
    ast.BinOp,
    ast.BoolOp,
    ast.Compare,
    ast.Load,
    # Unary operators
    ast.Not,
    ast.Invert,
    ast.UAdd,
    ast.USub,
    # Binary operators
    ast.BitAnd,
    ast.BitOr,
    ast.BitXor,
    ast.Add,
    ast.Mult,
    ast.Sub,
    # Boolean operators
    ast.And,
    ast.Or,
    # Comparisons
    ast.Eq,
    ast.NotEq,
)


def _validate_ast(node: ast.AST) -> None:
    """Ensure the AST only contains safe boolean/arithmetic operations."""
    for child in ast.walk(node):
        if not isinstance(child, _SAFE_NODES):
            raise ValueError(f"Unsupported syntax in boolean expression: {type(child).__name__}")


def _infer_var_names(tree: ast.AST) -> list[str]:
    """Find all variable names in AST and order them naturally (x0, x1... or a, b...)."""
    names = set()
    for child in ast.walk(tree):
        if isinstance(child, ast.Name):
            # Ignore built-in True/False/None names if represented as Name
            if child.id not in ("True", "False", "None"):
                names.add(child.id)
    if not names:
        return ["x0"]

    # Check if all names are of form x<num> or q<num>
    pattern = re.compile(r"^[a-zA-Z]+(\d+)$")
    indexed = []
    all_indexed = True
    for name in names:
        m = pattern.match(name)
        if m:
            indexed.append((int(m.group(1)), name))
        else:
            all_indexed = False
            break

    if all_indexed:
        indexed.sort(key=lambda t: t[0])
        return [t[1] for t in indexed]
    return sorted(names)


def parse_bool_expr(
    expr: str, var_names: list[str] | None = None
) -> tuple[Callable[[dict[str, int]], int], list[str]]:
    """Parse a boolean expression string into a callable and variable name list.

    Supports Python operators: and, or, not, &, |, ^, ~, ==, !=, +, *.
    Example: '(x0 and x1) ^ x2' or 'a & b | ~c'.
    """
    cleaned = expr.strip()
    if not cleaned:
        raise ValueError("Boolean expression cannot be empty")

    try:
        tree = ast.parse(cleaned, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid boolean expression syntax: {exc}") from exc

    _validate_ast(tree)

    inferred_vars = _infer_var_names(tree)
    if var_names is None:
        var_names = inferred_vars
    else:
        var_names = list(var_names)
        missing = [v for v in inferred_vars if v not in var_names]
        if missing:
            raise ValueError(
                f"Expression contains variables not in provided var_names: {missing}"
            )

    code = compile(tree, "<bool_expr>", "eval")

    def eval_fn(env: dict[str, int]) -> int:
        safe_env = {"__builtins__": {}}
        safe_env.update(env)
        safe_env["True"] = True
        safe_env["False"] = False
        val = eval(code, safe_env)  # noqa: S307
        return 1 if bool(val) else 0

    return eval_fn, var_names


def bool_expr_to_truth_table(
    expr: str, var_names: list[str] | None = None
) -> tuple[np.ndarray, list[str]]:
    """Convert a boolean expression string into a truth table numpy array.

    The table length is 2^n where n = len(var_names).
    In little-endian convention, row k corresponds to integer k where
    the i-th variable var_names[i] has bit value (k >> i) & 1.
    """
    eval_fn, var_names = parse_bool_expr(expr, var_names)
    n = len(var_names)
    num_rows = 1 << n
    table = np.zeros(num_rows, dtype=np.int64)

    for k in range(num_rows):
        env = {var: (k >> i) & 1 for i, var in enumerate(var_names)}
        table[k] = eval_fn(env)

    return table, var_names


def parse_truth_table(spec: str | Iterable[int] | dict) -> tuple[np.ndarray, list[str]]:
    """Parse truth table specification into a numpy array of outputs.

    Supported formats:
    - Bitstring: "0110" or "01101001" (length must be 2^n)
    - Comma/space separated: "0, 1, 1, 0" or "0 1 1 0"
    - Mapping/dict: {"00": 0, "01": 1, ...} or "00:0, 01:1, 10:1, 11:0"
    - Reversible mapping: "0->1, 1->0, 2->3, 3->2"
    - List/array of integers: [0, 1, 1, 0]
    """
    if isinstance(spec, dict):
        return _parse_dict_truth_table(spec)

    if isinstance(spec, (list, tuple, np.ndarray)):
        arr = np.asarray(spec, dtype=np.int64)
        n = _validate_table_size(len(arr))
        var_names = [f"x{i}" for i in range(n)]
        return arr, var_names

    text = str(spec).strip()
    if not text:
        raise ValueError("Truth table specification cannot be empty")

    # Try JSON array or dict first
    if text.startswith("[") or text.startswith("{"):
        try:
            data = json.loads(text)
            return parse_truth_table(data)
        except json.JSONDecodeError:
            pass

    # Key-value mapping like "00:0, 01:1, 10:1, 11:0" or "0->1, 1->0"
    if ":" in text or "->" in text:
        sep = "->" if "->" in text else ":"
        parts = [p.strip() for p in re.split(r"[,;\n]", text) if p.strip()]
        mapping = {}
        for part in parts:
            if sep not in part:
                raise ValueError(f"Malformed truth table entry: {part!r}")
            k_str, v_str = part.split(sep, 1)
            mapping[k_str.strip()] = int(v_str.strip())
        return _parse_dict_truth_table(mapping)

    # Delimited list like "0, 1, 1, 0" or "0 1 1 0"
    if "," in text or " " in text:
        parts = [p.strip() for p in re.split(r"[, \t\n]+", text) if p.strip()]
        vals = [int(p) for p in parts]
        return parse_truth_table(vals)

    # Plain bitstring like "0110"
    if all(c in "01" for c in text):
        vals = [int(c) for c in text]
        return parse_truth_table(vals)

    raise ValueError(f"Could not parse truth table format: {text!r}")


def _parse_dict_truth_table(d: dict) -> tuple[np.ndarray, list[str]]:
    """Parse dictionary of input -> output into a truth table array."""
    num_entries = len(d)
    n = _validate_table_size(num_entries)
    arr = np.zeros(num_entries, dtype=np.int64)

    for k, v in d.items():
        if isinstance(k, str) and all(c in "01" for c in k):
            # Bitstring key: e.g. "01" -> x0=1, x1=0 or little-endian?
            # In standard binary notation for bitstrings "b_{n-1}...b_1 b_0":
            # The integer value is int(k, 2).
            # e.g. "00"->0, "01"->1, "10"->2, "11"->3.
            idx = int(k, 2)
        else:
            idx = int(k)
        if idx < 0 or idx >= num_entries:
            raise ValueError(f"Truth table input index {idx} out of range [0, {num_entries - 1}]")
        arr[idx] = int(v)

    var_names = [f"x{i}" for i in range(n)]
    return arr, var_names


def _validate_table_size(size: int) -> int:
    if size < 2:
        raise ValueError(f"Truth table must have at least 2 entries; got {size}")
    n = size.bit_length() - 1
    if (1 << n) != size:
        raise ValueError(
            f"Truth table length must be a power of 2 (2^n); got {size} entries"
        )
    return n


def truth_table_to_oracle(
    tt: np.ndarray | Iterable[int],
    oracle_mode: str = "bitflip",
) -> tuple[np.ndarray, int]:
    """Convert a truth table into a unitary quantum oracle matrix.

    Modes:
    - 'bitflip': |x>|y> -> |x>|y ^ f(x)>, size 2^(n+1) x 2^(n+1), n+1 qubits.
      Inputs x on qubits 0..n-1, target ancilla y on qubit n.
    - 'phase': |x> -> (-1)^f(x) |x>, size 2^n x 2^n, n qubits.
    - 'permutation': |x> -> |f(x)>, size 2^n x 2^n, n qubits.
      Requires tt to be a bijection (permutation of 0..2^n-1).

    Returns (matrix, total_qubits).
    """
    arr = np.asarray(tt, dtype=np.int64)
    n_inputs = _validate_table_size(len(arr))
    mode = oracle_mode.lower().strip()

    if mode == "bitflip":
        n_total = n_inputs + 1
        dim = 1 << n_total
        mat = np.zeros((dim, dim), dtype=np.complex128)
        target_bit = n_inputs  # qubit index of target y

        for x in range(1 << n_inputs):
            fx = int(arr[x]) & 1
            for y in (0, 1):
                col = x | (y << target_bit)
                y_new = y ^ fx
                row = x | (y_new << target_bit)
                mat[row, col] = 1.0

        check_unitary(mat, what="bit-flip oracle")
        return mat, n_total

    elif mode == "phase":
        dim = 1 << n_inputs
        mat = np.zeros((dim, dim), dtype=np.complex128)
        for x in range(dim):
            fx = int(arr[x]) & 1
            mat[x, x] = -1.0 if fx == 1 else 1.0

        check_unitary(mat, what="phase oracle")
        return mat, n_inputs

    elif mode == "permutation":
        dim = 1 << n_inputs
        if sorted(arr.tolist()) != list(range(dim)):
            raise ValueError(
                f"Permutation oracle requires truth table to be a permutation of 0..{dim-1}"
            )
        mat = np.zeros((dim, dim), dtype=np.complex128)
        for x in range(dim):
            row = int(arr[x])
            mat[row, x] = 1.0

        check_unitary(mat, what="permutation oracle")
        return mat, n_inputs

    else:
        raise ValueError(
            f"Unknown oracle mode {oracle_mode!r}; expected 'bitflip', 'phase', or 'permutation'"
        )


def format_truth_table(tt: np.ndarray, var_names: list[str] | None = None) -> str:
    """Render a truth table as an ASCII table string."""
    arr = np.asarray(tt, dtype=np.int64)
    n = _validate_table_size(len(arr))
    if var_names is None or len(var_names) != n:
        var_names = [f"x{i}" for i in range(n)]

    # Display variables from highest bit down to bit 0 (left to right)
    disp_vars = list(reversed(var_names))
    disp_indices = list(reversed(range(n)))

    header_cols = [f"{v:>3}" for v in disp_vars]
    header = " ".join(header_cols) + " |  f"
    sep = "-" * len(" ".join(header_cols)) + "-+----"
    lines = [header, sep]

    for k in range(len(arr)):
        row_bits = [f"{((k >> bit_idx) & 1):>3}" for bit_idx in disp_indices]
        lines.append(" ".join(row_bits) + f" | {arr[k]:>2}")

    return "\n".join(lines)
