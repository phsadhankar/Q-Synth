"""Command line interface for the quantum circuit synthesizer."""

from __future__ import annotations

import argparse
import sys
import time

import numpy as np

from .gates import load_gate_set
from .search import beam_search, enumerate_moves, verify
from .targets import load_matrix_file, n_qubits_of, resolve_target

DEFAULT_GATES_FILE = "gates/clifford_t.json"


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="synthesizer",
        description="Beam-search a circuit of allowed gates that reproduces a "
                    "target unitary up to global phase.")
    p.add_argument("--n", type=int, default=None,
                   help="number of qubits (inferred from the target by default)")
    p.add_argument("--matrix", default=None, metavar="NAME|JSON",
                   help="target unitary: built-in name (swap, cnot, cz, x, y, "
                        "z, h, s, t, i) or inline JSON matrix, e.g. "
                        "'[[\"sqrt2/2\",\"sqrt2/2\"],[\"sqrt2/2\",\"-sqrt2/2\"]]'; "
                        "file targets use --matrix-file")
    p.add_argument("--matrix-file", default=None, metavar="PATH",
                   help="target unitary from .npy or text/CSV file")
    p.add_argument("--gates-file", default=DEFAULT_GATES_FILE, metavar="PATH",
                   help="JSON file describing the allowed gates "
                        f"(default: {DEFAULT_GATES_FILE})")
    p.add_argument("--gate-names", default=None, metavar="N1,N2,...",
                   help="use only these gates from the gate-set file")
    p.add_argument("--depth", type=int, default=8,
                   help="maximum circuit length to search (default 8)")
    p.add_argument("--beam", type=int, default=2000,
                   help="beam width: how many best candidates to keep per level")
    p.add_argument("--tol", type=float, default=1e-9,
                   help="similarity tolerance treated as exact match")
    p.add_argument("--time-limit", type=float, default=None,
                   help="stop searching after this many seconds (best effort)")
    p.add_argument("--quiet", action="store_true", help="suppress per-level progress")
    p.add_argument("--show-matrix", action="store_true",
                   help="also print the found circuit's matrix")
    p.add_argument("demo", nargs="?", default=None,
                   help="(optional) literally 'demo' to run example syntheses")
    args = p.parse_args(argv)
    if not args.matrix and not args.matrix_file and args.demo != "demo":
        p.error("give --matrix NAME, --matrix-file PATH, or the 'demo' argument")
    return args


def run_synthesis(args):
    if args.matrix:
        target, tname = resolve_target(args.matrix)
    else:
        target = load_matrix_file(args.matrix_file)
        tname = args.matrix_file
    n = args.n if args.n is not None else n_qubits_of(target)
    if n_qubits_of(target) != n:
        raise SystemExit(f"Target is {n_qubits_of(target)} qubits, but --n {n} was given")

    names = args.gate_names.split(",") if args.gate_names else None
    _, gates, doc = load_gate_set(args.gates_file, names=names)
    moves = enumerate_moves(gates, n)
    plural = lambda m, s: f"{m} {s}{'s' if m != 1 else ''}"  # noqa: E731
    print(f"Target: {tname} ({plural(n, 'qubit')}, {target.shape[0]}x{target.shape[0]})")
    preset = doc.get("name", args.gates_file)
    print(f"Gate set: {preset} - {plural(len(gates), 'gate instance')}, "
          f"{len(moves)} placements (beam {args.beam}, max depth {args.depth})")

    def progress(depth, best_s, n_cands):
        if not args.quiet:
            print(f"  depth {depth:2d}: best similarity {best_s:.10f} "
                  f"({n_cands} candidates)")

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

    print(f"SUCCESS at depth {len(state.ops)} "
          f"({stats['expanded']} expansions, {time.perf_counter() - t0:.2f}s): "
          f"V = {' @ '.join(op.gate.label(op.placement, n) for op in reversed(state.ops))}")
    print(f"  (gates applied in this order: "
          f"{', '.join(op.gate.label(op.placement, n) for op in state.ops)})")
    v = verify(state.ops, target, n)
    print(f"  similarity {v['s']:.10f}, global phase {v['phi']:+.6f} rad, "
          f"max element error {v['err']:.2e}")
    if args.show_matrix:
        with np.printoptions(precision=4, suppress=True):
            print(state.matrix)
    return 0


def run_demo():
    """Three example runs using the shipped presets."""
    demos = [
        (["--matrix", "swap", "--gates-file", "gates/clifford_t.json",
          "--gate-names", "CNOT", "--depth", "3", "--quiet"], "SWAP as 3 CNOTs"),
        (["--matrix", "swap", "--gates-file", "gates/clifford_t.json",
          "--depth", "5", "--quiet"], "SWAP from the full Clifford+T preset"),
        (["--matrix", "h", "--gates-file", "gates/universal_rxy.json",
          "--depth", "4", "--quiet"], "Hadamard from discrete RX/RY/RZ"),
    ]
    for flags, title in demos:
        print(f"=== demo: {title} ===")
        code = run_synthesis(parse_args(flags))
        print()
    return 0


def main(argv=None):
    args = parse_args(argv)
    if args.demo == "demo":
        args.demo = None
        return run_demo()
    try:
        return run_synthesis(args)
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
