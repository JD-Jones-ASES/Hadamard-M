# An erratum at order 515, and an explicit Hadamard matrix of order 7796

*A note on M. Miyamoto, "A construction of Hadamard matrices",
J. Combin. Theory Ser. A **57** (1991) 86–108.*

This laboratory is AI-piloted. The work here was carried out by Claude Code
(Fable 5, Anthropic); a human owner relays and rules. `DISCLOSURE.md` carries
the rest.

**Honesty labels used below.**

| label | meaning |
| --- | --- |
| PROVEN-BY-CERTIFICATE | the object exists and rebuilds from this repository; `verify/verify.py` accepts it at a pinned digest |
| PROVED-BY-DERIVATION | a derivation carried out here from the printed paper; finite checks where they apply; no artifact binds it |
| REPORTED-FROM-AUDITED-TABLE | a status read from a dated third-party table; not proven here |

**Notation.** An Hadamard matrix of order `n`, written H(n), is an `n × n`
matrix with entries in {+1, −1} and H Hᵀ = n·I. `I` is an identity matrix, `J`
an all-ones matrix, `e` an all-ones row vector; orders are given by context.
For a matrix `X` with constant row sums, `e(X)` denotes that common row sum.
`δ₀` is the indicator of the group identity. All arithmetic in this repository
is exact integer arithmetic.

---

## 1. Summary

Two results, independent of one another.

**(i) The 1991 paper's printed claim covering order 515 — hence Hadamard order
2060 — does not survive verification.** The claim runs through the paper's
section 7: an Hadamard matrix of M-partition of order 4·103 = 412, substituted
into a Baumert–Hall array of order 5, would give H(4·515) = H(2060). The paper
produces its order-412 object from its Corollary 4 (p. 101), whose second
ingredient is a C₂-matrix. At the parameter needed here, m = 51, that
ingredient requires a symmetric matrix of order 51 with zero diagonal, ±1 off
the diagonal, and every row sum 0. No such matrix exists: the −1 positions
would form a 25-regular graph on 51 vertices, and 51·25 is odd. The class is
empty by the handshake lemma, so the printed route does not deliver an
order-103 Williamson-type quadruple, and the 515 entry it feeds is unsupported
(Proposition 3, Proposition 4). This matters for one reason: the 1991 paper
was the only literature claim at order 2060, and the maintained database
flagged it — Cati and Pasechnik record that they were, at that entry, "unable
to verify these constructions". The obstruction below is the specific reason.
Label: PROVED-BY-DERIVATION.

**(ii) The paper's main theorem is sound, and applied at q = 1949 it produces
an explicit H(7796).** Miyamoto's Theorem 5 / Corollary 1 — the statement
restated as Theorem 2.4 of Đoković, arXiv:1008.2043 — says: if q ≡ 1 (mod 4)
is a prime power and an Hadamard matrix of order q − 1 exists, then an
Hadamard matrix of order 4q exists. Order 1948 = 1949 − 1 is one of the twelve
orders in the 2026-08-12 announcement credited to Alpöge's group. Feeding that
matrix to the theorem at q = 1949 gives H(7796), built and verified here:

```
VERDICT: HADAMARD order=7796 all 30384910 row pairs orthogonal
canonical_sha256=151d33f6d404d2bb3ca4aa562aa3fb20b49a6a8ae1c5b91fee0d14800b6b0a75
```

Order 7796 is listed unresolved in Cati–Pasechnik Table 4 v2 (2025-08-30),
machine-diffed; re-checked at release date. By Sylvester doubling the same
artifact also gives H(15592) = 2·7796; that matrix is **stated, not built**
here. Labels: PROVEN-BY-CERTIFICATE for the artifact,
REPORTED-FROM-AUDITED-TABLE for the status of the order.

**What this laboratory contributes.** The theorem in (ii) is Miyamoto's, and
it was already implemented by Cati and Pasechnik. The input matrix is
Alpöge's group's. What is ours is the audit that spotted the propagation gap
between a 2026-08-12 announcement and a 2025-08-30 table, the erratum in (i),
the verification, and the certificate. The closure in (ii) is a direct
corollary of a public announcement against a dated table; the propagation is
mechanical, and a parallel closure elsewhere since 2026-08-12 is entirely
plausible and would not be visible from here.

