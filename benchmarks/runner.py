"""Benchmark runner: executes Case records from benchmarks.cases and reports.

Usage (from the repository root):

    python -m benchmarks.run_benchmarks              # full suite
    python -m benchmarks.run_benchmarks --quick      # fast subset
    python -m benchmarks.run_benchmarks --category scaling
    python -m benchmarks.run_benchmarks --only SWAP
    python -m benchmarks.run_benchmarks --time-limit 5 --limit 50

Outputs (benchmarks/results/):
    benchmarks.json   one record per case (full details)
    benchmarks.csv    flat table for spreadsheets / pandas
    summary.md        per-category tables + scaling curves
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from qcsynth.gates import load_gate_set                     # noqa: E402
from qcsynth.search import (beam_search, enumerate_moves,   # noqa: E402
                            run_circuit, verify)
from qcsynth.targets import n_qubits_of                     # noqa: E402

from .cases import Case, build_cases                        # noqa: E402

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

CSV_FIELDS = [
    "index", "category", "label", "n_qubits", "dim", "gates_file",
    "gate_names", "depth", "beam", "time_limit", "expect", "found",
    "n_ops", "best_score", "verify_s", "verify_err", "circuit",
    "expanded", "elapsed", "exp_per_sec", "search_depth", "match_expect",
]


def run_case(case: Case, beam=None, tol=1e-9, override_time_limit=None):
    """Execute one benchmark case; returns a result record dict."""
    _, flat, _doc = load_gate_set(case.gates_file, names=case.gate_names)
    n = n_qubits_of(case.target)
    moves = enumerate_moves(flat, n)
    state, found, stats = beam_search(
        case.target, moves,
        max_depth=case.depth,
        beam_width=(case.beam if beam is None else beam),
        tol=tol,
        time_limit=(case.time_limit if override_time_limit is None
                    else override_time_limit))
    rec = {
        "index": case.index,
        "category": case.category,
        "label": case.label,
        "n_qubits": n,
        "dim": case.target.shape[0],
        "gates_file": case.gates_file,
        "gate_names": ",".join(case.gate_names) if case.gate_names else None,
        "depth": case.depth,
        "beam": case.beam,
        "time_limit": case.time_limit,
        "expect": case.expect,
        "found": found,
        "best_score": state.score,
        "circuit": None,
        "n_ops": None,
        "verify_s": None,
        "verify_err": None,
        "expanded": stats["expanded"],
        "elapsed": stats["elapsed"],
        "search_depth": stats["depth"],
    }
    if found:
        ops = list(state.ops)
        rec["n_ops"] = len(ops)
        rec["circuit"] = " @ ".join(
            op.gate.label(op.placement, n) for op in reversed(ops))
        ver = verify(ops, case.target, n)
        rec["verify_s"] = ver["s"]
        rec["verify_err"] = ver["err"]
        rec["best_score"] = ver["s"]
    rec["exp_per_sec"] = rec["expanded"] / rec["elapsed"] if rec["elapsed"] else 0
    if case.expect is not None:
        rec["match_expect"] = bool(rec["found"]) == (case.expect == "found")
    else:
        rec["match_expect"] = None
    return rec


def _fmt(rec):
    verdict = {True: "FOUND", False: "miss", None: "warn"}[rec["match_expect"]]
    ops = "" if rec["n_ops"] is None else f"{rec['n_ops']} ops"
    return (f"elapsed {rec['elapsed']:7.3f}s  exp {rec['expanded']:>9d}  "
            f"score {rec['best_score']:.6f}  {fmt_circuit(rec)}  {ops}  [{verdict}]")


def fmt_circuit(rec):
    """Circuit gate string, en-dash-free and clipped."""
    if not rec["circuit"]:
        return "-"
    text = rec["circuit"]
    return text if len(text) <= 60 else text[:57] + "..."


def write_outputs(records, meta, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "benchmarks.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"meta": meta, "records": records}, fh, indent=1)
    with open(os.path.join(out_dir, "benchmarks.csv"), "w",
              encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS,
                                extrasaction="ignore")
        writer.writeheader()
        for row in records:
            writer.writerow({k: row.get(k) for k in CSV_FIELDS})


def write_summary(records, meta, out_dir):
    """Group tables + scaling views, as Markdown."""
    lines = ["# Benchmarks summary", "",
             f"- environment: {meta['quick']} mode, "
             f"{meta['records']} cases, wall time {meta['wall_seconds']:.1f}s",
             f"- platform: {meta['platform']}, python {meta['python']}, "
             f"numpy {meta['numpy']}",
             "-" * 60,
             "## Categories", "",
             "| category | cases | found | match `expect` | mean s | med s | max s |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    cats = {}
    for r in records:
        cats.setdefault(r["category"], []).append(r)
    for cat in sorted(cats):
        rs = cats[cat]
        n_expect = sum(1 for r in rs if r["match_expect"] is not None)
        hit = sum(1 for r in rs if r["match_expect"])
        mean_time = sum(r["elapsed"] for r in rs) / len(rs)
        times = sorted(r["elapsed"] for r in rs)
        med = times[len(times) // 2]
        lines.append(f"| {cat} | {len(rs)} | "
                     f"{sum(1 for r in rs if r['found'])} | "
                     f"{hit}/{n_expect} | {mean_time:6.2f} | {med:6.2f} | "
                     f"{max(times):7.2f} |")

    lines += ["", "## Slowest cases", "",
              "| case | category | elapsed | expanded | verdict |",
              "|---|---|---:|---:|---|"]
    slowest = sorted((r for r in records if r["match_expect"] is not False),
                     key=lambda r: -r["elapsed"])[:10]
    for r in slowest:
        verdict = "FOUND" if r["found"] else "miss"
        lines.append(f"| {r['label']} | {r['category']} "
                     f"| {r['elapsed']:.2f} | {r['expanded']} | {verdict} |")

    for cat, x_field in (("scaling-beam", "beam"),):
        rs = [r for r in records if r["category"] == cat and not r["found"]]
        if rs:
            lines += [f"## {cat}: expansions vs {x_field} (unfound targets)",
                      "", f"| {x_field} | elapsed | expanded | best score |",
                      "|---:|---:|---:|---:|"]
            for r in sorted(cats.get(cat, []), key=lambda r: r[x_field]):
                lines.append(f"| {r[x_field]} | {r['elapsed']:.3f} | "
                             f"{r['expanded']} | {r['best_score']:.4f} |")

    gs = [r for r in records if r["category"] == "scaling-gateset"]
    if gs:
        lines += ["## scaling-gateset", "",
                  "| subset | gate instances | elapsed | expanded | found |",
                  "|---|---:|---:|---:|---|"]
        for r in sorted(gs, key=lambda r: r["expanded"]):
            n_moves = r.get("n_moves", "")
            lines.append(f"| {r['label']} | {n_moves} | {r['elapsed']:.3f} "
                         f"| {r['expanded']} | {r['found']} |")

    ds = [r for r in records if r["category"] == "scaling-depth"]
    if ds:
        lines += ["## scaling-depth", "",
                  "| depth | elapsed | expanded | best score |",
                  "|---:|---:|---:|---:|"]
        for r in sorted(ds, key=lambda r: r["depth"]):
            lines.append(f"| {r['depth']} | {r['elapsed']:.3f} | "
                         f"{r['expanded']} | {r['best_score']:.4f} |")

    with open(os.path.join(out_dir, "summary.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main(argv=None):
    import numpy as np

    ap = argparse.ArgumentParser(prog="run_benchmarks",
                                 description=__doc__)
    ap.add_argument("--quick", action="store_true",
                    help="only quick_ok cases, tightened limits")
    ap.add_argument("--category", default=None,
                    help="only cases whose category contains this text")
    ap.add_argument("--only", default=None,
                    help="only cases whose label contains this text")
    ap.add_argument("--limit", type=int, default=None,
                    help="stop after this many cases")
    ap.add_argument("--time-limit", type=float, default=None,
                    help="override per-case time limit")
    ap.add_argument("--out-dir", default=None,
                    help=f"default: {RESULTS_DIR}")
    args = ap.parse_args(argv)

    out_dir = args.out_dir or RESULTS_DIR
    cases = build_cases()
    if args.quick:
        cases = [c for c in cases if c.quick_ok]
    if args.category:
        cases = [c for c in cases if args.category.lower() in c.category]
    if args.only:
        cases = [c for c in cases if args.only.lower() in c.label]
    if args.limit is not None:
        cases = cases[:args.limit]

    records = []
    t_start = time.perf_counter()
    for i, case in enumerate(cases):
        blurb = (f"{i + 1:3d}/{len(cases)} [{case.category:<18}] "
                 f"{case.label}")
        t0 = time.perf_counter()
        try:
            rec = run_case(case, override_time_limit=args.time_limit)
        except Exception as exc:                       # noqa: BLE001
            rec = {"index": case.index, "category": case.category,
                   "label": case.label, "error": f"{type(exc).__name__}: {exc}",
                   "found": False, "best_score": 0.0, "expanded": 0,
                   "elapsed": time.perf_counter() - t0, "match_expect": None}
        records.append(rec)
        print(f"{blurb:<58} -> {rec.get('error') or _fmt(rec)}",
              flush=True)

        meta = {
            "quick": args.quick,
            "records": len(records),
            "wall_seconds": time.perf_counter() - t_start,
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "expect_matched": sum(1 for r in records
                                  if r.get("match_expect")),
            "expect_total": sum(1 for r in records
                                if r.get("match_expect") is not None),
        }
        # checkpoint after every case so interrupted runs keep partial data
        write_outputs(records, meta, out_dir)
        write_summary(records, meta, out_dir)

    print(f"\n{meta['records']} cases, wall {meta['wall_seconds']:.1f}s; "
          f"expectations matched: {meta['expect_matched']}/"
          f"{meta['expect_total']}")
    print(f"results in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
