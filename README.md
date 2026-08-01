# Companion-Matrix Normality Diagnostic for Candidate Recurrences

A universal diagnostic for linear recurrences: given a candidate holonomic
recurrence, this tool builds its companion matrix and checks whether its
transport geometry is well-conditioned or genuinely obstructed — a
practical signal for whether a plain, single-hypergeometric-term closed
form is likely to exist.

## The method

For any recurrence `a0(n)u_n + a1(n)u_{n-1} + ... + ak(n)u_{n-k} = 0`,
build the companion matrix `M(n)` and split it into symmetric and
skew-symmetric parts, `M = S + K`. Whether `[S,K] = 0` (normal) or not
governs the pseudospectrum: for a non-normal operator, the pseudospectrum
can bulge far outside a δ-ball around the eigenvalues even when the system
is asymptotically stable (Trefethen & Embree, *Spectra and Pseudospectra*)
— and that bulge is the real mechanism behind transient/ill-conditioned
behavior, not the eigenvalues alone.

Three quantities are tracked as `n` grows:
- **SVD rank-one residual** — how fast the cumulative transport collapses toward rank one
- **Spectral stress Φ(P) = ½‖[P,Pᵀ]‖²_F** — how non-normal the transport becomes
- **Riesz projector norm ‖Π(n)‖₂** — operator norm of the projector onto the dominant eigenspace

## The classification rule (sharpened by testing, not assumed)

The original hypothesis was "a characteristic root of multiplicity ≥3
rules out plain monomial-sum closed forms." Testing that against 5
independently-verifiable cases with known ground truth showed it's too
coarse — two cases (`2.2`, `2.4`) both have genuine triple roots, but
behave completely differently:

| Case | Root structure | Ground truth | Riesz projector ‖Π(n)‖₂ | Diagnostic verdict |
|---|---|---|---|---|
| **γ Apéry limit** | triple root | **OPEN** | diverges (10⁴→10¹¹) | ✅ obstructed |
| **T(m) inner recurrence** | triple root | **SOLVED** | bounded (~6) | ✅ unobstructed |
| **ζ(2)+ζ(3) series** | distinct roots | partially open | bounded (~2) | — (declines to call it, honestly) |
| **Apéry's ζ(3)** | distinct roots | **famously SOLVED** | bounded (~1.0) | ✅ unobstructed |
| **Fibonacci** | distinct roots | trivially solved | bounded (=1) | ✅ unobstructed |

**4/4 scored cases matched ground truth.** Root multiplicity ≥3 turned out
to be necessary but not sufficient — the load-bearing signal is whether
the **Riesz projector norm actually diverges**, not the multiplicity
count alone. Rank-one collapse *rate* was tested too and found to be
uninformative on its own: it tracks the raw spectral gap between the top
two roots, not problem difficulty (Fibonacci — the most trivial possible
case — collapses slowly; Apéry's famous solved case collapses fast).

## Usage

```python
import sympy as sp
from recurrence_diagnostic import diagnose

n = sp.symbols('n')
# for a0(n)u_n + a1(n)u_{n-1} + a2(n)u_{n-2} = 0
diagnose([a0_expr, a1_expr, a2_expr], var=n)
```

That's the whole setup — hand it the recurrence's own coefficients (same
requirement as any CAS/Ore tool) and it builds the companion matrix, runs
all three diagnostics, and returns a classification automatically. No
per-case tuning beyond supplying the coefficients.

## Files

- `recurrence_diagnostic.py` — the diagnostic itself
- `validate_diagnostic.py` — the 5-case validation suite above, runnable directly

## Honest scope

This is a **necessary-condition filter**, not a proof tool. An
"unobstructed" verdict rules out this specific obstruction; it does not
guarantee a closed form exists or is easy to find. An "obstructed"
verdict is a strong signal that plain monomial-sum ansätze are the wrong
shape to search, based on the pattern observed across the validated cases
above.