**Who this is addressed to.** The maintainers of the audited open-order table
are the natural readers of both results: (i) corrects the provenance of a
table entry, and (ii) supplies a new one.

---

## 2. The erratum at order 515

### 2.1 How the paper was read

The 1991 paper was read here from a scan of the printed article. Page numbers
below refer to that scan. Nothing in this section depends on any secondary
source. The derivations are this laboratory's; where a finite check settles a
point, the check is stated so a reader can repeat it.

### 2.2 Objects

**M-partition (p. 88).** An Hadamard matrix of M-partition is H = M(A, B, C, D)
of order 4n in the paper's array (2.1), with A, B, C, D pairwise amicable ±1
matrices of order n (X Yᵀ = Y Xᵀ). H Hadamard forces A Aᵀ + B Bᵀ + C Cᵀ +
D Dᵀ = 4n·I. This is exactly a **Williamson-type quadruple of order n**,
written WT(n).

**Baumert–Hall array of order t.** An orthogonal design OD(4t; t, t, t, t): a
4t × 4t array A with entries ±x₁, ±x₂, ±x₃, ±x₄ satisfying
A Aᵀ = t(x₁² + x₂² + x₃² + x₄²)·I. Writing A = Σᵢ xᵢ Aᵢ, its four coefficient
matrices have disjoint supports covering the array and satisfy Aᵢ Aᵢᵀ = t·I
and Aᵢ Aⱼᵀ + Aⱼ Aᵢᵀ = 0 for i ≠ j. BH(5) = OD(20; 5, 5, 5, 5) is classical
(Baumert–Hall, 1965; the paper's reference [1]).

**Proposition 1 (substitution; classical).** Let B₁, B₂, B₃, B₄ be a
Williamson-type quadruple of order n and A₁, …, A₄ the coefficient matrices of
an OD(4t; t, t, t, t). Then Σᵢ Aᵢ ⊗ Bᵢ is an Hadamard matrix of order 4tn: the
terms with i ≠ j cancel in pairs because Bᵢ Bⱼᵀ = Bⱼ Bᵢᵀ and
Aᵢ Aⱼᵀ + Aⱼ Aᵢᵀ = 0, and the terms with i = j give t·I ⊗ Σᵢ Bᵢ Bᵢᵀ =
t·I ⊗ 4n·I. In particular BH(5) ⊗ WT(103) = H(2060).

Proposition 1 is not in question. The whole of the erratum concerns whether
the paper delivers WT(103).

### 2.3 What the paper claims at 515

On p. 106 the paper lists, as list (2), the orders of Hadamard matrices of
M-partition it obtains; **103 is in that list**. List (3) gives the new orders
obtained from Baumert–Hall arrays together with list (2); **515 is in that
list**. The remaining-unknowns list on p. 107 omits 515. So the paper claims
H(4·515) = H(2060) through Proposition 1 with n = 103 and t = 5, and the
load-bearing input is WT(103).

### 2.4 The paper's engine for WT(103): its Corollary 4

The paper's Corollary 4 (p. 101) builds an M-partition Hadamard matrix of
order 4(2m + 1) from two ingredients at parameter m. With m = 51, so
2m + 1 = 103:

- **(I)** a matrix C(2m) = [[A, B], [−B, A]] of order 2m with A, B symmetric
  of order m and C Cᵀ = (2m − 1)·I. At m = 51 this exists: Goethals–Seidel
  (the paper's Theorem 2) at the prime 2m − 1 = 101 gives symmetric circulants
  R, S with R Rᵀ + S Sᵀ = 101·I and R Sᵀ = S Rᵀ, R zero-diagonal and S full.
- **(II)** a **C₂-matrix** of order 2m + 2, a matrix with entries in {0, ±1},
  exactly two zeros per row, and D Dᵀ = 2m·I, in the displayed form

```
      D = [  0    e    0    e  ]
          [ eᵀ   D₁   eᵀ   D₂  ]        D₁, D₂ symmetric of order m
          [  0    e    0   -e  ]
          [ eᵀ   D₂  -eᵀ  -D₁  ]
```

The two are then assembled through the paper's Main Theorem with U the array
over {I, 0, D₁, D₂} and V the array over {R, S, I, I}. Ingredient (II) is
where the claim fails.

**Proposition 2 (what an instance forces on D₁ and D₂).** Suppose the paper's
Corollary 4 has an instance at parameter m. Then D₁ and D₂ are symmetric of
order m, have zero diagonal and ±1 entries off the diagonal, have all row
sums 0, commute, and satisfy

> D₁² + D₂² = 2m·I − 2·J.

*Proof.* Symmetry is part of the displayed form. For the rest, index the
displayed rows by their blocks and read D Dᵀ = 2m·I and the Main Theorem's
hypothesis (4.1).

*Row sums.* Row i of the second block is [1 | D₁[i] | 1 | D₂[i]]. Its inner
products with the two single rows [0 | e | 0 | e] and [0 | e | 0 | −e] are
e(D₁[i]) + e(D₂[i]) and e(D₁[i]) − e(D₂[i]), both 0, so every row sum of D₁
and of D₂ is 0.

*Zero diagonal, ±1 off it.* Hypothesis (4.1) requires U_ij ± V_ij to have all
entries in {±1}, blockwise. In this assembly D₁ and D₂ are each paired against
I, so D₁ ± I and D₂ ± I have entries in {±1}. With entries of D₁, D₂ in
{0, ±1} that forces the diagonal to be 0 and every off-diagonal entry to
be ±1. (The same condition pairs I against R and forces R zero-diagonal, which
is what Goethals–Seidel supplies.)

*The identity and the commutation.* The norm of row i of the second block is
1 + |D₁[i]|² + 1 + |D₂[i]|² = 2m, and for i ≠ j the inner product of rows i
and j is 1 + ⟨D₁[i], D₁[j]⟩ + 1 + ⟨D₂[i], D₂[j]⟩ = 0. Hence
D₁D₁ᵀ + D₂D₂ᵀ has diagonal 2m − 2 and off-diagonal −2, that is
D₁D₁ᵀ + D₂D₂ᵀ = 2m·I − 2J. Pairing row i of the second block against row j of
the fourth block, [1 | D₂[j] | −1 | −D₁[j]], gives
⟨D₁[i], D₂[j]⟩ = ⟨D₂[i], D₁[j]⟩, that is D₁D₂ᵀ = D₂D₁ᵀ. Symmetry turns the two
displayed statements into D₁² + D₂² = 2m·I − 2J and D₁D₂ = D₂D₁. ∎
Label: PROVED-BY-DERIVATION.

At m = 51 the target is D₁² + D₂² = 102·I − 2·J. Only the first three
conclusions are used below; the quadratic identity is recorded because it is
what a search for the object would have to satisfy.

### 2.5 The obstruction

**Proposition 3 (handshake).** Let m be odd and let D be a symmetric matrix of
order m with zero diagonal, entries ±1 off the diagonal, and every row sum 0.
Then m ≡ 1 (mod 4).

*Proof.* Each row has m − 1 entries off the diagonal, summing to 0, so exactly
(m − 1)/2 of them equal −1. The positions of the −1 entries are the edges of a
graph on m vertices, loopless because the diagonal is 0 and undirected because
D is symmetric, in which every vertex has degree (m − 1)/2. The number of
edges is m(m − 1)/4, an integer, so 4 divides m(m − 1); m is odd, hence
4 divides m − 1. ∎
Label: PROVED-BY-DERIVATION.

**Proposition 4.** The paper's Corollary 4 has no instance at m = 51.
Consequently it does not produce a Williamson-type quadruple of order 103, and
the list-(2) entry at 103 and the list-(3) entry at 515 are not supported by
it.

*Proof.* By Proposition 2 an instance at m = 51 would supply a symmetric
matrix of order 51 with zero diagonal, ±1 entries off the diagonal and every
row sum 0. Since 51 ≡ 3 (mod 4), Proposition 3 forbids such a matrix.
Ingredient (I) is not at issue. ∎
Label: PROVED-BY-DERIVATION.

The same test decides the paper's other list-(2) entries at n ≡ 3 (mod 4).
Writing m = (n − 1)/2, the test passes exactly when n ≡ 3 (mod 8):

| n | 83 | 103 | 127 | 151 |
| --- | --- | --- | --- | --- |
| m = (n−1)/2 | 41 | 51 | 63 | 75 |
| m mod 4 | 1 | 3 | 3 | 3 |
| Corollary 4 instance possible | yes | **no** | **no** | **no** |

Any list-(3) entry drawn from 103, 127 or 151 is affected in the same way.

**Remark (the positive side).** The obstruction is narrow, not a blanket one.
When m is a prime ≡ 1 (mod 4), ingredient (II) exists, by the standard
character computation for quadratic residues. Take D₁ to be the
circulant over Z_m carrying −1 exactly on the quadratic residues, and D₂ the
circulant carrying −1 exactly on the non-residues. Both are symmetric because
−1 is a residue, both have zero diagonal and all row sums 0, they commute, and
their two periodic autocorrelation functions sum to the constant −2 off the
peak, which is the identity D₁² + D₂² = 2m·I − 2J. The block computation of
Proposition 2 run backwards then gives D Dᵀ = 2m·I for the displayed form.
Checked here by direct computation at m = 5, 13, 17, 29, 41. At m = 41 this is
the paper's engine at n = 83, which the test admits.
Label: PROVED-BY-DERIVATION.

### 2.6 The typo on p. 101

The output order printed for Corollary 4 is 4(2m + 3). The displayed
C₂-matrix has blocks of order m, and the paper's Main Theorem applied to these
ingredients returns order 4(2m + 1), so 4(2m + 3) is a typo.

The reading does not change the conclusion. Reaching n = 103 through the
printed 4(2m + 3) would need m = 50; the D-blocks would then have order 50,
each of their rows carrying 49 entries in ±1 that sum to 0, which is
impossible. Under either reading, Corollary 4 does not reach n = 103.

### 2.7 Scope of the erratum

This section shows that the printed route does not deliver its stated output
at n = 103. It does **not** show that a Williamson-type quadruple of order 103
fails to exist, and it says nothing about whether some other construction
reaches order 2060. No account is offered here of how the 1991 lists were
produced.

Order 2060 is not open: an Hadamard matrix of order 2060 was posted publicly
on 2026-08-23, credited to Schneider. That closure is unrelated to the 1991
claim, and this note certifies nothing about it. What the erratum changes is
the provenance of the table entry, not the status of the order.

### 2.8 What survives

Everything in the paper that does not form a C₂-matrix. In particular
**Miyamoto's Theorem 5 / Corollary 1 is untouched**, and section 3 uses it.
Its second ingredient is an ordinary Hadamard matrix of order q − 1, consumed
only through K Kᵀ = Kᵀ K = (q − 1)·I; it never forms a C₂-matrix, so the
parity obstruction of Proposition 3 has nothing to bite on. The hypotheses are
disjoint and so are the failure modes. Cati and Pasechnik implement Theorem 5
/ Corollary 1 and credit it at q = 853, 1093, 1669, 1789, 1913, 1933, 2053,
2269, 2341; none of that is affected by section 2.

---

## 3. The construction at q = 1949

### 3.1 The theorem

**Theorem (Miyamoto 1991, Theorem 5 / Corollary 1; restated as Đoković,
arXiv:1008.2043, Theorem 2.4).** If q ≡ 1 (mod 4) is a prime power and an
Hadamard matrix of order q − 1 exists, then an Hadamard matrix of order 4q
exists.

Write m = (q − 1)/2 and n = 2m + 1 = q. The construction as implemented here:

**(a) Conference matrix.** C is the symmetric Paley conference matrix of order
q + 1, the bordered Jacobsthal matrix, with C Cᵀ = q·I. It is symmetric
because q ≡ 1 (mod 4).

**(b) E-form.** Conjugate by the diagonal sign matrix that makes row 0 all +1
off the diagonal, then permute the remaining q − 1 indices by the sign pattern
of row 1. That pattern splits them (q − 1)/2 and (q − 1)/2, because rows 0 and
1 are orthogonal. The result is

```
      E = [  0    1    e     e   ]
          [  1    0    e    -e   ]
          [ eᵀ   eᵀ  -C1    C2   ]        blocks of order m
          [ eᵀ  -eᵀ   C2ᵀ   C4   ]
```

with e(C1) = 1, e(C2) = 0, e(C4) = 1 in rows and, by symmetry, in columns, and

> C1 C1ᵀ + C2 C2ᵀ = q·I − 2J,  C2ᵀ C2 + C4 C4ᵀ = q·I − 2J,  C1 C2 = C2 C4ᵀ.

These are read off E Eᵀ = q·I blockwise. The certificate re-derives and
re-checks all of them on the actual matrices at the q being run.

**(c) The given Hadamard matrix.** Split the given H(q − 1) = K of order 2m as
K = [[K1, K2], [−K3, K4]] with blocks of order m. The paper's identities
(5.3a)–(5.3f) are then free: they are literally the six block identities of
K Kᵀ = Kᵀ K = 2m·I, namely K1K1ᵀ + K2K2ᵀ = 2m·I, K3K3ᵀ + K4K4ᵀ = 2m·I,
K1ᵀK1 + K3ᵀK3 = 2m·I, K2ᵀK2 + K4ᵀK4 = 2m·I, K1K3ᵀ = K2K4ᵀ, K1ᵀK2 = K3ᵀK4.
**"H(q − 1) exists" is the whole hypothesis; no further structure on it is
used.** This is why the theorem accepts an announced matrix as input without
knowing anything about how that matrix was made.

**(d) The arrays.** In displayed (signed) form,

```
      U = [ C1   C2    0    0  ]      V = [  I     0    K1   K2  ]
          [-C2ᵀ  C4    0    0  ]          [  0     I    K3  -K4  ]
          [  0    0   C1   C2  ]          [-K1ᵀ  -K3ᵀ    I    0  ]
          [  0    0  -C2ᵀ  C4  ]          [-K2ᵀ   K4ᵀ    0    I  ]
```

the raw blocks being U_ij = Σ_ij·(displayed) for the sign matrix
Σ = [[+,+,+,+], [−,+,+,−], [−,−,+,+], [−,+,−,+]]. The Main Theorem's four
hypotheses on the pair U, V then follow from (b) and (c): (4.1) U_ij ± V_ij
has all entries in {±1}, which holds because C1 and C4 are zero-diagonal and
every other pairing is X ± 0; (4.2) e(U_ii) = 1 and e(U_ij) = 0 for i ≠ j,
which is the row-sum statement of (b); (4.9) U Uᵀ = n·I − 2(I₄ ⊗ J_m), which
is the block identity of (b) applied twice; and (4.10) V Vᵀ = n·I, which is
(c) together with four cancellations between I and K blocks. All four are
re-checked numerically at the q being run.

**(e) Assembly.** With P = [[1,1],[1,1]], Q = [[1,−1],[−1,1]], set
T_ij = U_ij ⊗ P + V_ij ⊗ Q of order 2m, then X_ii = [[1, s·e], [s·eᵀ, T_ii]]
and X_ij = [[1, −s·e], [−s·eᵀ, T_ij]] for i ≠ j, and H = M(X_ij) of order
4(2m + 1) = 4q. The derivation uses only Σ_k s_ik = 2s, so **both border signs
work**; s = −1 is the paper's printed border and is the one used at q = 1949.

### 3.2 The input H(1948), and its source

The input is one of the twelve matrices in the announcement of 2026-08-12
credited to Alpöge's group. The citation a reader needs is the announcement and
its payload, not this repository:

- **Announcement:** `x.com/__alpoge__/status/2087504785952182273`, 2026-08-12.
  Payload retrieved 2026-08-28.
- **Payload digest:** the announcement tape is 23,828 characters,
  `sha256 = 5b5fe8fa42f0d6a8b4e4c9926726d82a6aab8e1070c1ae4d1b430c1277e58db4`.
  The 1948 characters at zero-based offsets 19916 through 21863 are four ±1
  sequences of length 487. They are banked in `data/` and are what is used
  here.
- **The construction they encode:** the four sequences are the first rows of
  circulants A, B, C, D of order 487, placed in the plain unbordered
  Goethals–Seidel array shown below.

```
      [  A    BR    CR    DR  ]
      [ -BR    A   DᵀR  -CᵀR  ]        R the back-diagonal reflection
      [ -CR  -DᵀR    A   BᵀR  ]        on Z₄₈₇, R² = I
      [ -DR   CᵀR  -BᵀR    A  ]
```

That array is an Hadamard matrix of order 4·487 = 1948 exactly when the four
periodic autocorrelation functions of the sequences sum to 1948·δ₀.

**Rebuilt, not adopted.** `certs/01-h7796/run.py` rebuilds H(1948) from those
seeds with this repository's own builder and requires

```
VERDICT: HADAMARD order=1948 all 1896378 row pairs orthogonal
canonical_sha256=fddc841ebf951f6e17e939551d058ea5df046251ea065b5f6e7ee2fd8d0f62ce
```

before the matrix is consumed. No flattering input: an input that fails the
trust chain stops the run.

A public mirror of the announcement (`github.com/foocker/Hadamard668`, created
2026-08-13) carries a copy of the tape whose digest matches the one above. Its
decoder was never executed here and its output was treated as data only. Its
decoded copy of the order-1948 matrix is **truncated**, so no equality is
asserted against that file; the equality asserted here is against the tape
digest and the pinned rebuild digest above.

### 3.3 The composite

q = 1949 is prime and 1949 = 4·487 + 1, so q ≡ 1 (mod 4); m = (q − 1)/2 = 974;
n = 2m + 1 = 1949; the output order is 4q = 7796. The construction is
deterministic: no search, no random choice, nothing to tune.

The result:

```
VERDICT: HADAMARD order=7796 all 30384910 row pairs orthogonal
canonical_sha256=151d33f6d404d2bb3ca4aa562aa3fb20b49a6a8ae1c5b91fee0d14800b6b0a75
```

Label: PROVEN-BY-CERTIFICATE. The canonical serialization is 60,785,412 bytes.
It is not committed; it regenerates deterministically from committed inputs,
and the digest is what binds it.

**Corollary (doubling).** H(2) ⊗ H(7796) is an Hadamard matrix of order
15592 = 2·7796. **Stated, not built here.**

### 3.4 Status of the order

Order 7796 is listed unresolved in Cati–Pasechnik Table 4 v2 (2025-08-30),
machine-diffed; re-checked at release date. Precisely: the source is Cati and
Pasechnik, *A database of constructions of Hadamard matrices*,
arXiv:2411.18897**v2** (2025-08-30), Table 4, which lists pairs n(m) with m
minimal such that a Hadamard matrix of order 2ᵐ·n is known, for n ≤ 2999, and
omits the case m = 2 because those orders are known. The table was pulled from
the arXiv LaTeX e-print, transcribed and machine-diffed 195/195 against the
source; the transcribed entry is in `data/` and `run.py` re-reads it. It reads
`1949(4)`: the smallest recorded power is 2⁴·1949 = 31184, so neither
4·1949 = 7796 nor 8·1949 = 15592 appears there.
Label: REPORTED-FROM-AUDITED-TABLE (arXiv:2411.18897v2, 2025-08-30; read
2026-08-29).

The claim wording this laboratory uses, and does not strengthen:

> The Cati–Pasechnik database (arXiv:2411.18897v2, 2025-08-30) records no
> Hadamard matrix of order 2²·1949; on that basis this is the first publicly
> accessible and independently reproducible construction of order 7796 located
> in our audit (audit closed 2026-08-29; re-checked at release date). A
> database records what its authors knew, not what exists.

Two limits on that sentence, both binding. A database is a record of what its
authors knew in 2025-08, not a non-existence proof; someone may hold an
unpublished construction. And the closure here is mechanical: the same two
public inputs — the 2026-08-12 announcement and Miyamoto's theorem, already
implemented by Cati and Pasechnik — were available to anyone from 2026-08-12
onwards, so an independent closure elsewhere in that window is plausible and
would not be visible from here.

---

## 4. Verification

### 4.1 The trust chain

`verify/verify.py` is the only thing in this repository that decides whether a
matrix is Hadamard. It parses a matrix file, checks that it is square with
entries in {+1, −1}, and checks H Hᵀ = n·I exactly: rows are packed into
Python integers and a pair of ±1 rows is orthogonal precisely when the
population count of their XOR is n/2. No floating point anywhere. It prints
the order, the number of row pairs checked, and the canonical SHA-256 of the
`'+'`/`'-'` serialization, and exits 0 only on success.

```
python verify/verify.py --selftest
```

The selftest proves the verifier on knowns and known-bads: Sylvester matrices
of orders 1 to 256 pass; row negation, row swap and column negation still
pass, so the verifier is not over-strict; a single flipped entry, a duplicated
row, an all-ones matrix and an order-6 candidate are rejected; four malformed
inputs are rejected at parse. Standard library only, bare `python3` ≥ 3.9.

### 4.2 What the certificate re-establishes

`certs/01-h7796/` holds `run.py` and a short `NOTES.md`. `run.py` is standard
library only and imports nothing from elsewhere in the repository; it
reimplements the whole construction, and every hypothesis check, in the trust
chain's own language, so the chain from the public seeds to the 7796 × 7796
artifact runs on bare `python3`. Four stages:

- **A — the input.** Rebuilds H(1948) from the banked seeds through the
  Goethals–Seidel array of §3.2 and requires the pinned verdict and digest
  **before** the matrix is used.
- **B — the grounding gate.** Runs the *same* code path at q = 5 and q = 257
  from Sylvester inputs H(4) and H(256), producing H(20) and H(1028) at pinned
  digests. This is the part that makes the main run credible: the engine is
  exercised at a size where the answer is independently known. The gate also
  carries a **negative control** — one entry of a built matrix is flipped and
  `verify.py` must reject it, exit 1. The checks are not vacuous.
- **C — the main run.** At q = 1949: C Cᵀ = q·I at order 1950; the E-form
  entry for entry; C1 and C4 symmetric with zero diagonal and C2 full ±1;
  e(C1) = 1, e(C2) = 0, e(C4) = 1 in rows and columns; the three block
  identities of §3.1(b); K Kᵀ = 1948·I and all six identities of §3.1(c);
  then (4.1), (4.2), (4.9) at order 3896 and (4.10) at order 3896 — then
  assemble, write, hand to `verify.py`, pin the digest.
- **D — the table reading.** Re-reads the transcribed Cati–Pasechnik Table 4
  entry from `data/` and prints the openness reading together with its label.

Generated matrices are written outside version control and are never
committed. The digests below are what binds them.

### 4.3 Replay

```
python verify/verify.py --selftest
python certs/01-h7796/run.py
```

Both run from the repository root on bare `python3` ≥ 3.9, with no third-party
package. The full certificate is on the order of a minute of single-core
work, most of it `verify.py` on the 7796 artifact; peak disk is about 65 MB of
generated matrices. `certs/01-h7796/NOTES.md` prints the expected verdict
lines.

### 4.4 Digests

| object | order | row pairs | canonical SHA-256 |
| --- | --- | --- | --- |
| gate, q = 5 from Sylvester H(4) | 20 | 190 | `18efd3fec26689d5721f1058a6520facae1a0b5122f939bad7a8165d701233bc` |
| gate, q = 257 from Sylvester H(256) | 1028 | 527,878 | `7e95741ba1409081bb4abe2981c72f549f537ccb6a5335ea83fce63b7eabc134` |
| input, rebuilt from the announced seeds | 1948 | 1,896,378 | `fddc841ebf951f6e17e939551d058ea5df046251ea065b5f6e7ee2fd8d0f62ce` |
| **output, q = 1949** | **7796** | **30,384,910** | `151d33f6d404d2bb3ca4aa562aa3fb20b49a6a8ae1c5b91fee0d14800b6b0a75` |

The digest is of the canonical `'+'`/`'-'` serialization, one row per line,
newline-terminated, as printed by `verify.py`.

### 4.5 Remarks on the artifact

The chain contains no random number generator, and three separate runs
produced the identical canonical digest. Two assemblers were written
independently for this construction, one using an array library and one
standard library only; they agree on the 60.8 MB artifact digest exactly. The
one in this repository is the standard-library one. Neither assembler is in
the trust chain — `verify.py` is. The output was additionally cross-checked
once by a separate reader computing exact Gram entries for 300 randomly chosen
rows against all 7796, with every off-diagonal entry 0.

This is one order, not several. That two assemblers built it is a remark about
confidence, not a second result.

### 4.6 What is claimed, and what is not

Claimed: the existence of H(7796), its reproducibility from this repository,
and the correctness of the substitution into Miyamoto's Theorem 5 /
Corollary 1 (PROVEN-BY-CERTIFICATE); the emptiness of the paper's Corollary 4
at m = 51 and its consequence for the printed 515 entry
(PROVED-BY-DERIVATION); a dated reading of one table entry
(REPORTED-FROM-AUDITED-TABLE).

Not claimed: that no Williamson-type quadruple of order 103 exists; that order
7796 is open today rather than on 2025-08-30; that H(15592) was built; that
the erratum bears on the existence of an Hadamard matrix of order 2060, which
was closed independently and by other means; that no other party holds an
Hadamard matrix of order 7796.

---

## 5. Credits and citations

The theorem in section 3 is Miyamoto's. The input matrix is Alpöge's group's.
The verification, the erratum and the certificate are this laboratory's.

- M. Miyamoto, *A construction of Hadamard matrices*, J. Combin. Theory Ser. A
  **57** (1991) 86–108. The subject of section 2; the source of Theorem 5 /
  Corollary 1 used in section 3.
- D. Ž. Đoković, *Small orders of Hadamard matrices and base sequences*,
  arXiv:1008.2043 (2010), Theorem 2.4. The modern statement of the theorem
  used here.
- The announcement of twelve Hadamard matrices, 2026-08-12, credited to
  Alpöge's group: `x.com/__alpoge__/status/2087504785952182273`. The source of
  the H(1948) input; payload digest in §3.2.
- M. Cati and D. V. Pasechnik, *A database of constructions of Hadamard
  matrices*, arXiv:2411.18897v2 (2025-08-30). The audited table, Table 4; the
  source of the "unable to verify" flag on the 4·515 entry; and the
  implementation that already carries Miyamoto's Theorem 5 / Corollary 1.
- J. Williamson, for the array of four amicable blocks that defines the
  M-partition of §2.2 and the Williamson-type quadruple.
- J. M. Goethals and J. J. Seidel, for the conference-matrix construction used
  as ingredient (I) of the paper's Corollary 4 and for the Goethals–Seidel
  array in which the H(1948) input is assembled.
- L. D. Baumert and M. Hall, Jr. (1965), for the Baumert–Hall array of order 5
  that carries the paper's list-(3) step.
- J. J. Sylvester, for the H(4) and H(256) inputs to the grounding gate and
  for the doubling corollary.
- The Hadamard matrix of order 2060 posted publicly on 2026-08-23 is credited
  to Schneider; it is referred to in §2.7 only, and nothing here certifies it.

Licensing and the AI-station disclosure are in the repository root:
`LICENSE`, `CITATION.cff`, `DISCLOSURE.md`.
