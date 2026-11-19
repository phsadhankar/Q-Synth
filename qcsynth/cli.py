"""Command line interface for the quantum circuit synthesizer and optimizer."""

from __future__ import annotations

import argparse
import sys
import time

import numpy as np

from .boolean import (
    bool_expr_to_truth_table,
    format_truth_table,
    parse_truth_table,
    truth_table_to_oracle,
)
from .circuit import circuit_to_diagram, circuit_to_qasm, parse_circuit
from .gates import load_gate_set
from .optimize import optimize_circuit
from .search import beam_search, enumerate_moves, verify
from .targets import load_matrix_file, n_qubits_of, resolve_target

DEFAULT_GATES_FILE = "gates/clifford_t.json"


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="synthesizer",
        description="Quantum circuit synthesizer: beam-search gate sequences for unitaries, "
                    "Boolean functions, and truth tables; optimize existing circuits to fewer gates.")
    p.add_argument("--n", type=int, default=None,
                   help="number of qubits (inferred from target or circuit if omitted)")

    # Target Unitary inputs
    g_target = p.add_argument_group("target unitary specification")
    g_target.add_argument("--matrix", default=None, metavar="NAME|JSON",
                          help="target unitary: built-in name (swap, cnot, cz, x, y, "
                               "z, h, s, t, ccx, toffoli, cswap, fredkin, i) or inline JSON matrix")
    g_target.add_argument("--matrix-file", default=None, metavar="PATH",
                          help="target unitary from .npy or text/CSV file")

    # Boolean & Truth Table inputs
    g_bool = p.add_argument_group("Boolean function & truth table specification")
    g_bool.add_argument("--bool-expr", default=None, metavar="EXPR",
                        help="Boolean function expression, e.g. '(x0 and x1) ^ x2' or 'a & b | ~c'")
    g_bool.add_argument("--truth-table", default=None, metavar="SPEC",
                        help="truth table: bitstring ('0110'), comma-separated ('0,1,1,0'), "
                             "or mapping ('00:0, 01:1, ...')")
    g_bool.add_argument("--truth-table-file", default=None, metavar="PATH",
                        help="path to file containing a truth table")
    g_bool.add_argument("--oracle-mode", default="bitflip",
                        choices=["bitflip", "phase", "permutation"],
                        help="oracle embedding for Boolean/truth table: 'bitflip' "
                             "(|x>|y> -> |x>|y^f(x)>, n+1 qubits, default), "
                             "'phase' (|x> -> (-1)^f(x)|x>, n qubits), or "
                             "'permutation' (|x> -> |f(x)>, n qubits)")
    g_bool.add_argument("--var-names", default=None, metavar="X0,X1,...",
                        help="ordered input variable names (inferred if omitted)")

    # Circuit optimization inputs
    g_opt = p.add_argument_group("circuit optimization")
    g_opt.add_argument("--circuit", default=None, metavar="OPS",
                       help="input circuit to optimize to fewer gates, e.g. "
                            "'H[0], CNOT[0,1], H[0]' or OpenQASM 2.0 text")
    g_opt.add_argument("--circuit-file", default=None, metavar="PATH",
                       help="path to circuit file (.txt or .qasm) to optimize")
    g_opt.add_argument("--optimize", action="store_true",
                       help="optimize the provided circuit to fewer gates using allowed gates")
    g_opt.add_argument("--window-size", type=int, default=4,
                       help="sliding window size for block resynthesis (default: 4)")

    # Gate set specification
    g_gates = p.add_argument_group("allowed gates specification")
    g_gates.add_argument("--gates-file", default=DEFAULT_GATES_FILE, metavar="PATH",
                         help=f"JSON file describing allowed gates (default: {DEFAULT_GATES_FILE})")
    g_gates.add_argument("--gate-names", default=None, metavar="N1,N2,...",
                         help="use only these gates from the gate-set file")

    # Search parameters
    g_search = p.add_argument_group("search parameters")
    g_search.add_argument("--depth", type=int, default=8,
                          help="maximum circuit length to search (default 8)")
    g_search.add_argument("--beam", type=int, default=2000,
                          help="beam width: how many best candidates to keep per level (default 2000)")
    g_search.add_argument("--tol", type=float, default=1e-9,
                          help="similarity tolerance treated as exact match (default 1e-9)")
    g_search.add_argument("--time-limit", type=float, default=None,
                          help="stop searching after this many seconds")

    # Output options
    g_out = p.add_argument_group("output options")
    g_out.add_argument("--quiet", action="store_true", help="suppress per-level progress")
    g_out.add_argument("--show-matrix", action="store_true",
                       help="also print the circuit's full matrix")
    g_out.add_argument("--show-diagram", action="store_true",
                       help="display ASCII quantum circuit diagram")
    g_out.add_argument("--qasm-out", default=None, metavar="PATH",
                       help="export resulting circuit to OpenQASM 2.0 file")
    p.add_argument("demo", nargs="?", default=None,
                   help="(optional) literally 'demo' to run example syntheses and optimizations")

    args = p.parse_args(argv)

    has_target = bool(args.matrix or args.matrix_file or args.bool_expr or
                      args.truth_table or args.truth_table_file)
    has_circuit = bool(args.circuit or args.circuit_file or args.optimize)

    if not has_target and not has_circuit and args.demo != "demo":
        p.error("give a target (--matrix, --matrix-file, --bool-expr, --truth-table), "
                "a circuit to optimize (--circuit, --circuit-file), or 'demo'")
    return args


