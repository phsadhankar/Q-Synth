#!/usr/bin/env python
"""Entry point for the benchmark suite (see benchmarks/runner.py)."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if __name__ == "__main__":
    from benchmarks.runner import main

    sys.setrecursionlimit(10000)
    sys.exit(main())
