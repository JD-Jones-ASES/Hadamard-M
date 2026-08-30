# Certificate 01 — H(7796) = H(4·1949)

## Statement

**The theorem.** Miyamoto, *A construction of Hadamard matrices*, JCTA **57**
(1991) 86–108, Theorem 5 / Corollary 1. The same statement appears as Theorem
2.4 of Đoković, arXiv:1008.2043, in the form used here:

> If `q ≡ 1 (mod 4)` is a prime power and there exists an Hadamard matrix of
> order `q − 1`, then there exists an Hadamard matrix of order `4q`.

**The substitution.** `q = 1949 = 4·487 + 1`, prime, with `H(1948)` as the
second ingredient. Derived parameters: `m = (q−1)/2 = 974`, `n = 2m + 1 = q`,
output order `4n = 7796`. The construction is deterministic. There is no
search and no random number generator anywhere in the chain.

**The input, and where it comes from.** `H(1948)` is one of the orders in the
public announcement of 2026-08-12 by Alpoge's group
(`x.com/__alpoge__/status/2087504785952182273`). This laboratory decoded the
announcement tape; the four ±1 seeds of length 487, the tape digest, and the
law governing equality claims are in [`../../data/PROVENANCE.md`](../../data/PROVENANCE.md).
`run.py` rebuilds the matrix from those seeds through the plain
Goethals-Seidel array over `Z₄₈₇` and requires it to be `verify.py`-green at
its pinned digest **before** it is consumed.

**The output.** An Hadamard matrix of order 7796, canonical
`sha256 = 151d33f6d404d2bb3ca4aa562aa3fb20b49a6a8ae1c5b91fee0d14800b6b0a75`.
The canonical digest is the SHA-256 of the `'+'`/`'-'` serialisation, one row
per line, which `verify.py` prints in its own verdict.

**Label: PROVEN-BY-CERTIFICATE.** `H(7796)` exists and is reproducible from
this directory plus `data/`.

By Sylvester doubling, `H(2) ⊗ H(7796)` gives **`H(15592) = 2·7796`**. That is
stated as a corollary and is **not built** here.

## How to run

From the repository root, on bare `python3 ≥ 3.9`. Standard library only, no
numpy, exact integer arithmetic throughout, no floats.

```
python verify/verify.py --selftest        # the trust chain, exit 0
python certs/01-h7796/run.py              # the full certificate, exit 0
python certs/01-h7796/run.py --gate-only  # stages 1, 2, 4, 5, ~2 s
```

Recorded run (2026-08-29, Python 3.14.2, single process): **44.3 s wall, 80
checks green, zero failures, exit 0**, of which `verify.py` on the order-7796
artifact is 23 s. A second run took 45.4 s and produced the identical digests.
Generated matrices are written to `out/` and deleted after verification. They
are never committed. Peak disk 61 MB.

## What the run establishes, and the expected verdict lines

| stage | what it does |
| --- | --- |
| 1 | grounding gate: the *same* code path at `q = 5` from the Sylvester `H(4)` and at `q = 257` from the Sylvester `H(256)`, each output green at a pinned digest. At `q = 5` the packed-integer dot product is calibrated against a naive `O(n³)` triple loop, and the output is re-checked by an independent popcount path. |
| 2 | rebuilds `H(1948)` from `data/h1948-seeds.json` and greens it at its pinned digest before use |
| 3 | `q = 1949`: `C Cᵗ = qI` at order 1950; the E-form entry for entry; `e(C1) = 1, e(C2) = 0, e(C4) = 1` in rows and columns; `C1C1ᵗ + C2C2ᵗ = qI − 2J`, `C2ᵗC2 + C4C4ᵗ = qI − 2J`, `C1C2 = C2C4ᵗ`; `K Kᵗ = 1948·I` and all six K-block identities; (4.1), (4.2), (4.9) `U Uᵗ = nI − 2(I₄ ⊗ J_m)` at order 3896, (4.10) `V Vᵗ = nI` at order 3896. Then assemble, write, verify, pin. |
| 4 | negative control: one flipped entry of the verified `H(20)` must be rejected by `verify.py` with exit 1 |
| 5 | prints the openness reading with its label |