def _plural(m: int, s: str) -> str:
    return f"{m} {s}{'s' if m != 1 else ''}"


def run_synthesis(args) -> int:
    # 1. Determine target unitary and metadata
    tname = ""
    tt_display = None
    var_list = [v.strip() for v in args.var_names.split(",")] if args.var_names else None

    if args.bool_expr:
        tt, vars_found = bool_expr_to_truth_table(args.bool_expr, var_names=var_list)
        target, inferred_n = truth_table_to_oracle(tt, oracle_mode=args.oracle_mode)
        tname = f"Boolean expression {args.bool_expr!r} ({args.oracle_mode} oracle)"
        tt_display = format_truth_table(tt, vars_found)

    elif args.truth_table or args.truth_table_file:
        spec = args.truth_table
        if args.truth_table_file:
            with open(args.truth_table_file, encoding="utf-8") as fh:
                spec = fh.read().strip()
        tt, vars_found = parse_truth_table(spec)
        target, inferred_n = truth_table_to_oracle(tt, oracle_mode=args.oracle_mode)
        tname = f"Truth table ({args.oracle_mode} oracle)"
        tt_display = format_truth_table(tt, vars_found)

    elif args.matrix:
        target, tname = resolve_target(args.matrix)
        inferred_n = n_qubits_of(target)

    elif args.matrix_file:
        target = load_matrix_file(args.matrix_file)
        tname = args.matrix_file
        inferred_n = n_qubits_of(target)
    else:
        raise ValueError("No target provided for synthesis")

    n = args.n if args.n is not None else inferred_n
    if n_qubits_of(target) != n:
        raise SystemExit(f"Target is {n_qubits_of(target)} qubits, but --n {n} was given")

    # 2. Load allowed gate set
    names = [n.strip() for n in args.gate_names.split(",")] if args.gate_names else None
    _, gates, doc = load_gate_set(args.gates_file, names=names)
    moves = enumerate_moves(gates, n)

    print(f"Target: {tname} ({_plural(n, 'qubit')}, {target.shape[0]}x{target.shape[0]})")
    if tt_display and not args.quiet:
        print("\nTruth table:")
        print(tt_display)
        print()

    preset = doc.get("name", args.gates_file)
    print(f"Gate set: {preset} - {_plural(len(gates), 'gate instance')}, "
          f"{len(moves)} placements (beam {args.beam}, max depth {args.depth})")

    def progress(depth, best_s, n_cands):
        if not args.quiet:
            print(f"  depth {depth:2d}: best similarity {best_s:.10f} ({n_cands} candidates)")

    t0 = time.perf_counter()
    state, found, stats = beam_search(
        target, moves, max_depth=args.depth, beam_width=args.beam,
        tol=args.tol, on_level=progress, time_limit=args.time_limit)
    print()

    if not found:
        print(f"FAILED: no circuit of length <= {args.depth} found "
              f"(best similarity {state.score:.10f}, "
              f"{stats['expanded']} expansions in {time.perf_counter() - t0:.2f}s).")
        print("Try increasing --beam, --depth, or enlarging the gate set.")
        return 1

    ops_repr = ', '.join(op.gate.label(op.placement, n) for op in state.ops)
    print(f"SUCCESS at depth {len(state.ops)} "
          f"({stats['expanded']} expansions, {time.perf_counter() - t0:.2f}s): "
          f"V = {' @ '.join(op.gate.label(op.placement, n) for op in reversed(state.ops))}")
    print(f"  (gates applied in this order: {ops_repr})")
    v = verify(state.ops, target, n)
    print(f"  similarity {v['s']:.10f}, global phase {v['phi']:+.6f} rad, "
          f"max element error {v['err']:.2e}")

    if args.show_diagram:
        print("\nCircuit diagram:")
        print(circuit_to_diagram(state.ops, n))

    if args.qasm_out:
        qasm = circuit_to_qasm(state.ops, n)
        with open(args.qasm_out, "w", encoding="utf-8") as fh:
            fh.write(qasm)
        print(f"Exported OpenQASM 2.0 to {args.qasm_out}")

    if args.show_matrix:
        with np.printoptions(precision=4, suppress=True):
            print(state.matrix)
    return 0


