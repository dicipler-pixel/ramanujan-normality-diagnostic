# SCRIPT: validate_diagnostic
#
# Runs recurrence_diagnostic.diagnose() against 5 independently-verifiable
# cases and checks the classification against known ground truth.

import sympy as sp
from recurrence_diagnostic import diagnose

n = sp.symbols('n')

CASES = []

# 2.2 -- gamma Apery limit. Ground truth: OPEN (no closed form found).
a0 = -(8*n**3+51*n**2+105*n+68)
a1 = 24*n**5+337*n**4+1833*n**3+4818*n**2+6092*n+2928
a2 = -(n+2)*(n+3)*(24*n**5+273*n**4+1150*n**3+2154*n**2+1635*n+268)
a3 = (n+1)*(n+2)**4*(n+3)*(8*n**3+75*n**2+231*n+232)
CASES.append(("2.2 gamma (OPEN)", [a0, a1, a2, a3], True))

# 2.4 -- T(m) inner recurrence. Ground truth: this piece is SOLVED
# (guessed + verified exactly); the separate outer sum is open, but that's
# a different object layered on top, not this recurrence's own obstruction.
c4 = (576*n**10+13536*n**9+138484*n**8+809733*n**7+2985986*n**6+7225375*n**5
      +11554836*n**4+11965706*n**3+7587960*n**2+2607840*n+355968)
c3 = -(7488*n**10+164448*n**9+1581988*n**8+8750321*n**7+30699902*n**6+71052846*n**5
       +109209090*n**4+109189237*n**3+67178640*n**2+22557240*n+3049920)
c2 = (34560*n**10+705024*n**9+6318960*n**8+32675460*n**7+107579986*n**6+234597976*n**5
      +341182650*n**4+324239568*n**3+190653656*n**2+61694168*n+8174112)
c1 = -(64512*n**10+1211904*n**9+9978304*n**8+47310192*n**7+142648192*n**6+284793476*n**5
       +379520812*n**4+331300928*n**3+179836956*n**2+54258020*n+6843984)
c0 = (36864*n**10+626688*n**9+4605184*n**8+19176128*n**7+49862496*n**6+84169200*n**5
      +92965080*n**4+66094152*n**3+28898360*n**2+7025752*n+723936)
CASES.append(("2.4 T(m) inner recurrence (SOLVED)", [c0, c1, c2, c3, c4], False))

# 2.6 -- zeta(2)+zeta(3). Ground truth: NOT fully closed-form (one
# constant remains open) -- included as a genuine, honestly-labeled
# borderline case, not cherry-picked to fit.
d0 = -2*(n+3)**3*(2*n+5)*(3*n+5)
d1 = (n+2)**2*(15*n**3+85*n**2+155*n+93)
d2 = -(n+1)**3*(n+2)*(3*n+8)
CASES.append(("2.6 zeta(2)+zeta(3) (partially OPEN)", [d0, d1, d2], None))

# 3.2 -- Apery's own zeta(3) recurrence. Ground truth: FAMOUSLY SOLVED.
e0 = (n+1)**3
e1 = -(34*n**3+51*n**2+27*n+5)
e2 = n**3
CASES.append(("3.2 Apery zeta(3) (SOLVED)", [e0, e1, e2], False))

# Fibonacci. Ground truth: trivially solved.
CASES.append(("Fibonacci (SOLVED, trivial)",
               [sp.Integer(1), sp.Integer(-1), sp.Integer(-1)], False))


def main():
    correct = 0
    total_checked = 0
    for label, coeffs, expect_obstructed in CASES:
        print("=" * 70)
        print(label)
        print("=" * 70)
        result = diagnose(coeffs, var=n, n_range=(10, 50, 100, 200, 500))
        if expect_obstructed is not None:
            total_checked += 1
            match = result['diverging'] == expect_obstructed
            correct += match
            print("Matches ground truth:", match)
        else:
            print("(borderline case, not scored -- see writeup for discussion)")
        print()

    print(f"Score: {correct}/{total_checked} scored cases matched ground truth")


if __name__ == "__main__":
    main()
