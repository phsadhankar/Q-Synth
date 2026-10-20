"""Safe evaluation of the small expression language used in gate-set JSON files.

Supported syntax: ordinary Python arithmetic with ^ allowed as an alias for **.
Available names: I (imaginary unit), pi, e, sqrt2, sqrt3, exp, sqrt, sin, cos,
tan, log, conj, abs.
"""

import cmath
import math

_EVAL_ENV = {
    "I": 1j,
    "pi": math.pi,
    "e": math.e,
    "sqrt2": math.sqrt(2.0),
    "sqrt3": math.sqrt(3.0),
    "sqrt5": math.sqrt(5.0),
    "sqrt": cmath.sqrt,
    "exp": cmath.exp,
    "sin": cmath.sin,
    "cos": cmath.cos,
    "tan": cmath.tan,
    "log": cmath.log,
    "conj": lambda z: complex(z).conjugate(),
    "abs": abs,
}


def evaluate(expr, extra_vars=None):
    """Evaluate an expression string (or numeric value) to complex."""
    if isinstance(expr, (int, float, complex)):
        return complex(expr)
    if not isinstance(expr, str):
        raise ValueError(f"Unsupported matrix element type: {expr!r}")
    expr = expr.replace("^", "**").replace(" ", "")
    env = dict(_EVAL_ENV)
    if extra_vars:
        for k, v in extra_vars.items():
            env[k] = evaluate(v) if isinstance(v, str) else complex(v)
    try:
        val = eval(  # noqa: S307 - JSON gate files are user-provided, env is restricted
            expr, {"__builtins__": {}}, env
        )
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Failed to evaluate expression {expr!r}: {exc}") from exc
    return complex(val)


def evaluate_real(expr, extra_vars=None):
    """Evaluate an expression that must be (numerically) real."""
    val = evaluate(expr, extra_vars)
    if abs(val.imag) > 1e-12:
        raise ValueError(f"Expected a real value, got {expr!r} = {val}")
    return val.real