def run_optimization(args) -> int:
    """Optimize a user-provided circuit to fewer gates using allowed gates."""
    # 1. Parse input circuit
    raw_circuit = args.circuit
    if args.circuit_file:
        with open(args.circuit_file, encoding="utf-8") as fh:
            raw_circuit = fh.read()

    if not raw_circuit:
        raise ValueError("Must provide circuit text via --circuit or a file via --circuit-file")

    # Load gate set to get names and lookup
    names = [n.strip() for n in args.gate_names.split(",")] if args.gate_names else None
    gate_dict, flat_gates, doc = load_gate_set(args.gates_file, names=names)

    ops, n_inferred = parse_circuit(raw_circuit, gate_dict=gate_dict, n_qubits=args.n)
    n = args.n if args.n is not None else n_inferred
    if n == 0:
        print("Input circuit is empty; 0 gates.")
        return 0

    preset = doc.get("name", args.gates_file)
    print(f"Original Circuit: {_plural(len(ops), 'gate')}, {_plural(n, 'qubit')}")
    print(f"  Applied order: {', '.join(op.gate.label(op.placement, n) for op in ops)}")
    if args.show_diagram or not args.quiet:
        print("\nOriginal diagram:")
        print(circuit_to_diagram(ops, n))
        print()

    print(f"Allowed Gate Set: {preset} - {_plural(len(flat_gates), 'gate instance')}")
    if names:
        print(f"  Allowed gate names: {', '.join(names)}")

    print(f"Optimizing circuit (beam {args.beam}, max depth {args.depth}, "
          f"window {args.window_size})...")

    opt_ops, stats = optimize_circuit(
        ops=ops,
        allowed_gates=flat_gates,
        n_qubits=n,
        max_depth=args.depth,
        beam_width=args.beam,
        tol=args.tol,
        window_size=args.window_size,
        time_limit=args.time_limit,
    )

    print()
    print(f"Optimization complete in {stats.elapsed_seconds:.2f}s:")
    print(f"  Original gates:  {stats.original_gates}")
    print(f"  Optimized gates: {stats.optimized_gates}")
    print(f"  Reduction:       {stats.gates_saved} fewer gates "
          f"({stats.reduction_pct:.1f}% reduction)")
    if stats.passes_run:
        print(f"  Passes applied:  {', '.join(stats.passes_run)}")

    opt_repr = ', '.join(op.gate.label(op.placement, n) for op in opt_ops) if opt_ops else "(empty)"
    print(f"  Optimized order: {opt_repr}")
    print(f"  Verification: similarity {stats.similarity:.10f}, "
          f"phase {stats.global_phase:+.6f} rad, max err {stats.max_error:.2e}")

    if args.show_diagram or not args.quiet:
        print("\nOptimized diagram:")
        print(circuit_to_diagram(opt_ops, n))

    if args.qasm_out:
        qasm = circuit_to_qasm(opt_ops, n)
        with open(args.qasm_out, "w", encoding="utf-8") as fh:
            fh.write(qasm)
        print(f"\nExported optimized OpenQASM 2.0 to {args.qasm_out}")

    return 0


