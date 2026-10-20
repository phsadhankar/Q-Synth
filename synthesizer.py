#!/usr/bin/env python
"""Entry point for the quantum circuit synthesizer CLI.

Examples:
    python synthesizer.py --matrix swap --gates-file gates/clifford_t.json
    python synthesizer.py --matrix h --gates-file gates/universal_rxy.json --depth 4
    python synthesizer.py demo
"""

import sys

from qcsynth.cli import main

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    sys.exit(main())
