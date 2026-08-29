# Disclosure

AI-generated results with a human managing the workflow. Produced by Claude
Code (Fable 5, Anthropic); external reviews by GPT 5.6 (OpenAI) and by
Grok (xAI), intaken and adjudicated.

## What the AI stations did

Everything mathematical. The reading of the 1991 paper; the re-derivation of
its main theorem rather than its quotation; the parity obstruction that isolates
where the order-515 entry fails, and the check that the obstruction does not
touch the main theorem; the decode of the announced order-1948 matrix and the
assembler that rebuilds it; the construction and verification of the order-7796
matrix; the verifier and the certificate. Outside stations reviewed the claims
and the hedging; their reports were relayed in and adjudicated
here against primary sources; where a report and a source disagreed, the source
governed.

## What the human owner did

Granted the sessions, paid for the compute, obtained the scan of the 1991 paper
that this laboratory could not otherwise read, relayed material to and from the
outside reviewers, and ruled on publication, licensing, and scope. No
mathematical contribution, and none is claimed. The owner's name appears here
and in the copyright line; it appears in no derivation.

## Verification

The two results are checked in different ways, and both are open to a reader.

The erratum is a proof. It is the obstruction and its consequence as stated in
the README, in full in the note (Propositions 2–4), and it is verified by
reading them against the paper. No computation is involved and none would
settle it.

The construction is a certificate. The trust chain is `verify/verify.py`, which
accepts a matrix only if the matrix is square, has every entry in {+1, −1}, and
satisfies H·Hᵀ = n·I. The arithmetic is exact: rows are packed into integers and
orthogonality of a pair is a popcount identity, so no floating point enters
anywhere. `python verify/verify.py --selftest` exercises it against known
Hadamard matrices, against Hadamard-preserving row and column operations, and
against corruptions it must reject. `certs/01-h7796/run.py` then rebuilds the
order-1948 input from the banked seeds and requires the trust chain to accept it
at a pinned digest before it is consumed, re-checks the theorem's hypotheses on
the actual matrices, builds the order-7796 output, and requires the trust chain
to accept that at a pinned digest too. Nothing outside the standard library is
used, and nothing requires the network.

Independent verification is invited. Questions and verification reports are
welcome via GitHub issues.

## Credit for external mathematics

- **Miyamoto**, *A construction of Hadamard matrices*, JCTA 57 (1991) 86–108 —
  the theorem this repository builds with, and the paper the erratum concerns.
  The erratum is confined to the Corollary 4 chain and the section 7 lists that
  depend on it. The main theorem is sound and is used here as such.
- **Đoković**, arXiv:1008.2043 — the modern statement of that main theorem, in
  the form used here, together with the record of which database entries were
  unverified.
- **Alpöge's group** — the announcement of 2026-08-12 carrying the order-1948
  matrix used as input. The seeds are read from the announcement tape, cited by
  URL and SHA-256 in the README and the certificate.
- **Goethals and Seidel; Paley; Williamson; Baumert and Hall** — the classical
  arrays the construction and the erratum both refer to.
- **Cati and Pasechnik**, *A database of constructions of Hadamard matrices*,
  arXiv:2411.18897v2 (2025-08-30) — the status table against which order 7796
  is reported, and the source of the recorded doubt about order 4·515. A
  database records what its authors knew, not what exists.
