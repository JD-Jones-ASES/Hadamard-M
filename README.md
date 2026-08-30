# Hadamard-M

An erratum on one 1991 construction, and one Hadamard matrix built by the sound
part of the same paper.

**The erratum.** Through its section 7 lists and the classical substitution of
its Proposition 1, Miyamoto 1991 claims a Hadamard matrix of order 2060: the
order-103 entry of list (2) feeds the order-515 entry of list (3), and the
remaining-unknowns list on p. 107 omits 515. That claim is unsupported by the
paper's own machinery. A parity test on the ingredient the route requires
decides the paper's printed list-(2) entries at n ≡ 3 (mod 4): the route is
reachable at 83, and impossible at 103, at 127 and at 151. The order-515 entry
— the only claim at Hadamard order 2060 located in our dated audit of the
literature, audit closed 2026-08-29 — therefore falls with 103, as does any
other list-(3) entry drawn from 103, 127 or 151. Cati and Pasechnik reach the
same entry independently: they record being "unable to verify these
constructions" there (arXiv:2411.18897v2, 2025-08-30), and the obstruction
below is the specific reason.

**The construction.** The paper's main theorem is sound. Applied to a publicly
announced Hadamard matrix of order 1948, it gives an explicit Hadamard matrix
of order 7796, verified here in exact integer arithmetic at a pinned digest.

## Definitions

**Hadamard matrix of order n.** A matrix H of order n with entries in {+1, −1}
and H·Hᵀ = n·I.

