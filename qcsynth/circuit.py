"""Quantum circuit parsing, OpenQASM 2.0 import/export, and ASCII visualization."""

from __future__ import annotations

import math
import re
from typing import Sequence

import numpy as np

from .gates import Gate
from .search import Move, embed_gate
from .targets import TARGETS, get_target

# Standard single and two qubit gate definitions for standalone circuit parsing
_STD_GATES = {
    "i": Gate("I", TARGETS["i"]),
    "x": Gate("X", TARGETS["x"]),
    "y": Gate("Y", TARGETS["y"]),
    "z": Gate("Z", TARGETS["z"]),
    "h": Gate("H", TARGETS["h"]),
    "s": Gate("S", TARGETS["s"]),
    "sdg": Gate("Sdg", np.array([[1, 0], [0, -1j]], dtype=np.complex128)),
    "t": Gate("T", TARGETS["t"]),
    "tdg": Gate("Tdg", np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]], dtype=np.complex128)),
    "cnot": Gate("CNOT", TARGETS["cnot"]),
    "cx": Gate("CNOT", TARGETS["cnot"]),
    "cz": Gate("CZ", TARGETS["cz"]),
    "swap": Gate("SWAP", TARGETS["swap"]),
    "ccx": Gate("CCX", TARGETS["ccx"]),
    "toffoli": Gate("CCX", TARGETS["ccx"]),
    "cswap": Gate("CSWAP", TARGETS["cswap"]),
    "fredkin": Gate("CSWAP", TARGETS["cswap"]),
}


def _make_rot_gate(name: str, theta: float) -> Gate:
    """Instantiate a single-qubit rotation gate for an arbitrary angle."""
    name_upper = name.upper()
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    if name_upper == "RX":
        mat = np.array([[c, -1j * s], [-1j * s, c]], dtype=np.complex128)
    elif name_upper == "RY":
        mat = np.array([[c, -s], [s, c]], dtype=np.complex128)
    elif name_upper == "RZ":
        mat = np.array([[cmath_exp(-1j * theta / 2.0), 0],
                        [0, cmath_exp(1j * theta / 2.0)]], dtype=np.complex128)
    else:
        raise ValueError(f"Unknown rotation gate {name}")
    from .gates import _fmt_angle
    return Gate(f"{name_upper}({_fmt_angle(theta)})", mat)


def cmath_exp(z: complex) -> complex:
    import cmath
    return cmath.exp(z)


def _eval_angle_str(expr_str: str) -> float:
    """Safely parse angle expressions like 'pi/4', '-pi/2', '0.5'."""
    from .expr import evaluate_real
    return evaluate_real(expr_str)


def _split_statements(text: str) -> list[str]:
    """Split circuit text on commas, semicolons, or newlines outside brackets/parentheses."""
    statements = []
    current = []
    depth = 0
    for char in text:
        if char in "([":
            depth += 1
            current.append(char)
        elif char in ")]":
            depth = max(0, depth - 1)
            current.append(char)
        elif char in ",;\n" and depth == 0:
            stmt = "".join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []
        else:
            current.append(char)
    stmt = "".join(current).strip()
    if stmt:
        statements.append(stmt)
    return statements