Four green verdict lines, verbatim as `verify.py` prints them:

```
VERDICT: HADAMARD order=20 all 190 row pairs orthogonal canonical_sha256=18efd3fec26689d5721f1058a6520facae1a0b5122f939bad7a8165d701233bc
VERDICT: HADAMARD order=1028 all 527878 row pairs orthogonal canonical_sha256=7e95741ba1409081bb4abe2981c72f549f537ccb6a5335ea83fce63b7eabc134
VERDICT: HADAMARD order=1948 all 1896378 row pairs orthogonal canonical_sha256=fddc841ebf951f6e17e939551d058ea5df046251ea065b5f6e7ee2fd8d0f62ce
VERDICT: HADAMARD order=7796 all 30384910 row pairs orthogonal canonical_sha256=151d33f6d404d2bb3ca4aa562aa3fb20b49a6a8ae1c5b91fee0d14800b6b0a75
```

and one red one, which is the control and must appear:

```
VERDICT: FAIL order=20 non-orthogonal row pairs (first 5): [(0, 3), (1, 3), (2, 3), (3, 4), (3, 5)] canonical_sha256=77eb68f8345521a2c261dfbe49d453330104d5c8ac4ae78fa9451aa074f5819a
```

The gate digests at `q = 5` and `q = 257` are pinned in `run.py`, not merely
`verify.py`-green. The order-1028 output reproduces, bit for bit, an `H(1028)`
this laboratory built earlier with an independently written implementation of
the same theorem, so the generalisation to `q = 1949` did not drift.

Miyamoto's prose is scaffolding here, never load-bearing: the engine is
certified against a known answer, every hypothesis is re-checked on the actual
matrices at the `q` being run, and the output is accepted only by `verify.py`.

## The openness of order 7796, which is a separate claim with a separate label

**Label: REPORTED-FROM-AUDITED-TABLE** (Cati and Pasechnik, *A database of
constructions of Hadamard matrices*, arXiv:2411.18897**v2**, 2025-08-30, Table
4; transcribed from the arXiv LaTeX e-print and machine-diffed; retrieved
2026-08-29). Đoković (arXiv:1008.2043, p. 1–2) records that the corresponding
Handbook table "was not accurate even at the time of its publication".

The transcription is published here as `data/cp-table4-v2.json` (195 entries;
see `data/PROVENANCE.md`), and **stage 5 reads it** rather than quoting a
constant: it asserts that the file loads with all 195 entries at odd
`n ≤ 2999`, that the entry for `n = 1949` reads `m = 4`, and that `m = 4`
therefore puts the smallest recorded `2ᵗ·1949` at `2⁴·1949 = 31184` — so
neither `4·1949 = 7796` nor `8·1949 = 15592` was recorded known there. The
matrix built above settles the second by Sylvester doubling. Re-check at
release date.

The wording this repository uses, and does not strengthen:

> The Cati–Pasechnik database (arXiv:2411.18897v2, 2025-08-30) records no
> Hadamard matrix of order 2²·1949; on that basis this is the first publicly
> accessible and independently reproducible construction of this order located
> in our audit. A database records what its authors knew, not what exists.

## Credit, and what is not claimed here

The theorem is Miyamoto's and the input matrix is Alpoge's group's; this
laboratory contributes neither. Cati and Pasechnik already implement the
theorem; their footnote credits it at `q = 853, 1093, 1669, 1789, 1913, 1933,
2053, 2269, 2341`. What was missing on 2025-08-30 was `H(1948)`, and that came
from the announcement of 2026-08-12. This closure is a direct corollary of the
second against the first.

The propagation is mechanical, and the two inputs are public. A parallel
closure elsewhere is plausible and would not be visible from here. What this
laboratory contributes is the firsthand decode of the input, the
standard-library implementation, and this certificate.

## Scope

`H(15592)` is stated as a corollary of the artifact above by Sylvester
doubling, and is not built here. The openness of order 7796 is not proved here
either; it is reported from a dated table, with the label above. What this
certificate binds, and nothing more, is the existence of `H(7796)`, its
reproducibility from this repository plus `data/`, and the correctness of the
substitution into Miyamoto's Theorem 5 / Corollary 1.