**Williamson-type quadruple of order n** (the paper's M-partition input). Four
±1 matrices A, B, C, D of order n, pairwise amicable (XYᵀ = YXᵀ), with
A·Aᵀ + B·Bᵀ + C·Cᵀ + D·Dᵀ = 4n·I.

**C₂-matrix ingredient.** The second hypothesis of the paper's Corollary 4, in
the reduced form derived in the note: two symmetric matrices D₁, D₂ of order m
with zero diagonal, off-diagonal entries in {+1, −1}, and every row sum 0,
satisfying D₁² + D₂² = 2m·I − 2·J, where J is the all-ones matrix.

## The erratum

Section 7 of Miyamoto 1991 lists 103 among the orders of Hadamard matrices of
M-partition, and lists 515 among the orders obtained from those by a
Baumert–Hall array; the remaining-unknowns list on p. 107 omits 515. The second
list is the claim of a Hadamard matrix of order 4·515 = 2060. Cati and Pasechnik
record the entry as unverified: missing details left them unable to verify the
construction. The gap can be made precise.

**The obstruction** (Proposition 3 of the note). Let m be odd and let D be a
matrix of order m that is symmetric, has zero diagonal, has off-diagonal
entries in {+1, −1}, and has every row sum 0. Then m ≡ 1 (mod 4).

*Proof.* Each row has m − 1 off-diagonal entries summing to 0, so exactly
(m − 1)/2 of them equal −1. The positions of the −1 entries are therefore the
edges of a graph on m vertices in which every vertex has degree (m − 1)/2. Its
edge count is m(m − 1)/4, an integer, so 4 divides m(m − 1). With m odd this
forces m ≡ 1 (mod 4). ∎

**Consequence** (Proposition 4 of the note). The C₂-matrix ingredient does not
exist for m ≢ 1 (mod 4). Corollary 4 of the paper therefore yields a
Williamson-type quadruple of order n = 2m + 1 only when n ≡ 3 (mod 8). Since
103 ≡ 7 (mod 8), it does not yield one at order 103, and the order-515 entry
that depends on it is unsupported. ∎

The test is sharp on the paper's own list. Writing m = (n − 1)/2 for the
printed list-(2) entries at n ≡ 3 (mod 4):

| n | 83 | 103 | 127 | 151 |
| --- | --- | --- | --- | --- |
| m = (n−1)/2 | 41 | 51 | 63 | 75 |
| m mod 4 | 1 | 3 | 3 | 3 |
| Corollary 4 instance possible | yes | **no** | **no** | **no** |

At n = 83 the hypothesis is satisfiable, since m = 41 ≡ 1 (mod 4), and there
the construction goes through; the note exhibits the ingredient explicitly from
the quadratic residues of Z₄₁. Any list-(3) entry drawn from 103, 127 or 151 is
affected exactly as 515 is.

The printed output order 4(2m + 3) on page 101 is a typo for 4(2m + 1): the
displayed ingredient has blocks of order m, and Corollary 4's own proof
substitutes them into Theorem 6 (p. 100), whose printed output order is
4(2m + 1). Both readings close at 103. Reaching 103 through the printed
4(2m + 3) would need m = 50, whose blocks would carry 49 off-diagonal ±1
entries per row summing to 0, which an odd count of ±1 entries cannot do.

The consequence is a statement about this paper's machinery, not a nonexistence
proof: a Williamson-type quadruple of order 103 from another source is not
excluded, and the paper supplies none. The note states the argument in full,
and the obstruction together with the emptiness of the ingredient class is
machine-checked in the companion Lean development; the transcriptions from the
printed paper remain human-audited.

## The construction

**The theorem** (Miyamoto 1991, Theorem 5 and Corollary 1; stated as Theorem
2.4 of Đoković, arXiv:1008.2043; §3.1 of the note). If q ≡ 1 (mod 4) is a
prime power and a Hadamard matrix of order q − 1 exists, then a Hadamard
matrix of order 4q exists.

The theorem never forms a C₂-matrix. Its second ingredient is an ordinary
Hadamard matrix of order q − 1, used only through K·Kᵀ = Kᵀ·K = (q − 1)·I, so
the obstruction has nothing to bite on. The hypotheses are disjoint from
Corollary 4's, and so are the failure modes.

Taking q = 1949 and a Hadamard matrix of order 1948 gives a Hadamard matrix of
order **7796**. The order-1948 input comes from the twelve matrices announced by
Alpöge's group at `x.com/__alpoge__/status/2087504785952182273` (2026-08-12);
the announcement tape is 23,828 characters with SHA-256
`5b5fe8fa42f0d6a8b4e4c9926726d82a6aab8e1070c1ae4d1b430c1277e58db4`. The seeds
are read from that tape, the order-1948 matrix is rebuilt by this laboratory's
own assembler and accepted by the trust chain before it is consumed, and the
order-7796 output is then accepted in turn.

Order 7796 is listed unresolved in Cati–Pasechnik Table 4 v2 (2025-08-30) as the
entry 1949(4), machine-diffed; re-checked at release date. The claim wording
this laboratory uses, and does not strengthen:

> The Cati–Pasechnik database (arXiv:2411.18897v2, 2025-08-30) records no
> Hadamard matrix of order 2²·1949; on that basis this is the first publicly
> accessible and independently reproducible construction of order 7796 located
> in our audit (audit closed 2026-08-29; re-checked at release date). A
> database records what its authors knew, not what exists.

The artifact itself is bound by the canonical SHA-256 pinned in
`certs/01-h7796/NOTES.md`; `run.py` rebuilds it from the banked seeds and hands
it to the trust chain on bare Python. Labels: PROVEN-BY-CERTIFICATE for the
artifact, REPORTED-FROM-AUDITED-TABLE for the status of the order.

## Replay

Everything runs from the repository root on bare Python 3.9 or newer, stdlib only.

```
python verify/verify.py --selftest
python certs/01-h7796/run.py
```

`verify/verify.py` is the trust chain. It accepts a matrix file only if the
matrix is square, has every entry in {+1, −1}, and satisfies H·Hᵀ = n·I, by
exact integer arithmetic on packed rows with no floating point anywhere. The
certificate rebuilds both matrices from the banked seeds, re-checks the
theorem's hypotheses on the actual matrices, hands each result to the trust
chain, and
compares the canonical SHA-256 in the verdict against the digest pinned in its
`NOTES.md`. Generated matrices go to `out/` or a temporary file, never
committed.

## Layout

| path | contents |
| --- | --- |
| `note/NOTE.md` | the note: the erratum in full, the construction, and each claim's cert |
| `verify/verify.py` | the trust chain: Hadamard check, exact arithmetic, stdlib only |
| `data/` | the banked order-487 seeds and the provenance pins |
| `certs/01-h7796/` | the replay: `run.py` and `NOTES.md` |

## Credits, license, provenance

The theorem is Miyamoto's, *A construction of Hadamard matrices*, JCTA 57
(1991) 86–108; the modern statement used here is Đoković's, arXiv:1008.2043.
The order-1948 matrix is from the announcement by Alpöge's group cited above.
The audited status table is Cati and Pasechnik, arXiv:2411.18897v2 (2025-08-30).

Code is MIT; see [LICENSE](LICENSE). The note (`note/`) and the prose
documentation in `data/` are CC BY-SA 4.0; see [LICENSE-DOCS](LICENSE-DOCS.md)
for the exact boundary. The banked seeds are mathematical data extracted from
a publicly announced payload; no license is claimed over them, and neither the
announcement tape nor the 1991 paper's scan is redistributed here. Authorship
is in [DISCLOSURE.md](DISCLOSURE.md).

Companion repository: [Hadamard-T](https://github.com/JD-Jones-ASES/Hadamard-T),
the T-matrix witnesses and the thirteen Hadamard orders built from them.
Formalization: [Hadamard-formal](https://github.com/JD-Jones-ASES/Hadamard-formal)
— a Lean 4 / Mathlib development whose public theorems include this note's
handshake parity obstruction (Proposition 3, as `handshake_mod_four`) and the
emptiness of the ingredient class it forbids (`no_handshake_matrix`), so the
erratum's mathematical core is kernel-checked.