def parse_circuit(
    text: str,
    gate_dict: dict[str, list[Gate]] | None = None,
    n_qubits: int | None = None,
) -> tuple[list[Move], int]:
    """Parse a quantum circuit from text.

    Supports:
    - Native format: "H[0], CNOT[0,1], H[0]" or semicolon/newline separated
    - Space format: "h 0; cx 0 1; h 0"
    - OpenQASM 2.0 syntax (full file or snippet)
    """
    cleaned = text.strip()
    if not cleaned:
        return [], (n_qubits or 0)

    if "OPENQASM" in cleaned or "qreg" in cleaned:
        return parse_qasm(cleaned, gate_dict=gate_dict, n_qubits=n_qubits)

    # Tokenize statements split by comma, semicolon, or newline outside brackets
    tokens = _split_statements(cleaned)

    # Flatten gate_dict to lookup map
    lookup = dict(_STD_GATES)
    if gate_dict:
        for base, glist in gate_dict.items():
            lookup[base.lower()] = glist[0]
            for g in glist:
                lookup[g.name.lower()] = g

    ops = []
    max_qubit = -1

    for tok in tokens:
        # Match pattern like "CNOT[0,1]" or "RX(pi/4)[0]"
        m_bracket = re.match(r"^([a-zA-Z0-9_]+(?:\([^)]*\))?)\s*\[\s*([0-9,\s]+)\s*\]$", tok)
        if m_bracket:
            gname = m_bracket.group(1).strip()
            qstr = m_bracket.group(2).strip()
            placement = tuple(int(x.strip()) for x in qstr.split(","))
            gate = _resolve_gate(gname, len(placement), lookup)
            ops.append(Move(gate, placement))
            max_qubit = max(max_qubit, *placement)
            continue

        # Match pattern like "cx 0, 1" or "h 0" or "rx(pi/4) 0"
        m_space = re.match(r"^([a-zA-Z0-9_]+(?:\([^)]*\))?)\s+([0-9,\s]+)$", tok)
        if m_space:
            gname = m_space.group(1).strip()
            qstr = m_space.group(2).strip()
            placement = tuple(int(x.strip()) for x in re.split(r"[, \t]+", qstr) if x.strip())
            gate = _resolve_gate(gname, len(placement), lookup)
            ops.append(Move(gate, placement))
            max_qubit = max(max_qubit, *placement)
            continue

        raise ValueError(f"Could not parse circuit operation: {tok!r}")

    total_qubits = n_qubits if n_qubits is not None else (max_qubit + 1 if max_qubit >= 0 else 0)
    if max_qubit >= total_qubits:
        raise ValueError(
            f"Circuit references qubit {max_qubit}, but circuit qubit count is {total_qubits}"
        )

    return ops, total_qubits


def parse_qasm(
    qasm_text: str,
    gate_dict: dict[str, list[Gate]] | None = None,
    n_qubits: int | None = None,
) -> tuple[list[Move], int]:
    """Parse OpenQASM 2.0 text into circuit Move operations."""
    lookup = dict(_STD_GATES)
    if gate_dict:
        for base, glist in gate_dict.items():
            lookup[base.lower()] = glist[0]
            for g in glist:
                lookup[g.name.lower()] = g

    lines = qasm_text.splitlines()
    inferred_n = 0
    ops = []
    max_qubit = -1

    for line in lines:
        line = line.split("//")[0].strip()  # strip comments
        if not line or line.endswith(";"):
            line = line.rstrip(";")
        if not line:
            continue
        if line.startswith("OPENQASM") or line.startswith("include"):
            continue

        # Check register declaration: qreg q[2]
        m_qreg = re.match(r"^qreg\s+([a-zA-Z0-9_]+)\s*\[\s*(\d+)\s*\]", line)
        if m_qreg:
            inferred_n = max(inferred_n, int(m_qreg.group(2)))
            continue

        # Skip creg or barrier or measure
        if line.startswith("creg") or line.startswith("barrier") or line.startswith("measure"):
            continue

        # Match gate application: e.g. "cx q[0], q[1]" or "h q[0]" or "rx(pi/2) q[0]"
        m_gate = re.match(r"^([a-zA-Z0-9_]+(?:\([^)]*\))?)\s+(.+)$", line)
        if not m_gate:
            continue
        gname = m_gate.group(1).strip()
        arg_str = m_gate.group(2).strip()

        # Extract qubit indices from args like "q[0], q[1]" or "0, 1"
        qubits = [int(q) for q in re.findall(r"\[(\d+)\]", arg_str)]
        if not qubits:
            qubits = [int(q) for q in re.findall(r"\b(\d+)\b", arg_str)]

        if not qubits:
            continue

        placement = tuple(qubits)
        gate = _resolve_gate(gname, len(placement), lookup)
        ops.append(Move(gate, placement))
        max_qubit = max(max_qubit, *placement)

    total_qubits = n_qubits if n_qubits is not None else max(inferred_n, max_qubit + 1)
    return ops, total_qubits


def _resolve_gate(gname: str, n_wires: int, lookup: dict[str, Gate]) -> Gate:
    """Resolve a gate name (with optional parameters) into a concrete Gate."""
    key = gname.lower()
    if key in lookup:
        g = lookup[key]
        if g.qubits == n_wires:
            return g

    # Check for rotation gate like rx(pi/4) or rz(1.57)
    m_rot = re.match(r"^(rx|ry|rz)\s*\(([^)]+)\)$", key)
    if m_rot:
        rname = m_rot.group(1).upper()
        ang_val = _eval_angle_str(m_rot.group(2))
        return _make_rot_gate(rname, ang_val)

    # Check without parentheses if in lookup
    m_base = re.match(r"^([a-zA-Z0-9_]+)", key)
    if m_base and m_base.group(1) in lookup:
        g = lookup[m_base.group(1)]
        if g.qubits == n_wires:
            return g

    raise ValueError(f"Unrecognized or unsupported gate {gname!r} on {n_wires} qubits")


