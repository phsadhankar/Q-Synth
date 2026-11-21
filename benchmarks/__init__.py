"""Benchmark suite for the quantum circuit synthesizer.

Run from the repository root:

    python -m benchmarks.run_benchmarks            # full suite (~10 min)
    python -m benchmarks.run_benchmarks --quick    # fast smoke suite
    python -m benchmarks.run_benchmarks --category scaling

Writes JSON / CSV / Markdown summaries under benchmarks/results/.
"""
