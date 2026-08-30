#!/usr/bin/env python3
"""Certificate 01 -- H(7796) = H(4 * 1949) by Miyamoto's 1991 theorem.

See NOTES.md.  Exit 0 iff every gate is green.  Standard library only, exact
integer arithmetic throughout, no floats.  The only accepted verdict on a
matrix is a green subprocess run of verify/verify.py.

THE THEOREM

  Miyamoto, "A construction of Hadamard matrices", JCTA 57 (1991) 86-108,
  Theorem 5 / Corollary 1.  The same statement is Theorem 2.4 of Djokovic,
  arXiv:1008.2043, in the form used here:

      If q = 1 (mod 4) is a prime power and an Hadamard matrix of order
      q - 1 exists, then an Hadamard matrix of order 4q exists.

  The substitution made here is q = 1949 = 4 * 487 + 1 with the announced
  H(1948) as the second ingredient, giving order 4 * 1949 = 7796.

WHAT THIS FILE ESTABLISHES, IN ORDER

  Stage 1, the grounding gate.  The same code path that will run at
  q = 1949 is run at q = 5 from the Sylvester H(4) and at q = 257 from the
  Sylvester H(256).  Both outputs, H(20) and H(1028), must be verify.py
  green at their pinned canonical digests.  At q = 5 the packed-integer dot
  product is calibrated against a naive O(n^3) triple loop, and the output
  is re-checked by an independent packed-integer popcount path.

  Stage 2, the input.  H(1948) is rebuilt from data/h1948-seeds.json
  through the plain Goethals-Seidel array over Z_487 (s = 0, r_shift = 486,
  standard block pattern), and must be verify.py green at its pinned
  canonical digest before it is consumed.

  Stage 3, the target.  q = 1949.  Every hypothesis of the theorem is
  re-checked by exact integer arithmetic at q = 1949 itself: the conference
  matrix, the E-form entry for entry, e(C1) = 1, e(C2) = 0, e(C4) = 1 in
  rows and columns, the three E-block identities, the six K-block
  identities, (4.1), (4.2), (4.9) at order 3896 and (4.10) at order 3896.
  The matrix is then assembled, written, and handed to verify.py.

  Stage 4, the negative control.  One entry of the verified H(20) is
  flipped.  verify.py must reject the result with exit 1.

  Stage 5, the openness reading, printed with its label.  This certificate
  proves existence.  It does not prove openness.

THE CONSTRUCTION (m = (q-1)/2, n = 2m+1 = q)

  E = [[0, 1, e, e], [1, 0, e, -e], [e^t, e^t, -C1, C2], [e^t, -e^t, C2^t, C4]]
  K = the given H(q-1) split as [[K1, K2], [-K3, K4]]
  U = [[C1, C2, 0, 0], [-C2^t, C4, 0, 0], [0, 0, C1, C2], [0, 0, -C2^t, C4]]
  V = [[I, 0, K1, K2], [0, I, K3, -K4], [-K1^t, -K3^t, I, 0], [-K2^t, K4^t, 0, I]]
  T_ij = U_ij (x) [[1,1],[1,1]] + V_ij (x) [[1,-1],[-1,1]]
  X_ii = [[1, s e], [s e^t, T_ii]],  X_ij = [[1, -s e], [-s e^t, T_ij]]
  H    = (SIGMA_ij X_ij),  SIGMA = [[+,+,+,+],[-,+,+,-],[-,-,+,+],[-,+,-,+]]

  s = -1 is Miyamoto's printed border and is the variant used for every
  digest pinned here.  s = +1 is the mirror and is equally Hadamard; the
  derivation uses only SIGMA_k s_ik = 2s.  Because SIGMA_ij^2 = 1, the
  interior of superblock (i,j) of H is exactly T_ij built from the
  displayed U, V above, which is how this file assembles it: two bytearray
  slice assignments per superblock per row.

USAGE (from the repository root)

    python certs/01-h7796/run.py              # full certificate
    python certs/01-h7796/run.py --gate-only  # stages 1, 2, 4, 5

Generated matrices are written to out/ and deleted after verification.
They are never committed.  They are a deterministic rebuild from the files
in this repository; the pinned digests are what binds them.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True

DATA = os.path.join("data", "h1948-seeds.json")
TABLE4 = os.path.join("data", "cp-table4-v2.json")
VERIFY = os.path.join("verify", "verify.py")
OUTDIR = "out"

H1948_SHA = "fddc841ebf951f6e17e939551d058ea5df046251ea065b5f6e7ee2fd8d0f62ce"
H7796_SHA = "151d33f6d404d2bb3ca4aa562aa3fb20b49a6a8ae1c5b91fee0d14800b6b0a75"

# q -> canonical sha256 of the order-4q gate output
GATE_SHA = {
    5: "18efd3fec26689d5721f1058a6520facae1a0b5122f939bad7a8165d701233bc",
    257: "7e95741ba1409081bb4abe2981c72f549f537ccb6a5335ea83fce63b7eabc134",
}

SIGMA = ((1, 1, 1, 1), (-1, 1, 1, -1), (-1, -1, 1, 1), (-1, 1, -1, 1))

PLUS, MINUS = 43, 45                       # ord('+'), ord('-')
TO01 = bytes.maketrans(b"+-", b"10")
NEG = bytes.maketrans(b"+-", b"-+")

FAIL = []
_T0 = time.time()

if hasattr(int, "bit_count"):              # 3.10+
    def _popcount(x):
        return x.bit_count()
else:                                      # 3.9 fallback
    def _popcount(x):
        return bin(x).count("1")


def log(msg):
    print("[%6.1fs] %s" % (time.time() - _T0, msg), flush=True)


def check(label, cond, extra=""):
    ok = bool(cond)
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  -- " + extra) if extra else ""), flush=True)
    if not ok:
        FAIL.append(label)
    return ok


# --------------------------------------------------------------- utilities

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def read_pm(path):
    """Read a '+/-' matrix file into a list of bytes rows."""
    rows = []
    with open(path, "r", encoding="ascii") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            rows.append(s.encode("ascii"))
    return rows


def canonical_sha(rows):
    """sha256 of the canonical serialisation: one '+/-' row per line."""
    h = hashlib.sha256()
    for r in rows:
        h.update(r)
        h.update(b"\n")
    return h.hexdigest()


def emit(path, header, rowgen, order):
    """Stream rows to disk, returning the canonical sha of the body."""
    h = hashlib.sha256()
    nrows = 0
    with open(path, "wb") as fh:
        if header:
            fh.write(header)
        for row in rowgen:
            if len(row) != order:
                raise AssertionError("row %d has width %d, expected %d"
                                     % (nrows, len(row), order))
            fh.write(row)
            fh.write(b"\n")
            h.update(row)
            h.update(b"\n")
            nrows += 1
    if nrows != order:
        raise AssertionError("wrote %d rows, expected %d" % (nrows, order))
    return h.hexdigest()


def run_verify(path):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, VERIFY, path],
                       capture_output=True, text=True, env=env)
    line = ((r.stdout or r.stderr).strip().splitlines() or [""])[-1]
    print("  verify.py %-22s -> exit %d :: %s"
          % (os.path.basename(path), r.returncode, line[:96]), flush=True)
    return r.returncode, line


# ------------------------------------------------- exact bitset arithmetic
# A row of a {0, +-1} matrix of width L is packed into two non-negative
# integers:
#   mask  bit (L-1-j) set  <=>  entry j is nonzero
#   pos   bit (L-1-j) set  <=>  entry j is +1  (bits off the mask are never
#                               read)
# For two rows u, v:  both = mu & mv, same = both & ~(pu ^ pv), and
#   u . v = (#same) - (#both - #same) = 2*popcount(same) - popcount(both),
# an exact integer identity.  It is calibrated below against a naive O(n^3)
# triple loop at q = 5.

def dot(mu, pu, mv, pv):
    both = mu & mv
    return 2 * _popcount(both & ~(pu ^ pv)) - _popcount(both)


def pack_full(byte_rows):
    """Full +-1 rows given as bytes -> list of pos ints (mask = all ones)."""
    return [int(r.translate(TO01), 2) for r in byte_rows]


def gram_ok(masks, poss, target):
    """(M M^t)[i][j] == target(i, j) for all i, j.  M M^t is symmetric, so
    only i <= j is formed."""
    nrow = len(masks)
    for i in range(nrow):
        mi, pi = masks[i], poss[i]
        for j in range(i, nrow):
            if dot(mi, pi, masks[j], poss[j]) != target(i, j):
                return False, (i, j)
    return True, None


def naive_prod(A, B_rows):
    """A * B^t by a plain triple loop over int matrices (calibration only)."""
    return [[sum(A[i][k] * B_rows[j][k] for k in range(len(A[i])))
             for j in range(len(B_rows))] for i in range(len(A))]


def hadamard_by_popcount(rows):
    """Independent exact recheck of a +-1 matrix; small orders only."""
    n = len(rows)
    packed = [int(r.translate(TO01), 2) for r in rows]
    half = n // 2
    for i in range(n):
        for j in range(i + 1, n):
            if _popcount(packed[i] ^ packed[j]) != half:
                return False
    return True


# ------------------------------------------------- the H(1948) input build

def goethals_seidel_cyclic(seeds, rho):
    """Plain Goethals-Seidel array over Z_m from four +-1 seeds.

    A, B, C, D are the type-1 group-developed matrices X[g][h] = x(h - g),
    R is the permutation h -> rho - h, and the standard block pattern is

        [  A    BR    CR    DR  ]
        [ -BR    A   D^tR -C^tR ]
        [ -CR -D^tR    A   B^tR ]
        [ -DR  C^tR -B^tR    A  ]

    with (X R)[g][h] = x(rho - g - h) and (X^t R)[g][h] = x(g + h - rho).
    rho = -1 is the classical back-diagonal R for cyclic G.  Returns the
    4m rows of the order-4m matrix as bytes.
    """
    m = len(seeds[0])
    if any(len(s) != m for s in seeds):
        raise ValueError("the four seeds must have equal length")
    x = [bytes(PLUS if v == 1 else MINUS for v in s) for s in seeds]
    xx = [b + b for b in x]                       # x(k) at index k mod m
    yy = [b[::-1] + b[::-1] for b in x]           # x(-1-k) at index k mod m

    # (superblock I, superblock J) -> (sign, seed index, mode)
    pattern = {
        (0, 0): (1, 0, "diff"), (1, 1): (1, 0, "diff"),
        (2, 2): (1, 0, "diff"), (3, 3): (1, 0, "diff"),
        (0, 1): (1, 1, "rmix"), (0, 2): (1, 2, "rmix"),
        (0, 3): (1, 3, "rmix"),
        (1, 0): (-1, 1, "rmix"), (2, 0): (-1, 2, "rmix"),
        (3, 0): (-1, 3, "rmix"),
        (1, 2): (1, 3, "tmix"), (1, 3): (-1, 2, "tmix"),
        (2, 1): (-1, 3, "tmix"), (2, 3): (1, 1, "tmix"),
        (3, 1): (1, 2, "tmix"), (3, 2): (-1, 1, "tmix"),
    }
    rows = []
    for blk in range(4):
        for g in range(m):
            parts = []
            for j in range(4):
                sign, sd, mode = pattern[(blk, j)]
                if mode == "diff":                # x(h - g)
                    off = (-g) % m
                    seg = xx[sd][off:off + m]
                elif mode == "rmix":              # x(rho - g - h)
                    c = (rho - g) % m
                    off = (m - 1 - c) % m
                    seg = yy[sd][off:off + m]
                else:                             # x(g + h - rho)
                    off = (g - rho) % m
                    seg = xx[sd][off:off + m]
                parts.append(seg if sign == 1 else seg.translate(NEG))
            rows.append(b"".join(parts))
    return rows


# ------------------------------------------------------ Paley, E-form, K

def legendre_chi(q):
    res = set((i * i) % q for i in range(1, q))
    chi = [0] * q
    for i in range(1, q):
        chi[i] = 1 if i in res else -1
    assert sum(chi) == 0
    return chi


def paley_conference(q):
    """Symmetric conference matrix C of order q+1, C C^t = q I (q = 1 mod 4)."""
    chi = legendre_chi(q)
    cd = chi + chi
    C = [[0] + [1] * q]
    for i in range(q):
        row = cd[i + 1:i + q + 1]          # row[j] = chi[(i-j) mod q]
        row.reverse()
        C.append([1] + row)
    return C


def eform(q):
    """C -> (C1, C2, C4) of order m, with every hypothesis checked."""
    n, m = q + 1, (q - 1) // 2
    C = paley_conference(q)

    check("q=%d: C symmetric, zero diagonal, +-1 off-diagonal" % q,
          all(C[i][i] == 0 for i in range(n))
          and all(C[i][j] == C[j][i] for i in range(n) for j in range(i))
          and all(abs(C[i][j]) == 1 for i in range(n)
                  for j in range(n) if i != j))
    masks = [(1 << n) - 1 - (1 << (n - 1 - i)) for i in range(n)]
    poss = [int("".join("1" if v == 1 else "0" for v in r), 2) for r in C]
    ok, where = gram_ok(masks, poss, lambda i, j: q if i == j else 0)
    check("q=%d: C C^t = %d I_%d" % (q, q, n), ok, "" if ok else str(where))

    a, b = 0, 1
    d = [1] * n
    for j in range(n):
        if j != a:
            d[j] = C[a][j]
    Cn = [[d[i] * C[i][j] * d[j] for j in range(n)] for i in range(n)]
    check("q=%d: normalised row a is all +1 off the diagonal" % q,
          all(Cn[a][j] == 1 for j in range(n) if j != a))
    check("q=%d: normalisation preserved symmetry and the zero diagonal" % q,
          all(Cn[i][i] == 0 for i in range(n))
          and all(Cn[i][j] == Cn[j][i] for i in range(n) for j in range(i)))
    check("q=%d: C[a][b] = +1" % q, Cn[a][b] == 1)

    rest = [j for j in range(n) if j not in (a, b)]
    s1 = [j for j in rest if Cn[b][j] == 1]
    s2 = [j for j in rest if Cn[b][j] == -1]
    check("q=%d: row b splits the rest %d/%d" % (q, m, m),
          len(s1) == m and len(s2) == m,
          "|S1|=%d |S2|=%d" % (len(s1), len(s2)))
    order = [a, b] + s1 + s2
    E = [[Cn[r][c] for c in order] for r in order]

    C1 = [[-E[2 + i][2 + j] for j in range(m)] for i in range(m)]
    C2 = [[E[2 + i][2 + m + j] for j in range(m)] for i in range(m)]
    C4 = [[E[2 + m + i][2 + m + j] for j in range(m)] for i in range(m)]
    shape = (E[0] == [0, 1] + [1] * m + [1] * m
             and E[1] == [1, 0] + [1] * m + [-1] * m
             and all(E[2 + i][0] == 1 and E[2 + i][1] == 1 for i in range(m))
             and all(E[2 + m + i][0] == 1 and E[2 + m + i][1] == -1
                     for i in range(m))
             and all(E[2 + m + i][2 + j] == C2[j][i]
                     for i in range(m) for j in range(m)))
    check("q=%d: E is exactly [[0,1,e,e],[1,0,e,-e],[e^t,e^t,-C1,C2],"
          "[e^t,-e^t,C2^t,C4]]" % q, shape)

    check("q=%d: C1, C4 symmetric zero-diagonal +-1; C2 full +-1" % q,
          all(C1[i][i] == 0 and C4[i][i] == 0 for i in range(m))
          and all(C1[i][j] == C1[j][i] and C4[i][j] == C4[j][i]
                  for i in range(m) for j in range(i))
          and all(abs(C1[i][j]) == 1 and abs(C4[i][j]) == 1
                  for i in range(m) for j in range(m) if i != j)
          and all(abs(v) == 1 for r in C2 for v in r))
    colsum = lambda M: [sum(M[i][j] for i in range(len(M)))
                        for j in range(len(M[0]))]
    check("q=%d: e(C1)=1, e(C2)=0, e(C4)=1 (rows AND columns)" % q,
          all(sum(r) == 1 for r in C1) and all(v == 1 for v in colsum(C1))
          and all(sum(r) == 0 for r in C2) and all(v == 0 for v in colsum(C2))
          and all(sum(r) == 1 for r in C4) and all(v == 1 for v in colsum(C4)))
    return C1, C2, C4


def eblock_identities(q, C1, C2, C4, calibrate):
    """C1C1^t + C2C2^t = qI-2J, C2^tC2 + C4C4^t = qI-2J, C1C2 = C2C4^t."""
    m = (q - 1) // 2
    full = (1 << m) - 1
    zdmask = [full - (1 << (m - 1 - i)) for i in range(m)]

    def bits(M):
        return [int("".join("1" if v == 1 else "0" for v in r), 2) for r in M]

    p1, p2, p4 = bits(C1), bits(C2), bits(C4)
    C2T = [[C2[i][j] for i in range(m)] for j in range(m)]
    p2t = bits(C2T)

    ok = True
    for i in range(m):
        for j in range(i, m):
            v = (dot(zdmask[i], p1[i], zdmask[j], p1[j])
                 + dot(full, p2[i], full, p2[j]))
            if v != ((q - 2) if i == j else -2):
                ok = False
                break
        if not ok:
            break
    check("q=%d: C1 C1^t + C2 C2^t = qI - 2J" % q, ok)

    ok = True
    for i in range(m):
        for j in range(i, m):
            v = (dot(full, p2t[i], full, p2t[j])
                 + dot(zdmask[i], p4[i], zdmask[j], p4[j]))
            if v != ((q - 2) if i == j else -2):
                ok = False
                break
        if not ok:
            break
    check("q=%d: C2^t C2 + C4 C4^t = qI - 2J" % q, ok)

    # C1 C2 = C2 C4^t.  C4 is symmetric, so C2 C4^t is formed against C4's
    # rows.
    ok = True
    for i in range(m):
        for j in range(m):
            if (dot(zdmask[i], p1[i], full, p2t[j])
                    != dot(full, p2[i], zdmask[j], p4[j])):
                ok = False
                break
        if not ok:
            break
    check("q=%d: C1 C2 = C2 C4^t" % q, ok)

    if calibrate:
        want = naive_prod(C1, C1)
        got = [[dot(zdmask[i], p1[i], zdmask[j], p1[j]) for j in range(m)]
               for i in range(m)]
        check("q=%d: CALIBRATION bitset C1 C1^t == naive O(n^3) triple loop"
              % q, want == got)


def k_blocks(q, K, calibrate):
    """H(q-1) -> K1..K4 (bytes rows), with the six block identities of
    K K^t = K^t K = 2m I re-checked exactly."""
    m = (q - 1) // 2
    twom = 2 * m
    check("q=%d: the given H(%d) is square and +-1" % (q, twom),
          len(K) == twom and all(len(r) == twom for r in K)
          and all(set(r) <= {PLUS, MINUS} for r in K))
    pk = pack_full(K)
    full2 = (1 << twom) - 1
    ok, where = gram_ok([full2] * twom, pk,
                        lambda i, j: twom if i == j else 0)
    check("q=%d: the given H(%d) H^t = %d I" % (q, twom, twom), ok,
          "" if ok else str(where))

    K1 = [K[i][:m] for i in range(m)]
    K2 = [K[i][m:] for i in range(m)]
    K3 = [K[m + i][:m].translate(NEG) for i in range(m)]   # K3 = -K[m:, :m]
    K4 = [K[m + i][m:] for i in range(m)]
    full = (1 << m) - 1
    p = {nm: pack_full(B) for nm, B in
         (("K1", K1), ("K2", K2), ("K3", K3), ("K4", K4))}
    t = {}
    for name, B in (("K1", K1), ("K2", K2), ("K3", K3), ("K4", K4)):
        t[name] = pack_full([bytes(col) for col in zip(*B)])

    def gram2(u, v, sym=True):
        for i in range(m):
            for j in (range(i, m) if sym else range(m)):
                if (dot(full, u[i], full, u[j]) + dot(full, v[i], full, v[j])
                        != (twom if i == j else 0)):
                    return False
        return True

    ok = gram2(p["K1"], p["K2"])
    ok = ok and gram2(p["K3"], p["K4"])
    ok = ok and gram2(t["K1"], t["K3"])
    ok = ok and gram2(t["K2"], t["K4"])
    for i in range(m):                      # K1 K3^t = K2 K4^t
        for j in range(m):
            if (dot(full, p["K1"][i], full, p["K3"][j])
                    != dot(full, p["K2"][i], full, p["K4"][j])):
                ok = False
                break
        if not ok:
            break
    for i in range(m):                      # K1^t K2 = K3^t K4
        for j in range(m):
            if (dot(full, t["K1"][i], full, t["K2"][j])
                    != dot(full, t["K3"][i], full, t["K4"][j])):
                ok = False
                break
        if not ok:
            break
    check("q=%d: all six K-block identities hold for the split H(%d)"
          % (q, twom), ok)

    if calibrate:
        ints = [[1 if c == PLUS else -1 for c in r] for r in K1]
        want = naive_prod(ints, ints)
        got = [[dot(full, p["K1"][i], full, p["K1"][j]) for j in range(m)]
               for i in range(m)]
        check("q=%d: CALIBRATION bitset K1 K1^t == naive O(n^3) triple loop"
              % q, want == got)
    return K1, K2, K3, K4


# --------------------------------------------- U, V and (4.1)/(4.2)/(4.9)/(4.10)

def uv_checks(q, C1, C2, C4, K1, K2, K3, K4, calibrate):
    """(4.1), (4.2), (4.9) U U^t = nI - 2(I4 (x) J_m), (4.10) V V^t = nI."""
    m = (q - 1) // 2
    n = 2 * m + 1
    full = (1 << m) - 1
    zdm = [full - (1 << (m - 1 - i)) for i in range(m)]
    ident = [1 << (m - 1 - i) for i in range(m)]

    def bits(M):
        return [int("".join("1" if v == 1 else "0" for v in r), 2) for r in M]

    C2T = [[C2[i][j] for i in range(m)] for j in range(m)]
    nC2T = [[-v for v in r] for r in C2T]
    pC1, pC2, pC4, pnC2T = bits(C1), bits(C2), bits(C4), bits(nC2T)
    ZERO = [0] * m

    # (4.1): at every position exactly one of U_ij, V_ij is nonzero and the
    # other is 0, so U_ij +- V_ij is +-1.  Stated on the masks.
    Umask = [[zdm, [full] * m, ZERO, ZERO],
             [[full] * m, zdm, ZERO, ZERO],
             [ZERO, ZERO, zdm, [full] * m],
             [ZERO, ZERO, [full] * m, zdm]]
    Vmask = [[ident, ZERO, [full] * m, [full] * m],
             [ZERO, ident, [full] * m, [full] * m],
             [[full] * m, [full] * m, ident, ZERO],
             [[full] * m, [full] * m, ZERO, ident]]
    ok41 = all((Umask[i][j][r] & Vmask[i][j][r]) == 0
               and (Umask[i][j][r] | Vmask[i][j][r]) == full
               for i in range(4) for j in range(4) for r in range(m))
    check("q=%d: (4.1) U_ij +- V_ij in {+-1}, all 16 blocks" % q, ok41)

    # (4.2): row and column sums of the raw blocks SIGMA_ij * U_ij.
    rs = lambda M: [sum(r) for r in M]
    cs = lambda M: [sum(M[i][j] for i in range(len(M)))
                    for j in range(len(M[0]))]
    Z = [[0] * m for _ in range(m)]
    Udisp = [[C1, C2, Z, Z], [nC2T, C4, Z, Z],
             [Z, Z, C1, C2], [Z, Z, nC2T, C4]]
    ok42 = True
    for i in range(4):
        for j in range(4):
            want = 1 if i == j else 0
            B = Udisp[i][j]
            s = SIGMA[i][j]
            if (set(s * v for v in rs(B)) != {want}
                    or set(s * v for v in cs(B)) != {want}):
                ok42 = False
    check("q=%d: (4.2) e(U_ii)=1, e(U_ij)=0 (rows AND columns)" % q, ok42)

    # the packed rows of the displayed U and V at order 4m
    pT = {}
    for name, B in (("K1", K1), ("K2", K2), ("K3", K3), ("K4", K4)):
        pT[name] = pack_full([bytes(col) for col in zip(*B)])
    pK = {name: pack_full(B) for name, B in
          (("K1", K1), ("K2", K2), ("K3", K3), ("K4", K4))}
    negp = lambda v: full ^ v                        # negate a full +-1 row

    Upos = [[pC1, pC2, ZERO, ZERO],
            [pnC2T, pC4, ZERO, ZERO],
            [ZERO, ZERO, pC1, pC2],
            [ZERO, ZERO, pnC2T, pC4]]
    Vpos = [[ident, ZERO, pK["K1"], pK["K2"]],
            [ZERO, ident, pK["K3"], [negp(v) for v in pK["K4"]]],
            [[negp(v) for v in pT["K1"]], [negp(v) for v in pT["K3"]],
             ident, ZERO],
            [[negp(v) for v in pT["K2"]], pT["K4"], ZERO, ident]]

    def flatten(maskblocks, posblocks):
        masks, poss = [], []
        for bi in range(4):
            for r in range(m):
                mk = ps = 0
                for bj in range(4):
                    mk = (mk << m) | maskblocks[bi][bj][r]
                    ps = (ps << m) | posblocks[bi][bj][r]
                masks.append(mk)
                poss.append(ps)
        return masks, poss

    Um, Up = flatten(Umask, Upos)
    tgt49 = lambda i, j: ((n if i == j else 0)
                          - (2 if i // m == j // m else 0))
    ok, where = gram_ok(Um, Up, tgt49)
    check("q=%d: (4.9) U U^t = %d I_%d - 2 (I4 (x) J_%d)" % (q, n, 4 * m, m),
          ok, "" if ok else str(where))
    if calibrate:
        Uint = [[0] * (4 * m) for _ in range(4 * m)]
        for bi in range(4):
            for bj in range(4):
                B = Udisp[bi][bj]
                for r in range(m):
                    for c in range(m):
                        Uint[bi * m + r][bj * m + c] = B[r][c]
        want = naive_prod(Uint, Uint)
        got = [[dot(Um[i], Up[i], Um[j], Up[j]) for j in range(4 * m)]
               for i in range(4 * m)]
        check("q=%d: CALIBRATION bitset U U^t == naive O(n^3) triple loop" % q,
              want == got)
    del Um, Up

    Vm, Vp = flatten(Vmask, Vpos)
    ok, where = gram_ok(Vm, Vp, lambda i, j: n if i == j else 0)
    check("q=%d: (4.10) V V^t = %d I_%d" % (q, n, 4 * m), ok,
          "" if ok else str(where))
    del Vm, Vp


# ------------------------------------------------------------- the assembly

def merge_blocks(C1, C2, C4, K1, K2, K3, K4):
    """M_ij = U_ij + V_ij and N_ij = U_ij - V_ij as +-1 bytes matrices.

    Exactly one of U_ij, V_ij is nonzero at each position by (4.1), so both
    merges are +-1 everywhere and T_ij's rows are interleavings of them:
        T row 2a   = M[a][0] N[a][0] M[a][1] N[a][1] ...
        T row 2a+1 = N[a][0] M[a][0] N[a][1] M[a][1] ...
    """
    m = len(C1)
    tob = lambda M: [bytes(PLUS if v == 1 else MINUS for v in r) for r in M]
    A1 = tob(C1)                       # zero diagonal -> MINUS placeholder
    A4 = tob(C4)
    A1p, A1m, A4p, A4m = [], [], [], []
    for i in range(m):
        r = bytearray(A1[i])
        r[i] = MINUS
        A1m.append(bytes(r))
        r[i] = PLUS
        A1p.append(bytes(r))
        r = bytearray(A4[i])
        r[i] = MINUS
        A4m.append(bytes(r))
        r[i] = PLUS
        A4p.append(bytes(r))
    B = tob(C2)
    nBt = [bytes(col).translate(NEG) for col in zip(*B)]        # -C2^t
    T = {}
    for name, blk in (("K1", K1), ("K2", K2), ("K3", K3), ("K4", K4)):
        T[name] = [bytes(col) for col in zip(*blk)]
    nK = {k: [r.translate(NEG) for r in v]
          for k, v in (("K1", K1), ("K2", K2), ("K3", K3), ("K4", K4))}
    nT = {k: [r.translate(NEG) for r in v] for k, v in T.items()}

    M = {(0, 0): A1p, (0, 1): B,         (0, 2): K1,       (0, 3): K2,
         (1, 0): nBt, (1, 1): A4p,       (1, 2): K3,       (1, 3): nK["K4"],
         (2, 0): nT["K1"], (2, 1): nT["K3"], (2, 2): A1p,  (2, 3): B,
         (3, 0): nT["K2"], (3, 1): T["K4"],  (3, 2): nBt,  (3, 3): A4p}
    N = {(0, 0): A1m, (0, 1): B,         (0, 2): nK["K1"], (0, 3): nK["K2"],
         (1, 0): nBt, (1, 1): A4m,       (1, 2): nK["K3"], (1, 3): K4,
         (2, 0): T["K1"], (2, 1): T["K3"], (2, 2): A1m,    (2, 3): B,
         (3, 0): T["K2"], (3, 1): nT["K4"], (3, 2): nBt,   (3, 3): A4m}
    return M, N


def assemble_rows(M, N, q, border=-1):
    """Yield the 4q rows of H as bytes.  Two slice assignments per block."""
    m = (q - 1) // 2
    n = 2 * m + 1
    width = 4 * n
    corner = [[PLUS if SIGMA[i][j] == 1 else MINUS for j in range(4)]
              for i in range(4)]
    bord = [[PLUS if SIGMA[i][j] * (border if i == j else -border) == 1
             else MINUS for j in range(4)] for i in range(4)]
    for i in range(4):
        row = bytearray(width)
        for j in range(4):
            base = j * n
            row[base] = corner[i][j]
            row[base + 1:base + n] = bytes([bord[i][j]]) * (n - 1)
        yield bytes(row)
        blocks = [(j * n, bord[i][j], M[(i, j)], N[(i, j)]) for j in range(4)]
        for a in range(m):
            for swap in (False, True):
                row = bytearray(width)
                for base, bc, Mb, Nb in blocks:
                    row[base] = bc
                    x, y = (Nb[a], Mb[a]) if swap else (Mb[a], Nb[a])
                    row[base + 1:base + n:2] = x
                    row[base + 2:base + n:2] = y
                yield bytes(row)


def build(q, Hq1, outpath, calibrate=False, border=-1):
    m = (q - 1) // 2
    log("=== q = %d  (prime = 1 mod 4; m = %d; target order 4q = %d) ==="
        % (q, m, 4 * q))
    check("q=%d is prime and = 1 (mod 4)" % q, is_prime(q) and q % 4 == 1)
    C1, C2, C4 = eform(q)
    eblock_identities(q, C1, C2, C4, calibrate)
    K1, K2, K3, K4 = k_blocks(q, Hq1, calibrate)
    uv_checks(q, C1, C2, C4, K1, K2, K3, K4, calibrate)
    M, N = merge_blocks(C1, C2, C4, K1, K2, K3, K4)
    del C1, C2, C4, K1, K2, K3, K4
    header = (b"# H(%d) -- Miyamoto JCTA 57 (1991) Thm 5 / Cor 1 "
              b"(= Djokovic arXiv:1008.2043 Thm 2.4) at q = %d,\n"
              b"# from H(%d).  Border variant: printed(%d).  "
              b"Certificate 01, standard library only.\n"
              % (4 * q, q, q - 1, border))
    sha = emit(outpath, header, assemble_rows(M, N, q, border=border), 4 * q)
    del M, N
    log("wrote %s (%.1f MB), canonical sha256 = %s"
        % (os.path.basename(outpath), os.path.getsize(outpath) / 1e6, sha))
    return sha


# ------------------------------------------------------------------ stages

def sylvester(order):
    """Sylvester Hadamard matrix of a power-of-two order, as bytes rows."""
    h = [[1]]
    while len(h) < order:
        h = [r + r for r in h] + [r + [-v for v in r] for r in h]
    if len(h) != order:
        raise ValueError("order %d is not a power of two" % order)
    return [bytes(PLUS if v == 1 else MINUS for v in r) for r in h]


def stage_gate(outdir):
    """Stage 1: the same code path on two cases with known answers."""
    log("STAGE 1 -- grounding gate: q = 5 from H(4), q = 257 from H(256)")
    kept = None
    for q in (5, 257):
        Hq1 = sylvester(q - 1)
        check("q=%d: the Sylvester H(%d) input is a %dx%d +-1 matrix"
              % (q, q - 1, q - 1, q - 1),
              len(Hq1) == q - 1 and all(len(r) == q - 1 for r in Hq1))
        out = os.path.join(outdir, "H%d_gate.txt" % (4 * q))
        sha = build(q, Hq1, out, calibrate=(q == 5))
        want = GATE_SHA[q]
        rc, line = run_verify(out)
        check("q=%d: H(%d) verify.py exit 0 at the pinned canonical sha"
              % (q, 4 * q),
              rc == 0 and "order=%d" % (4 * q) in line and want in line)
        check("q=%d: canonical sha256 == pinned %s..." % (q, want[:16]),
              sha == want, sha)
        rows = read_pm(out)
        if q == 5:
            check("q=%d: H(%d) re-checked by an independent packed-integer "
                  "popcount path" % (q, 4 * q), hadamard_by_popcount(rows))
            kept = rows
        os.unlink(out)
    return kept


def stage_input(outdir):
    """Stage 2: rebuild H(1948) from the banked seeds and green it. Returns
    None if any of its checks failed, so the composite is never attempted on
    an input that failed the trust chain."""
    fails_before = len(FAIL)
    log("STAGE 2 -- rebuild the H(1948) input from data/h1948-seeds.json")
    with open(DATA, encoding="ascii") as fh:
        bank = json.load(fh)
    src, con = bank["source"], bank["construction"]
    print("  announcement %s (%s)"
          % (src["announcement_url"], src["announcement_date"]))
    print("  tape sha256 = %s (%d chars), seeds at tape[%d:%d]"
          % (src["tape_sha256"], src["tape_length"],
             src["tape_slice"][0], src["tape_slice"][1]))
    print("  construction: %s over Z_%d, s = %d, r_shift = %d"
          % (con["array"], con["group_order"], con["s"], con["r_shift"][0]))

    seeds = bank["seeds"]
    check("the banked entry declares order 1948 and four +-1 seeds of "
          "length 487",
          bank["order"] == 1948 and len(seeds) == 4
          and all(len(s) == 487 for s in seeds)
          and all(v in (1, -1) for s in seeds for v in s))
    check("the construction parameters are the plain Goethals-Seidel array "
          "over Z_487 (s = 0, r_shift = 486, standard)",
          con["group"] == [487] and con["group_order"] == 487
          and int(con["s"]) == 0 and con["r_shift"] == [486]
          and con["gs_variant"] == "standard")

    rows = goethals_seidel_cyclic(seeds, con["r_shift"][0])
    check("the builder returned a 1948 x 1948 +-1 matrix",
          len(rows) == 1948 and all(len(r) == 1948 for r in rows)
          and all(set(r) <= {PLUS, MINUS} for r in rows))
    sha = canonical_sha(rows)
    check("rebuilt H(1948) canonical sha256 == pinned %s..." % H1948_SHA[:16],
          sha == H1948_SHA, sha)
    path = os.path.join(outdir, "H1948_input.txt")
    got = emit(path, b"# H(1948) -- rebuilt from data/h1948-seeds.json, "
                     b"plain Goethals-Seidel over Z_487.\n", iter(rows), 1948)
    rc, line = run_verify(path)
    check("H(1948) is verify.py green BEFORE it is consumed",
          rc == 0 and "order=1948" in line and H1948_SHA in line
          and got == H1948_SHA)
    os.unlink(path)
    if len(FAIL) > fails_before:
        return None
    return rows


def stage_target(outdir, h1948):
    """Stage 3: the composite at q = 1949."""
    log("STAGE 3 -- the target: q = 1949, H(4 * 1949) = H(7796)")
    check("q = 1949 = 4*487 + 1, and the H(1948) seed group is Z_487",
          1949 == 4 * 487 + 1 and is_prime(1949) and is_prime(487))
    out = os.path.join(outdir, "H7796_miyamoto.txt")
    sha = build(1949, h1948, out)
    rc, line = run_verify(out)
    check("H(7796): verify.py exit 0, order=7796, all 30384910 row pairs "
          "orthogonal",
          rc == 0 and "order=7796" in line
          and "30384910 row pairs" in line and "HADAMARD" in line)
    check("H(7796): canonical sha256 == pinned %s..." % H7796_SHA[:16],
          sha == H7796_SHA and H7796_SHA in line, sha)
    os.unlink(out)
    print("  artifact deleted after verification; the pinned digest binds it")


def stage_control(outdir, h20):
    """Stage 4: the checks are not vacuous."""
    log("STAGE 4 -- negative control on the verified H(20)")
    if not h20:
        check("the gate produced an H(20) to corrupt", False)
        return
    bad = [bytearray(r) for r in h20]
    bad[3][5] = PLUS if bad[3][5] == MINUS else MINUS
    badrows = [bytes(r) for r in bad]
    check("one flipped entry is rejected by the independent popcount path",
          not hadamard_by_popcount(badrows))
    badpath = os.path.join(outdir, "H20_CONTROL_corrupt.txt")
    emit(badpath, None, iter(badrows), 20)
    rc, line = run_verify(badpath)
    check("one flipped entry is REJECTED by verify.py (exit 1)",
          rc == 1 and "FAIL" in line)
    os.unlink(badpath)


def stage_openness():
    """Stage 5: a reading of a dated table, parsed here and printed with its
    label."""
    log("STAGE 5 -- the openness of order 7796, with its label")
    d = json.load(open(TABLE4, encoding="ascii"))
    prov = d["provenance"]
    table = {int(k): int(v) for k, v in d["entries"].items()}
    print("  source: %s" % prov["source"])
    check("data/cp-table4-v2.json loads and holds all %d entries, every one "
          "at an odd n <= %d" % (prov["entry_count"], prov["range"]["n_max"]),
          len(table) == prov["entry_count"] == 195
          and all(n % 2 and n <= prov["range"]["n_max"] and m >= 3
                  for n, m in table.items()))
    m = table.get(1949)
    check("the entry for n = 1949 reads 1949(4)", m == 4)
    check("m = 4 means the smallest 2^t * 1949 that table records as known is "
          "2^4 * 1949 = %d, so NEITHER 4 * 1949 = 7796 NOR 8 * 1949 = 15592 "
          "was recorded known there" % (16 * 1949),
          m is not None and m > 3)
    print("  REPORTED-FROM-AUDITED-TABLE. 4 * 1949 = 7796 is listed")
    print("  unresolved in that table, and so is 8 * 1949 = 15592, which the")
    print("  matrix built above therefore also settles by Sylvester doubling.")
    print("  A table records what its authors knew on its date. This is a")
    print("  reading of that table, not a non-existence proof, and the entry")
    print("  may have been overtaken since.")


# ---------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description="Certificate 01 -- H(7796) by Miyamoto's 1991 theorem.")
    ap.add_argument("--gate-only", action="store_true",
                    help="stages 1, 2, 4, 5 only (skip the 7796 build)")
    args = ap.parse_args()

    if not (os.path.exists(VERIFY) and os.path.exists(DATA)
            and os.path.exists(TABLE4)):
        print("ERROR: run this from the repository root (verify/verify.py, "
              "data/h1948-seeds.json and data/cp-table4-v2.json not all found "
              "here).")
        return 2

    os.makedirs(OUTDIR, exist_ok=True)
    print("CERTIFICATE 01 -- H(7796) = H(4 * 1949), Miyamoto 1991 Thm 5 / Cor 1")
    print("python %s ; standard library only ; artifacts in %s/, deleted "
          "after verification\n" % (sys.version.split()[0], OUTDIR))

    h20 = stage_gate(OUTDIR)
    print()
    h1948 = stage_input(OUTDIR)
    print()
    if not args.gate_only:
        if h1948 is None:
            print("  STAGE 3 SKIPPED -- the H(1948) input failed the trust "
                  "chain; the composite is not attempted on it.")
        else:
            stage_target(OUTDIR, h1948)
        print()
    stage_control(OUTDIR, h20)
    print()
    stage_openness()

    try:
        os.rmdir(OUTDIR)
    except OSError:
        pass

    print("\n-- elapsed %.1fs --" % (time.time() - _T0))
    if FAIL:
        print("CERTIFICATE 01: FAIL (%d): %s" % (len(FAIL), FAIL))
        return 1
    if args.gate_only:
        print("CERTIFICATE 01: PARTIAL PASS (--gate-only; H(7796) not built)")
        return 0
    print("CERTIFICATE 01: PASS -- the engine grounded at q = 5 and q = 257, "
          "H(1948)\n  rebuilt from the banked seeds and greened before use, "
          "every hypothesis\n  re-checked in exact integers at q = 1949, and "
          "H(7796) accepted by\n  verify.py at canonical sha %s" % H7796_SHA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