def run_demo():
    """Demonstrate unitary synthesis, Boolean synthesis, and circuit optimization."""
    demos = [
        # Matrix syntheses
        (["--matrix", "swap", "--gates-file", "gates/clifford_t.json",
          "--gate-names", "CNOT", "--depth", "3", "--quiet"],
         "SWAP as 3 CNOTs"),
        (["--matrix", "h", "--gates-file", "gates/universal_rxy.json",
          "--depth", "4", "--quiet"],
         "Hadamard from discrete RX/RY/RZ rotations"),
        # Boolean function synthesis
        (["--bool-expr", "x0 ^ x1", "--gates-file", "gates/clifford_t.json",
          "--gate-names", "CNOT", "--oracle-mode", "bitflip", "--depth", "3", "--quiet"],
         "Boolean XOR: f(x0,x1) = x0 ^ x1 synthesized as 2 CNOTs"),
        (["--bool-expr", "x0 and x1", "--gates-file", "gates/clifford_t.json",
          "--oracle-mode", "phase", "--depth", "2", "--quiet"],
         "Boolean AND Phase Oracle: f(x0,x1) = x0 and x1 synthesized as CZ"),
        # Truth table synthesis
        (["--truth-table", "0110", "--gates-file", "gates/clifford_t.json",
          "--gate-names", "CNOT", "--oracle-mode", "bitflip", "--depth", "3", "--quiet"],
         "Truth table '0110' (XOR) synthesized as 2 CNOTs"),
        # Circuit optimization
        (["--circuit", "H[0], CNOT[0,1], CNOT[0,1], H[0]",
          "--gates-file", "gates/clifford_t.json", "--quiet"],
         "Optimization: canceling H-CNOT-CNOT-H (4 gates -> 0 gates)"),
        (["--circuit", "CNOT[0,1], CNOT[1,0], CNOT[0,1], CNOT[0,1], CNOT[1,0], CNOT[0,1]",
          "--gates-file", "gates/clifford_t.json", "--gate-names", "CNOT", "--quiet"],
         "Optimization: double SWAP cancellation (6 gates -> 0 gates)"),
        (["--circuit", "T[0], T[0]",
          "--gates-file", "gates/clifford_t.json", "--quiet"],
         "Optimization: gate merging T-T into S (2 gates -> 1 gate)"),
    ]

    for flags, title in demos:
        print(f"=== DEMO: {title} ===")
        parsed = parse_args(flags)
        if parsed.circuit or parsed.circuit_file or parsed.optimize:
            run_optimization(parsed)
        else:
            run_synthesis(parsed)
        print()
    return 0


def main(argv=None):
    args = parse_args(argv)
    if args.demo == "demo":
        args.demo = None
        return run_demo()
    try:
        if args.circuit or args.circuit_file or args.optimize:
            return run_optimization(args)
        return run_synthesis(args)
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
