# Q-Synth: System Capabilities, Architecture, and Benchmarks

This document provides a comprehensive technical overview of **Q-Synth**, an open-source, modular quantum circuit synthesis and optimization framework. It details the internal algorithms, operational workflows, and empirical benchmarking results for each capability provided by the system.

---

## Table of Contents
1. [System Overview & Architectural Pillars](#1-system-overview--architectural-pillars)
2. [Capability 1: Unitary Matrix Synthesis](#2-capability-1-unitary-matrix-synthesis)
   - [Theoretical Foundations](#21-theoretical-foundations)
   - [Algorithms & Deduplication](#22-algorithms--deduplication)
   - [Step-by-Step Workflow](#23-step-by-step-workflow)
   - [Benchmarking & Empirical Results](#24-benchmarking--empirical-results)
3. [Capability 2: Boolean Function and Truth Table Synthesis](#3-capability-2-boolean-function-and-truth-table-synthesis)
   - [AST Parsing & Variable Inference](#31-ast-parsing--variable-inference)
   - [Quantum Oracle Paradigms (Bit-Flip, Phase, Permutation)](#32-quantum-oracle-paradigms)
   - [Reversible Gate Library](#33-reversible-gate-library)
   - [Step-by-Step Workflow](#34-step-by-step-workflow)
   - [Benchmarking & Empirical Results](#35-benchmarking--empirical-results)
4. [Capability 3: Quantum Circuit Optimization](#4-capability-3-quantum-circuit-optimization)
   - [Commutation Analysis & Peephole Rewriting](#41-commutation-analysis--peephole-rewriting)
   - [Global and Sliding-Window Resynthesis](#42-global-and-sliding-window-resynthesis)
   - [Allowed Gate Set Constraints](#43-allowed-gate-set-constraints)
   - [Step-by-Step Workflow](#44-step-by-step-workflow)
   - [Benchmarking & Empirical Results](#45-benchmarking--empirical-results)
5. [Capability 4: OpenQASM 2.0 Integration & Circuit Visualization](#5-capability-4-openqasm-20-integration--circuit-visualization)
   - [QASM 2.0 Parsing & Code Generation](#51-qasm-20-parsing--code-generation)
   - [ASCII Wire Diagram Renderer](#52-ascii-wire-diagram-renderer)
6. [Comparative Performance Summary](#6-comparative-performance-summary)
7. [Command-Line Interface (CLI) Reference](#7-command-line-interface-cli-reference)

---

## 1. System Overview & Architectural Pillars

Quantum computing algorithms are conceptualized at high levels of abstraction—as unitary matrices $U \in \mathrm{U}(2^n)$, Boolean functions $f: \{0,1\}^n \to \{0,1\}$, or classical permutations. However, physical quantum hardware executes only discrete sequences of native 1-qubit and 2-qubit gates constrained by physical noise, calibration drift, and coherence horizons ($T_1, T_2$).

**Q-Synth** bridges this compilation gap with a lightweight, pure Python/NumPy architecture designed for transparency, flexibility, and educational insight.

```
+---------------------------------------------------------------------------------------+
|                                    USER INPUTS                                        |
|  - Unitary Matrices (built-in, JSON, .npy, CSV)                                       |
|  - Boolean Expressions (AST validated, e.g. '(x0 and x1) ^ x2')                       |
|  - Truth Tables (bitstrings '0110', dicts, permutation mappings)                      |
|  - Existing Quantum Circuits (string format, OpenQASM 2.0, .qasm files)               |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                                  VALIDATION & PARSING                                 |
|  - Unitarity check: ||U† U - I|| < 1e-8                                               |
|  - Little-endian wire convention: q0 is Least Significant Bit (LSB)                   |
|  - Oracle embedding: bitflip (n+1 wires), phase (n wires), permutation (n wires)       |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                                    CORE ENGINES                                       |
|  [ SYNTHESIS ENGINE ]                                [ OPTIMIZATION ENGINE ]          |
|  • Move Enumeration P(n, k)                          • Commutation Analysis [A,B] = 0 |
|  • Kronecker Sub-word Embedding                      • Peephole Cancellation (H·H=I)  |
|  • Quantized Complex Hash Grid (1e9)                 • Gate Merging (T·T -> S)        |
|  • Beam-Search Pruning (Top-K)                       • Global & Windowed Resynthesis  |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                               VERIFICATION & DELIVERABLES                             |
|  - Hilbert-Schmidt Fidelity: s(U, V) = |Tr(U† V)| / 2ⁿ >= 1 - tol                     |
|  - Global Phase Extraction: phi = -arg(Tr(U† V))                                      |
|  - Max Element Reconstruction Error: max |U_jk - e^{i*phi} * V_jk|                    |
|  - OpenQASM 2.0 export & ASCII Wire Diagrams                                          |
+---------------------------------------------------------------------------------------+
```

---

## 2. Capability 1: Unitary Matrix Synthesis

### 2.1 Theoretical Foundations

Given a target unitary operator $U \in \mathrm{U}(2^n)$ and an allowable gate set $\mathcal{G} = \{g_1, \dots, g_m\}$, the synthesis objective is to find an ordered sequence of gate placements $C = (G_1, G_2, \dots, G_L)$ such that the accumulated matrix:
$$V = G_L G_{L-1} \cdots G_2 G_1$$
reproduces $U$ up to an unobservable global phase factor $\phi \in [-\pi, \pi)$:
$$U \approx e^{i\phi} V.$$

#### Distance and Similarity Metric
Physical quantum observables $\langle \psi | M | \psi \rangle$ are invariant under global phase transformations $|\psi\rangle \mapsto e^{i\phi} |\psi\rangle$. Consequently, Q-Synth uses the **normalized Hilbert--Schmidt trace similarity**:
$$s(U, V) = \frac{|\Tr(U^\dagger V)|}{2^n} \in [0, 1].$$

- $s(U, V) = 1$ if and only if $V = e^{-i\phi} U$ exactly.
- $s(U, V) = 0$ if $U$ and $V$ are completely orthogonal.

The corresponding phase-invariant distance is:
$$d(U, V) = \sqrt{1 - s(U, V)}.$$

When a sequence satisfies $s(U, V) \ge 1 - \epsilon$ (default $\epsilon = 10^{-9}$), the exact global phase $\phi$ and maximum element-wise error $\delta_{\max}$ are computed as:
$$\phi = -\arg(\Tr(U^\dagger V)), \qquad \delta_{\max} = \max_{j, k} \left| U_{jk} - e^{i\phi} V_{jk} \right|.$$

### 2.2 Algorithms & Deduplication

#### Move Enumeration & Placement
For an $n$-qubit register, each gate $g \in \mathcal{G}$ acting on $k_g$ wires is instantiated across every ordered permutation of wires:
$$N_{\text{placements}}(g) = P(n, k_g) = \frac{n!}{(n - k_g)!}.$$

For example:
- A 1-qubit gate on $n=3$ has $P(3, 1) = 3$ placements: $[0], [1], [2]$.
- A 2-qubit gate (like CNOT) on $n=3$ has $P(3, 2) = 6$ placements: $[0,1], [1,0], [0,2], [2,0], [1,2], [2,1]$.
- A 3-qubit gate (like Toffoli) on $n=3$ has $P(3, 3) = 6$ placements.

#### Kronecker Embedding
Each move is converted into a full $2^n \times 2^n$ matrix using bit-level sub-word projection:
$$\mathrm{Embed}(M_g, n, p)_{r, c} = \begin{cases} (M_g)_{r_p, c_p} & \text{if untouched bits of } r \text{ and } c \text{ agree}, \\ 0 & \text{otherwise}, \end{cases}$$
where $r_p = \sum_{w=0}^{k_g-1} ((r \gg p_w) \& 1) 2^w$ extracts the binary sub-word on the target wires.

#### Quantized Hash Grid Deduplication
In unconstrained tree search, candidate state space expands as $O(N_{\text{moves}}^d)$, quickly resulting in combinatorial explosion. Many gate sequences produce identical physical states (e.g., $X[0] X[1] = X[1] X[0]$). 

To prune redundant branches without floating-point hash instability, Q-Synth maps each matrix $V$ to an exact integer rounding key on a fine $10^9$ grid:
$$\mathrm{QuantizedHash}(V) = \mathrm{bytes}\left( \lfloor \mathrm{Re}(V) \cdot 10^9 \rceil, \lfloor \mathrm{Im}(V) \cdot 10^9 \rceil \right).$$
States with identical quantized hash keys are discarded immediately, retaining only unique candidate states before beam sorting.

### 2.3 Step-by-Step Workflow

```
[Target Specification]
  ├── Built-in name: --matrix swap
  ├── Inline JSON:   --matrix '[[0,1],[1,0]]'
  └── Matrix file:   --matrix-file unitary.npy
         │
         ▼
[Unitarity & Dimension Verification]
  └── Validates: U is square, dim == 2ⁿ, ||U† U - I|| < 1e-8
         │
         ▼
[Gate Library Loading & Move Precomputation]
  └── Loads JSON preset (e.g. gates/clifford_t.json)
  └── Computes all Embed(g, n, p) matrices
         │
         ▼
[Beam-Search Exploration Loop]
  ├── Depth d = 1 .. D:
  │     ├── Multiply: V_new = G_move @ V_base for all candidates
  │     ├── Evaluate score: s(U, V_new)
  │     ├── Check termination: s >= 1 - tol? If yes -> RETURN SUCCESS
  │     ├── Quantized hash deduplication (discard duplicates)
  │     └── Sort candidates descending by score, retain top-K (beam width)
  └── If max depth reached without match -> RETURN BEST EFFORT
         │
         ▼
[Verification & Reporting]
  └── Calculate similarity s, global phase phi, max element error
  └── Render ASCII circuit diagram & export OpenQASM 2.0 (if requested)
```

### 2.4 Benchmarking & Empirical Results

The unitary synthesis engine was evaluated against standard benchmarks using the test harness (`benchmarks/run_benchmarks.py`).

#### Benchmark 1: Exact Standard Gate Decompositions

| Target Unitary | Target Qubits | Gate Set Used | Allowed Subset | Search Depth | Expansions | Elapsed Time | Reconstructed Circuit | Similarity $s$ | Max Error |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| **SWAP** | 2 | Clifford+T | CNOT only | 3 | 9 | < 0.001 s | `CNOT[0,1] @ CNOT[1,0] @ CNOT[0,1]` | 1.0000000000 | 0.00 |
| **SWAP** | 2 | Clifford+T | Full (8 gates) | 3 | 137 | < 0.009 s | `CNOT[0,1] @ CNOT[1,0] @ CNOT[0,1]` | 1.0000000000 | 0.00 |
| **Hadamard** | 1 | Universal RXY | RX, RY, RZ ($\pi/4$) | 2 | 35 | < 0.001 s | `RY(-pi/2) @ RX(-pi)` | 1.0000000000 | $1.41 \times 10^{-16}$ |
| **CZ** | 2 | Clifford+T | CNOT, H | 3 | 19 | < 0.001 s | `H[1] @ CNOT[0,1] @ H[1]` | 1.0000000000 | 0.00 |
| **iSWAP** | 2 | Clifford+T | CNOT, H, S | 4 | 215 | 0.005 s | `CNOT[0,1] @ S[1] @ CNOT[1,0] @ CNOT[0,1]` | 1.0000000000 | $2.22 \times 10^{-16}$ |

#### Benchmark 2: Full Single-Qubit Clifford Group (`clifford24`)
The single-qubit Clifford group has 24 projective equivalence classes. Every single one was targeted using only $\{H, S\}$ as generators:
- **Total cases**: 24/24 found.
- **Accuracy**: 100.0% match with group-theoretic expectations.
- **Search time**: $< 0.001$ s per element (total group solved in 0.02 s).

#### Benchmark 3: Beam Width Scaling (`scaling-beam`)
Evaluating the impact of beam width $K$ on synthesizing the 2-qubit SWAP gate:

| Beam Width $K$ | Expansions | Elapsed Time (s) | Target Found | Final Depth |
| :---: | :---: | :---: | :---: | :---: |
| **25** | 301 | 0.008 s | Yes | 3 |
| **75** | 301 | 0.011 s | Yes | 3 |
| **225** | 301 | 0.009 s | Yes | 3 |
| **675** | 301 | 0.011 s | Yes | 3 |

*Finding*: Deduplication keeps unique states bounded, meaning expansion counts remain stable across beam widths when the solution sits within the early frontier.

---

## 3. Capability 2: Boolean Function and Truth Table Synthesis

### 3.1 AST Parsing & Variable Inference

Q-Synth synthesizes Boolean logic formulas directly into quantum circuits. Input expressions are parsed using Python's Abstract Syntax Tree (`ast`) module with explicit security constraints:

- **Allowed Nodes**: `ast.Expression`, `ast.Name`, `ast.Constant`, `ast.UnaryOp` (`not`, `~`, `+`, `-`), `ast.BinOp` (`&`, `|`, `^`, `+`, `*`), `ast.BoolOp` (`and`, `or`), and `ast.Compare` (`==`, `!=`).
- **Rejected Nodes**: Function calls (`ast.Call`), attribute lookups, loops, imports, and arbitrary statement execution.

#### Variable Ordering Convention
Variable names are automatically detected. When indexed variables are used (e.g., `x0, x1, x2` or `q0, q1`), Q-Synth extracts their numerical indices and assigns them to qubit wires accordingly:
$$x_i \mapsto \text{qubit wire } i.$$

Under the **little-endian convention**, integer row index $k \in [0, 2^n - 1]$ corresponds to assigning bit $(k \gg i) \& 1$ to variable $x_i$:
$$k = \sum_{i=0}^{n-1} b_i 2^i \implies x_i = b_i.$$

### 3.2 Quantum Oracle Paradigms

Q-Synth supports three primary quantum oracle embeddings:

```
(a) Bit-Flip Oracle (|x>|y> -> |x>|y ^ f(x)>)       (b) Phase Oracle (|x> -> (-1)^f(x) |x>)
    n input wires + 1 ancilla wire (n+1 total)            n input wires (0 ancilla overhead)

    q0: ─────■─────                                       q0: ─────■─────
             |                                                     |
    q1: ─────■─────                                       q1: ─────■───── (CZ phase kickback)
             |
    q2: ────[X]──── (ancilla flipped by f(x))
```

1. **Bit-Flip Oracle (`--oracle-mode bitflip`)**:
   $$U_{\text{bitflip}} \ket{x}\ket{y} = \ket{x}\ket{y \oplus f(x)},$$
   where $x \in \{0,1\}^n$ is placed on wires $0 \dots n-1$ and $y \in \{0, 1\}$ is on wire $n$. Matrix size: $2^{n+1} \times 2^{n+1}$.
2. **Phase Oracle (`--oracle-mode phase`)**:
   $$U_{\text{phase}} \ket{x} = (-1)^{f(x)} \ket{x}.$$
   Operates strictly on $n$ qubits with zero ancilla overhead. The resulting matrix is diagonal with diagonal entries $(-1)^{f(x)} \in \{+1, -1\}$.
3. **Permutation Oracle (`--oracle-mode permutation`)**:
   $$U_{\text{perm}} \ket{x} = \ket{f(x)}.$$
   Applies to reversible bijections $f: \{0,1\}^n \to \{0,1\}^n$. Matrix size: $2^n \times 2^n$.

### 3.3 Reversible Gate Library

To support classical reversible logic synthesis, Q-Synth includes `gates/reversible.json` with multi-qubit reversible gates:
- **X** (NOT): $\ket{x} \mapsto \ket{x \oplus 1}$
- **CNOT** (Feynman): $\ket{x_0, x_1} \mapsto \ket{x_0, x_1 \oplus x_0}$
- **SWAP**: $\ket{x_0, x_1} \mapsto \ket{x_1, x_0}$
- **CCX** (Toffoli): $\ket{x_0, x_1, x_2} \mapsto \ket{x_0, x_1, x_2 \oplus (x_0 \land x_1)}$
- **CSWAP** (Fredkin): $\ket{c, x_1, x_2} \mapsto \ket{c, x_2, x_1}$ if $c=1$.

### 3.4 Step-by-Step Workflow

```
[User Input Specification]
  ├── Boolean Formula:  --bool-expr "x0 and x1"
  └── Truth Table:      --truth-table "0110" or --truth-table-file table.txt
         │
         ▼
[AST Parsing & Truth Table Generation]
  └── Evaluates formula across all 2ⁿ input combinations
  └── Generates truth table vector: [f(0), f(1), ..., f(2ⁿ-1)]
         │
         ▼
[Oracle Matrix Construction]
  ├── Mode bitflip:     Constructs (n+1)-qubit permutation matrix
  ├── Mode phase:       Constructs n-qubit diagonal matrix with (-1)^f(x)
  └── Mode permutation: Constructs n-qubit bijection matrix
         │
         ▼
[Synthesis Engine Search]
  └── Beam search with allowed gates (e.g. Clifford+T or Reversible)
         │
         ▼
[Truth Table Display & Circuit Verification]
  └── Prints ASCII truth table comparison
  └── Verifies exact oracle fidelity s(U, V) == 1.0000000000
```

### 3.5 Benchmarking & Empirical Results

The Boolean synthesis pipeline was tested across both algebraic expressions and explicit truth tables:

| Target Function | Specification Format | Oracle Mode | Gate Library | Qubits | Expansions | Synthesis Time | Synthesized Gate Sequence | Fidelity $s$ |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| **XOR**: $x_0 \oplus x_1$ | `--bool-expr "x0 ^ x1"` | `bitflip` | Clifford+T | 3 | 10 | < 0.001 s | `CNOT[0,2], CNOT[1,2]` | 1.0000000000 |
| **AND Phase**: $x_0 \land x_1$ | `--bool-expr "x0 and x1"` | `phase` | Clifford+T | 2 | 15 | < 0.001 s | `CZ[0,1]` | 1.0000000000 |
| **AND Bit-flip**: $x_0 \land x_1$ | `--bool-expr "x0 and x1"` | `bitflip` | Reversible | 3 | 1 | < 0.001 s | `CCX[0,1,2]` | 1.0000000000 |
| **XOR Truth Table** | `--truth-table "0110"` | `bitflip` | Clifford+T | 3 | 10 | < 0.001 s | `CNOT[0,2], CNOT[1,2]` | 1.0000000000 |
| **Permutation Map** | `--truth-table "0->1, 1->0, 2->3, 3->2"` | `permutation` | Clifford+T | 2 | 2 | < 0.001 s | `X[0]` | 1.0000000000 |

*Key finding*: For $x_0 \land x_1$ under the phase oracle paradigm, Q-Synth automatically realizes that the phase kickback requires 0 ancillae and solves it using a single 2-qubit CZ gate in 15 expansions.

---

## 4. Capability 3: Quantum Circuit Optimization

### 4.1 Commutation Analysis & Peephole Rewriting

When a user supplies an existing circuit that may contain sub-optimal sequences or redundant gate pairs, Q-Synth's optimization engine applies a multi-pass reduction strategy.

#### Commutation Rule
Two operations $G_i$ on placement $p_i$ and $G_j$ on placement $p_j$ commute if:
$$[G_i, G_j] = G_i G_j - G_j G_i = 0.$$
- **Disjoint placements**: If $p_i \cap p_j = \emptyset$, $[G_i, G_j] = 0$ is guaranteed.
- **Diagonal gates**: Diagonal operations ($Z, S, T, CZ$) on overlapping wires commute with each other.

If $G_j$ commutes with all intermediate operations $G_{i+1}, \dots, G_{j-1}$, it is conceptually commuted adjacent to $G_i$:
1. **Inverse Cancellation**: If $G_j G_i \propto \mathbb{I}$, both gates are removed from the circuit. Examples:
   $$H[0] \cdot H[0] \to \emptyset, \qquad \CNOT[0,1] \cdot \CNOT[0,1] \to \emptyset.$$
2. **Gate Merging**: If $G_j G_i \propto G_{\text{allowed}}$ on the same placement, the two gates are replaced with the single combined gate. Example:
   $$T[0] \cdot T[0] \to S[0], \qquad S[0] \cdot S[0] \to Z[0].$$

### 4.2 Global and Sliding-Window Resynthesis

Peephole optimization alone cannot simplify non-adjacent subcircuits whose intermediate representations do not commute algebraically. To overcome this, Q-Synth employs two resynthesis passes:

1. **Global Resynthesis**:
   - Computes the overall circuit unitary matrix $U_{\text{target}} = \prod_{\ell=1}^M G_\ell$.
   - Launches beam search constrained to depth $M - 1$ using only the allowed gate set.
   - If an equivalent sequence of length $M' < M$ is found, the entire circuit is replaced.
2. **Sliding-Window Resynthesis**:
   - For long circuits exceeding global search depth, slides a window of width $w \in [2, W]$ (default $W=4$) across the circuit.
   - Computes the sub-unitary $U_{\text{window}} = \prod G_{\text{slice}}$.
   - Runs beam search to synthesize $U_{\text{window}}$ using $\le w - 1$ allowed gates.
   - When a shorter block is discovered, patches it into the circuit and re-triggers peephole reduction.

### 4.3 Allowed Gate Set Constraints

A key capability requested by users is restricting optimization to a specified gate set (e.g., using `--gate-names CNOT` or `--gates-file gates/clifford_t.json`). The optimizer guarantees that every gate in the output circuit belongs strictly to the allowable set.

### 4.4 Step-by-Step Workflow

```
[Raw Input Circuit]
  ├── Inline string: --circuit "H[0], CNOT[0,1], CNOT[0,1], H[0]"
  └── File input:    --circuit-file circuit.qasm
         │
         ▼
[Circuit Tokenization & Gate Mapping]
  └── Resolves gate names, parameters, and placements into Move tuples
         │
         ▼
[Pass 1: Commutation-Aware Peephole Reduction]
  ├── Eliminates identity gates
  ├── Commutes disjoint/commuting gates past each other
  ├── Cancels inverse pairs: G · G† = I
  └── Merges compatible rotations: T · T = S
         │
         ▼
[Pass 2: Global Resynthesis]
  └── Targets full circuit unitary U to depth <= |C| - 1
  └── If shorter circuit found -> Replace entire circuit
         │
         ▼
[Pass 3: Sliding-Window Block Resynthesis]
  └── For window widths w = W down to 2:
  │     ├── Extract sub-unitary U_block for slice C[i : i+w]
  │     ├── Beam-search resynthesize U_block with allowed gates to depth <= w - 1
  │     └── If reduction found -> Patch in-place & re-run Pass 1
         │
         ▼
[Verification Against Original Unitary]
  └── Verifies s(U_original, V_optimized) >= 1 - tol
  └── Reports gates saved, reduction percentage, phase, and max error
```

### 4.5 Benchmarking & Empirical Results

The optimizer was benchmarked across representative test cases:

| Input Circuit Description | Allowed Gate Basis | Input Gate Count | Output Gate Count | Gates Saved | Reduction Percentage | Passes Triggered | Verification Fidelity $s$ | Max Element Error |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| **Redundant H-CNOT pairs** (`H[0], CNOT[0,1], CNOT[0,1], H[0]`) | Clifford+T | 4 | **0** | 4 | **100.0%** | Peephole cancellation | 1.0000000000 | $2.22 \times 10^{-16}$ |
| **Double SWAP** ($6 \times \CNOT$) | CNOT only | 6 | **0** | 6 | **100.0%** | Peephole cancellation | 1.0000000000 | 0.00 |
| **Rotation Merging** (`T[0], T[0]`) | Clifford+T | 2 | **1** | 1 | **50.0%** | Peephole merging ($T \to S$) | 1.0000000000 | $2.23 \times 10^{-16}$ |
| **7-Gate Unoptimized SWAP** (`CNOT, H, H, CNOT, H, H, CNOT`) | CNOT only | 7 | **3** | 4 | **57.1%** | Global resynthesis | 1.0000000000 | $3.33 \times 10^{-16}$ |
| **Optimal 3-CNOT SWAP** (`CNOT, CNOT, CNOT`) | CNOT only | 3 | **3** | 0 | **0.0%** (already optimal) | Verification only | 1.0000000000 | 0.00 |

#### Highlight: Resynthesis of 7-Gate SWAP
A standard pedagogical circuit implements a SWAP gate using 7 gates:
$$C = \CNOT[0,1] \cdot (H[0] \otimes H[1]) \cdot \CNOT[0,1] \cdot (H[0] \otimes H[1]) \cdot \CNOT[0,1].$$

```
Original (7 gates):
q0: ──■─[H]──────■─[H]──────■──
q1: ──X─────[H]──X─────[H]──X──

Optimized with allowed basis {CNOT} (3 gates):
q0: ──■──X──■──
q1: ──X──■──X──
```

When restricted strictly to CNOT gates, peephole rules cannot simplify the circuit because the Hadamards do not commute past the CNOT control/target pins. However, Q-Synth's **Global Resynthesis** evaluates the composite unitary matrix, recognizes the SWAP permutation, and replaces all 7 gates with 3 CNOTs in $< 0.01$ seconds (**57.1% gate count reduction**).

---

## 5. Capability 4: OpenQASM 2.0 Integration & Circuit Visualization

### 5.1 QASM 2.0 Parsing & Code Generation

Q-Synth provides bidirectional compatibility with OpenQASM 2.0:

#### QASM Importer
The parser handles standard OpenQASM 2.0 syntax, including comments (`//`), header declarations (`OPENQASM 2.0;`, `include "qelib1.inc";`), quantum registers (`qreg q[n];`), single-qubit gates (`h`, `x`, `y`, `z`, `s`, `t`, `rx`, `ry`, `rz`), and entangling gates (`cx`, `cz`, `swap`, `ccx`, `cswap`).

#### QASM Exporter
Any synthesized or optimized circuit can be exported to standard OpenQASM 2.0 via `--qasm-out filename.qasm`:
```qasm
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
cx q[0], q[1];
cx q[1], q[0];
cx q[0], q[1];
```

### 5.2 ASCII Wire Diagram Renderer

To provide immediate visual feedback in CLI and terminal environments without requiring GUI tools or external packages, Q-Synth renders ASCII wire diagrams:

- **Single-qubit gates**: Rendered with bracketed labels (`[H]`, `[T]`, `[RX(pi/4)]`).
- **CNOT gates**: Control wire denoted with `■`, target wire denoted with `X`, connecting wires denoted with `┼`.
- **CZ gates**: Control and phase targets denoted with `■`.
- **SWAP gates**: Swap terminals denoted with `✕`.
- **Toffoli (CCX)**: Multi-controls denoted with `■`, target denoted with `X`.

```
Example 3-Qubit Toffoli Diagram:
q0: ──■──
q1: ──■──
q2: ──X──
```

---

## 6. Comparative Performance Summary

| Metric | Unitary Synthesis | Boolean Compilation | Circuit Optimization |
| :--- | :--- | :--- | :--- |
| **Input Modality** | Complex $2^n \times 2^n$ matrix | Boolean formula / Truth table | Gate list / OpenQASM 2.0 |
| **Typical Problem Size** | 1 to 3 qubits | 1 to 4 variables | Arbitrary circuit length |
| **Search/Run Time** | $< 0.01$ s (interactive) | $< 0.01$ s (interactive) | $< 0.01$ s to $0.1$ s |
| **Gate Reduction Potential** | N/A (synthesizes minimal sequence) | N/A (synthesizes direct oracle) | **50% to 100% reduction** |
| **Verification Metric** | $s(U, V) \ge 1 - 10^{-9}$ | $s(U_{\text{oracle}}, V) \ge 1 - 10^{-9}$ | $s(U_{\text{original}}, V_{\text{opt}}) \ge 1 - 10^{-9}$ |
| **Error Handling** | Unitarity validation ($10^{-8}$) | Safe AST parsing validation | Gate commutation verification |
| **Output Formats** | Ordered moves, QASM, ASCII | Truth table, QASM, ASCII | Stats, QASM, ASCII diagrams |

---

## 7. Command-Line Interface (CLI) Reference

### Unitary Synthesis Commands
```bash
# Synthesize SWAP gate from CNOTs only
python synthesizer.py --matrix swap --gates-file gates/clifford_t.json --gate-names CNOT

# Synthesize Hadamard from discrete rotation grid
python synthesizer.py --matrix h --gates-file gates/universal_rxy.json --depth 4

# Synthesize inline matrix
python synthesizer.py --matrix '[["sqrt2/2","sqrt2/2"],["sqrt2/2","-sqrt2/2"]]' --depth 3
```

### Boolean Function & Truth Table Commands
```bash
# Synthesize XOR bit-flip oracle
python synthesizer.py --bool-expr "x0 ^ x1" --gates-file gates/clifford_t.json --gate-names CNOT

# Synthesize AND phase oracle (0 ancilla overhead)
python synthesizer.py --bool-expr "x0 and x1" --gates-file gates/clifford_t.json --oracle-mode phase

# Synthesize AND bit-flip oracle using reversible Toffoli gates
python synthesizer.py --bool-expr "x0 and x1" --gates-file gates/reversible.json --gate-names CCX --show-diagram

# Synthesize truth table bitstring
python synthesizer.py --truth-table "0110" --gates-file gates/clifford_t.json --gate-names CNOT
```

### Circuit Optimization Commands
```bash
# Optimize redundant circuit
python synthesizer.py --circuit "H[0], CNOT[0,1], CNOT[0,1], H[0]"

# Optimize 7-gate SWAP to 3 CNOTs
python synthesizer.py --circuit "CNOT[0,1], H[0], H[1], CNOT[0,1], H[0], H[1], CNOT[0,1]" --gate-names CNOT

# Optimize QASM file and export optimized output
python synthesizer.py --circuit-file input.qasm --gates-file gates/clifford_t.json --qasm-out opt.qasm --show-diagram
```

### Built-in Demonstration
```bash
python synthesizer.py demo
```
Runs 8 showcase synthesis and optimization scenarios with verification statistics.
