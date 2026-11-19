# Quantum Circuit Synthesizer & Optimizer

A synthesis and optimization tool that automatically searches for the shortest
sequence of allowed gates whose matrix product reproduces a target unitary,
Boolean function, or truth table, and optimizes existing quantum circuits to
fewer gates using an allowed gate set.

Given:

* a target **unitary** (`2^n x 2^n` matrix), a **Boolean function** expression, or a **truth table**, or
* an existing **circuit** (via string, file, or OpenQASM 2.0) to optimize to fewer gates, and
* a set of **allowed gates** defined in a JSON file (or specified subset of gate names),

the synthesizer runs a **beam search** and algebraic reduction passes to return
an optimal circuit with verification numbers (similarity, global phase, max
element error), optional OpenQASM 2.0 export, and ASCII circuit diagrams.

Currently an MVP: Python 3 + NumPy only, up to ~3-4 qubits.

## Quickstart

```bash
pip install -r requirements.txt
python synthesizer.py demo                                  # run showcase demos
```

### 1. Boolean Function Synthesis
Synthesize quantum circuits for Boolean expressions into oracles:

```bash
# Bit-flip oracle (|x>|y> -> |x>|y ^ (x0 ^ x1)>) using CNOTs:
python synthesizer.py --bool-expr "x0 ^ x1" --gates-file gates/clifford_t.json --gate-names CNOT

# Phase oracle (|x> -> (-1)^f(x)|x>) for AND synthesized as CZ:
python synthesizer.py --bool-expr "x0 and x1" --gates-file gates/clifford_t.json --oracle-mode phase

# Toffoli oracle for AND using reversible gate set:
python synthesizer.py --bool-expr "x0 and x1" --gates-file gates/reversible.json --gate-names CCX --show-diagram
```

### 2. Truth Table Synthesis
Synthesize from bitstrings, lists, or mapping dictionaries:

```bash
# 2-input XOR truth table '0110' into 2 CNOTs:
python synthesizer.py --truth-table "0110" --gates-file gates/clifford_t.json --gate-names CNOT

# Truth table file or comma-separated format:
python synthesizer.py --truth-table "0, 1, 1, 0" --oracle-mode bitflip
```

### 3. Circuit Optimization to Fewer Gates
Optimize a user-provided circuit using allowed gates:

```bash
# Peephole cancellation of redundant operations (4 gates -> 0 gates):
python synthesizer.py --circuit "H[0], CNOT[0,1], CNOT[0,1], H[0]"

# Resynthesize a 7-gate SWAP circuit into the minimal 3 CNOTs:
python synthesizer.py --circuit "CNOT[0,1], H[0], H[1], CNOT[0,1], H[0], H[1], CNOT[0,1]" --gate-names CNOT

# Gate merging (T + T -> S):
python synthesizer.py --circuit "T[0], T[0]"

# Optimize OpenQASM file and export optimized QASM:
python synthesizer.py --circuit-file input.qasm --qasm-out optimized.qasm --show-diagram
```

### 4. Unitary Matrix Synthesis
```bash
python synthesizer.py --matrix swap --gates-file gates/clifford_t.json
python synthesizer.py --matrix h --gates-file gates/universal_rxy.json --depth 4
python synthesizer.py --matrix-file my_unitary.npy --gates-file gates/clifford_t.json --gate-names CNOT,H,T
```

Run the tests:

```bash
python -m pytest tests -q
```

## Command Line Reference

```
python synthesizer.py [options]

Target inputs (choose one):
    --bool-expr EXPR             Boolean expression, e.g. '(x0 and x1) ^ x2' or 'a & b | ~c'
    --truth-table SPEC           Truth table: bitstring ('0110'), list ('0,1,1,0'), or mapping
    --truth-table-file PATH      Path to file containing a truth table
    --oracle-mode MODE           'bitflip' (|x>|y> -> |x>|y^f(x)>, n+1 qubits, default),
                                 'phase' (|x> -> (-1)^f(x)|x>, n qubits), or
                                 'permutation' (|x> -> |f(x)>, n qubits)
    --matrix NAME|JSON           Built-in name (swap, cnot, cz, ccx, toffoli, cswap, x, y, z, h, s, t)
                                 or inline JSON matrix
    --matrix-file PATH           Target unitary from .npy or text/CSV file

Circuit optimization:
    --circuit OPS                Input circuit to optimize, e.g. 'H[0], CNOT[0,1], H[0]'
    --circuit-file PATH          File containing circuit (.txt or OpenQASM .qasm)
    --optimize                   Flag to optimize the input circuit (inferred if --circuit is given)
    --window-size W              Sliding window size for block resynthesis (default 4)

Allowed gate specification:
    --gates-file PATH            JSON gate-set file (default: gates/clifford_t.json)
    --gate-names N1,N2,...       Optional subset of gates from the gate set to allow

Search parameters:
    --n N                        Number of qubits (inferred from target/circuit if omitted)
    --depth D                    Maximum circuit depth to search (default: 8)
    --beam K                     Beam width: candidate circuits kept per depth (default: 2000)
    --tol TOL                    Similarity tolerance treated as exact match (default: 1e-9)
    --time-limit SECONDS         Timeout in seconds

Output options:
    --show-diagram               Display ASCII quantum circuit diagram
    --qasm-out PATH              Export result to OpenQASM 2.0 file
    --show-matrix                Print the full unitary matrix
    --quiet                      Suppress step-by-step progress
```

## Shipped Gate Set Presets

* `gates/clifford_t.json`: Clifford+T basis (X, Y, Z, H, S, T, CNOT, CZ).
* `gates/reversible.json`: Reversible classical/quantum logic (X, CNOT, CCX/Toffoli, SWAP, CSWAP/Fredkin).
* `gates/universal_rxy.json`: Discrete single-qubit rotations (RX, RY, RZ on a pi/4 angle grid).

## How Optimization Works

When optimizing a circuit given by the user with specified allowed gates:
1. **Commutation-Aware Peephole Reduction**: Checks if gates commute across intermediate operations. Cancels adjacent self-inverses ($H H = I$, $C_X C_X = I$) and merges mergable gates ($T T = S$).
2. **Global Resynthesis**: Computes the circuit's overall unitary matrix $U$ and performs beam search with the allowed gates up to `depth = len(circuit) - 1`. If an equivalent shorter sequence is found, it replaces the entire circuit.
3. **Sliding-Window Block Resynthesis**: For longer circuits, slides a window of size $W \in [2, \text{window\_size}]$, computes the sub-unitary, and resynthesizes smaller blocks using allowed gates into strictly fewer gates.
4. **Verification**: Verifies that the optimized circuit matrix matches the original unitary up to global phase ($\text{similarity} \ge 1 - \text{tol}$).

## Conventions

* **Little-endian**: global qubit 0 is the least significant bit (LSB) of a basis index (same as Qiskit).
* **Similarity score**: $s = |\text{Tr}(U^\dagger V)| / 2^n$; $s = 1$ if and only if $V$ matches $U$ up to a global phase.
