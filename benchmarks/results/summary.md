# Benchmarks summary

- environment: True mode, 189 cases, wall time 17.0s
- platform: Windows-11-10.0.26300-SP0, python 3.14.4, numpy 2.4.1
------------------------------------------------------------
## Categories

| category | cases | found | match `expect` | mean s | med s | max s |
|---|---:|---:|---:|---:|---:|---:|
| basic | 8 | 8 | 8/8 |   0.00 |   0.00 |    0.00 |
| clifford24 | 24 | 24 | 24/24 |   0.00 |   0.00 |    0.00 |
| haar-1q | 10 | 0 | 10/10 |   1.08 |   0.06 |    2.76 |
| known-1q-pairs | 43 | 43 | 43/43 |   0.00 |   0.00 |    0.00 |
| known-2q-products | 80 | 80 | 80/80 |   0.02 |   0.00 |    0.09 |
| named-2q | 5 | 3 | 3/4 |   0.23 |   0.09 |    0.71 |
| not-found-1q | 6 | 0 | 6/6 |   0.01 |   0.00 |    0.07 |
| scaling-beam | 4 | 4 | 4/4 |   0.01 |   0.01 |    0.01 |
| scaling-gateset | 6 | 6 | 6/6 |   0.00 |   0.00 |    0.01 |
| stress-3q | 3 | 3 | 3/3 |   0.10 |   0.02 |    0.28 |

## Slowest cases

| case | category | elapsed | expanded | verdict |
|---|---|---:|---:|---|
| haar1q-07|RXY | haar-1q | 2.76 | 102168 | miss |
| haar1q-02|RXY | haar-1q | 2.71 | 102168 | miss |
| haar1q-03|RXY | haar-1q | 2.60 | 102168 | miss |
| haar1q-06|RXY | haar-1q | 2.55 | 102168 | miss |
| sqrt-SWAP | named-2q | 0.71 | 28240 | miss |
| H-H-H | stress-3q | 0.28 | 9102 | FOUND |
| SWAP o Y[0] (after) | known-2q-products | 0.09 | 2973 | FOUND |
| SWAP o Y[1] (after) | known-2q-products | 0.09 | 2973 | FOUND |
| iSWAP|full-preset | named-2q | 0.09 | 2813 | FOUND |
| SWAP o Y[1] (before) | known-2q-products | 0.09 | 2973 | FOUND |
## scaling-gateset

| subset | gate instances | elapsed | expanded | found |
|---|---:|---:|---:|---|
| SWAP|gates-CNOT |  | 0.000 | 9 | True |
| SWAP|gates-CNOT+CZ |  | 0.001 | 21 | True |
| SWAP|gates-CNOT+H |  | 0.001 | 31 | True |
| SWAP|gates-CNOT,CZ+H |  | 0.002 | 51 | True |
| SWAP|gates-CNOT,CZ,H+T |  | 0.002 | 85 | True |
| SWAP|gates-full-CT |  | 0.009 | 301 | True |