def circuit_to_qasm(ops: Sequence[Move], n_qubits: int) -> str:
    """Export a circuit to OpenQASM 2.0 format."""
    lines = [
        'OPENQASM 2.0;',
        'include "qelib1.inc";',
        f'qreg q[{n_qubits}];',
    ]

    for op in ops:
        name = op.gate.name.lower()
        pl = op.placement
        if name in ("cnot", "cx"):
            lines.append(f"cx q[{pl[0]}], q[{pl[1]}];")
        elif name == "cz":
            lines.append(f"cz q[{pl[0]}], q[{pl[1]}];")
        elif name == "swap":
            lines.append(f"swap q[{pl[0]}], q[{pl[1]}];")
        elif name in ("ccx", "toffoli"):
            lines.append(f"ccx q[{pl[0]}], q[{pl[1]}], q[{pl[2]}];")
        elif name in ("cswap", "fredkin"):
            lines.append(f"cswap q[{pl[0]}], q[{pl[1]}], q[{pl[2]}];")
        elif name.startswith("rx(") or name.startswith("ry(") or name.startswith("rz("):
            lines.append(f"{name} q[{pl[0]}];")
        elif name in ("h", "x", "y", "z", "s", "t"):
            lines.append(f"{name} q[{pl[0]}];")
        else:
            qs = ", ".join(f"q[{q}]" for q in pl)
            lines.append(f"{name} {qs};")

    return "\n".join(lines) + "\n"


def circuit_to_diagram(ops: Sequence[Move], n_qubits: int) -> str:
    """Generate an ASCII quantum circuit diagram."""
    if n_qubits == 0:
        return "(empty circuit)"

    # Grid of characters for each qubit wire
    lines = [f"q{q}: ─" for q in range(n_qubits)]

    for op in ops:
        gname = op.gate.name.upper()
        pl = op.placement

        # Determine wire symbols for this column
        if gname in ("CNOT", "CX") and len(pl) == 2:
            ctrl, tgt = pl[0], pl[1]
            min_q, max_q = min(ctrl, tgt), max(ctrl, tgt)
            for q in range(n_qubits):
                if q == ctrl:
                    lines[q] += "─■─"
                elif q == tgt:
                    lines[q] += "─X─"
                elif min_q < q < max_q:
                    lines[q] += "─┼─"
                else:
                    lines[q] += "───"

        elif gname == "CZ" and len(pl) == 2:
            q0, q1 = pl[0], pl[1]
            min_q, max_q = min(q0, q1), max(q0, q1)
            for q in range(n_qubits):
                if q in (q0, q1):
                    lines[q] += "─■─"
                elif min_q < q < max_q:
                    lines[q] += "─┼─"
                else:
                    lines[q] += "───"

        elif gname == "SWAP" and len(pl) == 2:
            q0, q1 = pl[0], pl[1]
            min_q, max_q = min(q0, q1), max(q0, q1)
            for q in range(n_qubits):
                if q in (q0, q1):
                    lines[q] += "─✕─"
                elif min_q < q < max_q:
                    lines[q] += "─┼─"
                else:
                    lines[q] += "───"

        elif gname in ("CCX", "TOFFOLI") and len(pl) == 3:
            c1, c2, tgt = pl[0], pl[1], pl[2]
            min_q, max_q = min(pl), max(pl)
            for q in range(n_qubits):
                if q in (c1, c2):
                    lines[q] += "─■─"
                elif q == tgt:
                    lines[q] += "─X─"
                elif min_q < q < max_q:
                    lines[q] += "─┼─"
                else:
                    lines[q] += "───"

        else:
            # Single-qubit or generic gate box
            label = op.gate.name
            w = len(label)
            for q in range(n_qubits):
                if q in pl:
                    lines[q] += f"[{label}]─"
                else:
                    lines[q] += "─" * (w + 3)

    for q in range(n_qubits):
        lines[q] += "─"

    return "\n".join(lines)
