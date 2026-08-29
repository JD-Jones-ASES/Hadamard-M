# Provenance of the data files

`data/h1948-seeds.json` holds the four ±1 seeds of length 487 that generate
H(1948), together with the Goethals-Seidel parameters that consume them. It is
the only input to the construction in `certs/01-h7796`.

`data/cp-table4-v2.json` holds all 195 entries of Table 4 of Cati and
Pasechnik, *A database of constructions of Hadamard matrices*,
arXiv:2411.18897**v2** (2025-08-30), transcribed from the arXiv LaTeX e-print
and machine-diffed against it, 195/195 agreeing, on 2026-08-29; an entry `n(m)`
means `m` is the least exponent with `2ᵐ·n` recorded known, the table covers
odd `n ≤ 2999`, and `m = 2` entries are omitted because those orders are known.
Stage 5 of the certificate reads it; it feeds no construction, only the dated
openness reading, which is labelled REPORTED-FROM-AUDITED-TABLE.
`sha256 = 74bdb560ccfb63bafbd717270c43b030a5db9a8a42f1c4131142aa3d2b151362`
(3620 bytes).

## Where the seeds come from

- **Public announcement.** `x.com/__alpoge__/status/2087504785952182273`,
  posted 2026-08-12 by Alpoge's group, announcing twelve Hadamard orders.
- **Payload digest.** The announcement tape is 23 828 characters, with
  `sha256 = 5b5fe8fa42f0d6a8b4e4c9926726d82a6aab8e1070c1ae4d1b430c1277e58db4`.
  This digest is the object this repository pins.
- **The bytes used here.** Tape positions `[19916:21864]`, four ±1 seeds of
  length 487, banked verbatim as the `seeds` field of `h1948-seeds.json`.
- **The construction they encode.** A plain Goethals-Seidel array over the
  cyclic group `Z₄₈₇`: `s = 0`, `r_shift = ρ = 486 ≡ −1`, which is the
  classical back-diagonal `R`, standard block pattern. This laboratory decoded
  the tape and replays the array with its own code. The announcer's decoder was
  not executed here.

The rebuilt matrix is required to be `verify.py`-green at canonical
`sha256 = fddc841ebf951f6e17e939551d058ea5df046251ea065b5f6e7ee2fd8d0f62ce`
before anything is built on top of it. `certs/01-h7796/run.py` enforces that.

## How equality is claimed, and how it is not

A public mirror of the announcement exists at `github.com/foocker/Hadamard668`
(created 2026-08-13). Its `answer.md` copy of the announcement tape carries the
digest recorded above. Its decoded copy of the H(1948) **matrix** is truncated
at row 604.

**The law this repository follows.** Any equality claim about the H(1948) input
cites the announcement URL and the tape `sha256`, and the canonical `sha256` of
the rebuilt matrix. No claim of byte-equality against the mirrored matrix file
is made anywhere in this repository, because that file is incomplete.

## Credit

The H(1948) payload is Alpoge's group's announcement of 2026-08-12. This
repository contributes the decode, the replay, the composite construction of
`certs/01-h7796`, and the certificate. It does not contribute the input.
