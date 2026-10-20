# Quantum Circuit Synthesizer

A synthesis tool that automatically searches for the shortest sequence of
allowed gates whose matrix product reproduces a target unitary, up to a
global phase.

Given

* a target unitary `U` (a `2^n x 2^n` matrix), and
* a set of allowed gates defined in a JSON file,

the synthesizer runs a **beam search** over gate sequences and returns a
circuit `V` with `U = e^{i*phi} * V`, together with verification numbers
(similarity, global phase, max element error).

Currently an MVP: Python 3 + NumPy only, up to ~3 qubits.

## Quickstart

```
pip install -r requirements.txt
python synthesizer.py demo                                  # three example runs
python synthesizer.py --matrix swap --gates-file gates/clifford_t.json
python synthesizer.py --matrix h --gates-file gates/universal_rxy.json --depth 4
python synthesizer.py --matrix-file my_unitary.npy --gates-file gates/clifford_t.json --gate-names CNOT,H,T
```

Run the tests:

```
python -m pytest tests -q
```

## What is "beam"?

Beam search is a breadth-first search that does not keep every candidate.
Level by level, every kept circuit is extended by every allowed gate
instantiation, all extensions are scored, and only the `K` best are carried
on (`K` = "beam width"). Larger `K` searches more thoroughly but is
proportionally slower; if a run fails, raise `--beam` or `--depth`.

## Command line

```
python synthesizer.py
    --matrix swap | --matrix-file PATH   target unitary (one is required)
    --n N                                qubit count (inferred from target if omitted)
    --gates-file PATH                    JSON gate-set file (default gates/clifford_t.json)
    --gate-names CNOT,H,T                optional subset of the gate set to allow
    --depth D                            longest circuit to consider (default 8)
    --beam K                             beam width (default 2000)
    --tol TOL                            similarity that counts as exact (default 1e-9)
    --time-limit SECONDS                 give up after this long (best-effort best found)
    --quiet / --show-matrix              output options
```

Target units built in: `i x y z h s t` (1 qubit), `cnot cz swap` (2 qubits).
`--matrix-file` accepts `.npy` or text/CSV matrices (real numbers, `a+bj`
strings, or the `(a+bj)` format written by `numpy.savetxt`).

## JSON gate-set format

A gate-set file lists every allowed gate by name with its matrix:

```json
{
  "name": "preset display name",
  "gates": [
    { "name": "H", "qubits": 1,
      "matrix": [["sqrt2/2", "sqrt2/2"], ["sqrt2/2", "-sqrt2/2"]] },
    { "name": "RX", "qubits": 1,
      "matrix": [["cos(theta/2)", "-I*sin(theta/2)"],
                 ["-I*sin(theta/2)", "cos(theta/2)"]],
      "params": { "theta": ["pi/4", "pi/2", "pi", "-pi/4"] } }
  ]
}
```

* Each matrix element is a JSON **number**, a **string** expression
  (`sqrt2/2`, `exp(1j*pi/8)`; `^` is accepted for `**`), or a **pair**
  `[re, im]`. Available symbols: `I` (imaginary unit), `pi`, `e`, `sqrt2`,
  `sqrt3`, `sqrt`, `exp`, `sin`, `cos`, `tan`, `log`, `conj`, `abs`.
* A gate with `"params"` instantiates one concrete gate per parameter
  combination (labelled e.g. `RX(pi/4)`), keeping the search space finite.
* Loaded matrices are checked for unitarity, so a bad matrix cannot
  silently break synthesis.

Shipped presets: `gates/clifford_t.json` (X, Y, Z, H, S, T, CNOT, CZ) and
`gates/universal_rxy.json` (RX, RY, RZ on a pi/4 angle grid).

## Conventions and scoring

* **Little-endian**: global qubit 0 is the least significant bit of a basis
  index (same as Qiskit). `CNOT[0,1]` flips qubit 1 when qubit 0 is 1.
* Gates are embedded around their placement as a Kronecker product; the
  circuit matrix is the product `V = G_k @ ... @ G_2 @ G_1` where `G_1` is
  applied first.
* Similarity: `s = |Tr(U^dagger V)| / 2^n`; `s = 1` iff `V` equals `U` up to
  global phase. The found circuit is verified after every search and the
  phase and max element error are reported.

## Project layout

```
qcsynth/gates.py      gate-set JSON parsing, expression evaluator, unitarity check
qcsynth/search.py     gate embedding, beam search, verification
qcsynth/targets.py    built-in target unitaries, matrix file loading
qcsynth/cli.py        command line interface and demo
synthesizer.py        entry point
gates/*.json          gate-set presets
tests/test_synth.py   pytest suite (embedding, JSON parsing, known decompositions)
```

## Present limitations (next steps)

* Search is exponential with qubit count/depth: practical range is 1-2
  qubits interactively, 3 qubits for moderately short circuits.
* Parameterized gates must be given a finite value grid.
* No QASM/circuit-diagram export yet.
* Possible next steps: QASM export, circuit-cost weighting (e.g. 2-qubit
  gates cost more), A*/iterative-deepening upgrades, Solovay-Kitaev parser
  for approximation, longer-range SOTA comparison.
