"""
Bell / Mermin Inequality Simulation - N-Particle Entanglement
=============================================================

Part 1: CHSH (2 particles) — does S break 2?
Part 2: Mermin (N particles) — exponential scaling
Part 3: GHZ one-shot proof (3 particles) — deterministic contradiction
Part 4: DECOHERENCE — can entanglement survive noise?

The big question:
  Quantum signal grows as 2^(N/2) with more particles.
  Decoherence destroys signal as particles interact with environment.
  Which one wins?

Run it:  python bell_simulation.py
"""

import math
import random
from itertools import product as cartesian


# =====================================================================
#  CORE: GHZ state measurement with decoherence
# =====================================================================

def ghz_state_measurement(n, angles, decoherence=0.0):
    """
    Simulate measuring an N-particle GHZ entangled state.

    GHZ state: (|00...0> + |11...1>) / sqrt(2)

    Decoherence model (depolarizing noise):
      decoherence = 0.0  ->  perfect entanglement
      decoherence = 1.0  ->  completely random (no entanglement)

    What decoherence does physically:
      The environment "measures" the particles before you do.
      Each interaction with the environment destroys some quantum
      correlation and replaces it with classical randomness.

    For N particles, decoherence compounds: the effective noise
    grows as (1 - decoherence)^N. More particles = more fragile.

    The quantum prediction for product of all results:
      <product> = cos(sum of angles) * (1 - decoherence)^N
    """
    angle_sum = sum(angles)

    # Decoherence: each particle independently loses coherence
    # Surviving quantum correlation decays exponentially with N
    visibility = (1 - decoherence) ** n
    quantum_correlation = math.cos(angle_sum) * visibility

    # Probability that product of all measurements = +1
    prob_positive = (1 + quantum_correlation) / 2

    if random.random() < prob_positive:
        target_product = +1
    else:
        target_product = -1

    # Generate N-1 random results, fix the last one
    results = [random.choice([+1, -1]) for _ in range(n - 1)]

    current_product = 1
    for r in results:
        current_product *= r

    results.append(target_product * current_product)
    return results


# =====================================================================
#  PART 1 — CHSH (2 particles)
# =====================================================================

def run_chsh(num_trials=50000, decoherence=0.0):
    """Run the 2-particle CHSH test with optional decoherence."""
    a1, a2 = 0, math.pi / 4
    b1, b2 = math.pi / 8, 3 * math.pi / 8

    correlations = []
    for angle_a, angle_b in [(a1, b1), (a1, b2), (a2, b1), (a2, b2)]:
        total = 0
        for _ in range(num_trials):
            results = ghz_state_measurement(2, [angle_a, angle_b], decoherence)
            total += results[0] * results[1]
        correlations.append(total / num_trials)

    e_ab, e_ab2, e_a2b, e_a2b2 = correlations
    return abs(e_ab - e_ab2 + e_a2b + e_a2b2)


# =====================================================================
#  PART 2 — MERMIN (N particles)
# =====================================================================

def mermin_coefficients_recursive(n):
    """
    Build Mermin operator coefficients recursively.

    Returns dict: {(s1, s2, ..., sn): coefficient}
    where si = 0 means "use angle X", si = 1 means "use angle Y".
    """
    if n == 1:
        return {(0,): 1.0, (1,): 1.0}

    prev = mermin_coefficients_recursive(n - 1)

    prev_prime = {}
    for settings, coeff in prev.items():
        flipped = tuple(1 - s for s in settings)
        prev_prime[flipped] = coeff

    result = {}
    for settings, c in prev.items():
        key0 = settings + (0,)
        result[key0] = result.get(key0, 0) + c * 0.5
        key1 = settings + (1,)
        result[key1] = result.get(key1, 0) + c * 0.5

    for settings, c in prev_prime.items():
        key0 = settings + (0,)
        result[key0] = result.get(key0, 0) + c * 0.5
        key1 = settings + (1,)
        result[key1] = result.get(key1, 0) - c * 0.5

    return result


def mermin_quantum_value(n, num_trials=50000, decoherence=0.0):
    """Compute Mermin operator value for N entangled (GHZ) particles."""
    angle_x = 0
    angle_y = math.pi / (2 * n)

    coeffs = mermin_coefficients_recursive(n)

    total = 0
    for settings, coeff in coeffs.items():
        if abs(coeff) < 1e-12:
            continue

        angles = [angle_y if s else angle_x for s in settings]

        corr_sum = 0
        for _ in range(num_trials):
            results = ghz_state_measurement(n, angles, decoherence)
            product = 1
            for r in results:
                product *= r
            corr_sum += product
        correlation = corr_sum / num_trials

        total += coeff * correlation

    return abs(total)


def mermin_classical_value(n):
    """Best classical value via brute force (or known result for n>6)."""
    if n > 6:
        return 2.0

    coeffs = mermin_coefficients_recursive(n)
    best = 0

    for strategy in cartesian(cartesian([+1, -1], repeat=2), repeat=n):
        val = 0
        for settings, coeff in coeffs.items():
            if abs(coeff) < 1e-12:
                continue
            product = 1
            for i in range(n):
                product *= strategy[i][settings[i]]
            val += coeff * product
        if abs(val) > best:
            best = abs(val)

    return best


# =====================================================================
#  PART 3 — GHZ ONE-SHOT PROOF (3 particles)
# =====================================================================

def ghz_one_shot_demo(num_trials=10000, decoherence=0.0):
    """GHZ theorem: entanglement proven in a single measurement."""
    results = {"XXX": [], "XYY": [], "YXY": [], "YYX": []}
    angle_x, angle_y = 0, math.pi / 2

    combos = {
        "XXX": [angle_x, angle_x, angle_x],
        "XYY": [angle_x, angle_y, angle_y],
        "YXY": [angle_y, angle_x, angle_y],
        "YYX": [angle_y, angle_y, angle_x],
    }

    for _ in range(num_trials):
        for label, angles in combos.items():
            r = ghz_state_measurement(3, angles, decoherence)
            results[label].append(r[0] * r[1] * r[2])

    return results


# =====================================================================
#  PART 4 — DECOHERENCE: Can entanglement survive noise?
# =====================================================================

def find_critical_decoherence(n, num_trials=10000):
    """
    Find the decoherence level where quantum signal drops to classical limit.

    Binary search for the threshold where Mermin value = 2.0
    (the classical limit).

    Returns the critical decoherence rate.
    """
    low, high = 0.0, 1.0

    for _ in range(15):  # 15 iterations of binary search = high precision
        mid = (low + high) / 2
        val = mermin_quantum_value(n, num_trials, decoherence=mid)
        if val > 2.0:
            low = mid  # Still violating, increase noise
        else:
            high = mid  # Lost violation, decrease noise

    return (low + high) / 2


# =====================================================================
#  MAIN
# =====================================================================

def main():
    num_trials = 30000

    print("=" * 70)
    print("  N-PARTICLE ENTANGLEMENT vs DECOHERENCE")
    print("  The race: exponential signal vs exponential noise")
    print("=" * 70)
    print()

    # ── Part 1: CHSH ─────────────────────────────────────────────
    print("--- PART 1: CHSH (2 particles, perfect conditions) ---")
    print()
    s = run_chsh(num_trials)
    print(f"  Quantum S:         {s:.4f}")
    print(f"  Classical limit:   2.0000")
    print(f"  Theory predicts:   {2 * math.sqrt(2):.4f}")
    print(f"  Violation:         +{s - 2:.4f}")
    print()

    # ── Part 2: Mermin scaling ────────────────────────────────────
    print("--- PART 2: MERMIN SCALING (perfect conditions) ---")
    print()
    print(f"  {'N':>3}  {'Quantum S':>12}  {'Classical':>12}  {'Theory Q':>12}  {'Violated?':>10}")
    print(f"  {'---':>3}  {'----------':>12}  {'----------':>12}  {'----------':>12}  {'---------':>10}")

    for n in range(2, 7):
        trials = max(5000, num_trials // (2 ** (n - 2)))
        q_val = mermin_quantum_value(n, trials)
        c_val = mermin_classical_value(n)
        theory = 2 ** (n / 2)
        violated = "YES" if q_val > c_val + 0.1 else "no"
        print(f"  {n:>3}  {q_val:>12.4f}  {c_val:>12.4f}  {theory:>12.4f}  {violated:>10}")

    print()

    # ── Part 3: GHZ one-shot ──────────────────────────────────────
    print("--- PART 3: GHZ ONE-SHOT (3 particles, perfect) ---")
    print()
    ghz = ghz_one_shot_demo(num_trials)
    for label in ["XYY", "YXY", "YYX", "XXX"]:
        avg = sum(ghz[label]) / len(ghz[label])
        print(f"  {label}:  product = {avg:+.4f}")
    avg_xxx = sum(ghz["XXX"]) / len(ghz["XXX"])
    print()
    print(f"  Hidden variables demand XXX = -1.  Quantum gives: {avg_xxx:+.4f}")
    print()

    # ── Part 4: DECOHERENCE ───────────────────────────────────────
    print("=" * 70)
    print("  PART 4: DECOHERENCE — THE BIG QUESTION")
    print("  How much noise can entanglement survive?")
    print("=" * 70)
    print()
    print("  Decoherence = 0.00: perfect lab, zero noise")
    print("  Decoherence = 0.05: excellent lab conditions")
    print("  Decoherence = 0.10: good conditions")
    print("  Decoherence = 0.20: noisy environment")
    print("  Decoherence = 0.50: very noisy (biological? room temp?)")
    print("  Decoherence = 1.00: total noise, no quantum signal")
    print()

    # 4A: CHSH under increasing noise
    print("--- 4A: 2 particles (CHSH) under noise ---")
    print()
    print(f"  {'Decoherence':>12}  {'S value':>10}  {'Limit':>8}  {'Status':>20}")
    print(f"  {'----------':>12}  {'--------':>10}  {'------':>8}  {'------------------':>20}")

    for d in [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]:
        s_val = run_chsh(num_trials, decoherence=d)
        if s_val > 2.05:
            status = "VIOLATION"
        elif s_val > 1.95:
            status = "borderline"
        else:
            status = "classical (dead)"
        print(f"  {d:>12.2f}  {s_val:>10.4f}  {2.0:>8.2f}  {status:>20}")

    print()

    # 4B: N particles under fixed noise levels
    print("--- 4B: N particles at different noise levels ---")
    print()
    print("  THE RACE: quantum signal grows as 2^(N/2)")
    print("            but decoherence kills as (1-d)^N")
    print()

    noise_levels = [0.00, 0.02, 0.05, 0.10, 0.20]
    header = f"  {'N':>3}"
    for d in noise_levels:
        header += f"  {'d='+str(d):>10}"
    header += f"  {'Classical':>10}"
    print(header)
    print(f"  {'---':>3}" + f"  {'--------':>10}" * (len(noise_levels) + 1))

    for n in range(2, 7):
        trials = max(3000, num_trials // (2 ** (n - 2)))
        row = f"  {n:>3}"
        for d in noise_levels:
            q_val = mermin_quantum_value(n, trials, decoherence=d)
            marker = "*" if q_val > 2.0 else " "
            row += f"  {q_val:>9.4f}{marker}"
        row += f"  {2.0:>10.4f}"
        print(row)

    print()
    print("  * = still violating classical limit (entanglement detected)")
    print()

    # 4C: GHZ one-shot under noise
    print("--- 4C: GHZ one-shot proof under noise ---")
    print()
    print("  Perfect: XXX should be +1.00, opposite of classical -1")
    print("  As noise increases, the signal fades toward 0 (random)")
    print()
    print(f"  {'Decoherence':>12}  {'XXX avg':>10}  {'XYY avg':>10}  {'Proof holds?':>15}")
    print(f"  {'----------':>12}  {'--------':>10}  {'--------':>10}  {'------------':>15}")

    for d in [0.0, 0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00]:
        ghz = ghz_one_shot_demo(10000, decoherence=d)
        xxx = sum(ghz["XXX"]) / len(ghz["XXX"])
        xyy = sum(ghz["XYY"]) / len(ghz["XYY"])

        if xxx > 0.5:
            status = "YES (strong)"
        elif xxx > 0.1:
            status = "weak signal"
        elif xxx > -0.1:
            status = "noise (dead)"
        else:
            status = "flipped (??)"

        print(f"  {d:>12.2f}  {xxx:>+10.4f}  {xyy:>+10.4f}  {status:>15}")

    print()

    # 4D: Critical decoherence threshold
    print("--- 4D: Critical noise threshold per particle count ---")
    print()
    print("  How much noise before entanglement becomes undetectable?")
    print()
    print(f"  {'N particles':>12}  {'Max survivable noise':>22}  {'Interpretation':>30}")
    print(f"  {'----------':>12}  {'--------------------':>22}  {'----------------------------':>30}")

    interpretations = {
        2: "",
        3: "",
        4: "",
        5: "",
        6: "",
    }

    for n in range(2, 7):
        trials = max(3000, 10000 // (2 ** (n - 2)))
        crit = find_critical_decoherence(n, trials)
        interpretations[n] = crit

        if crit > 0.25:
            interp = "robust — survives noisy conditions"
        elif crit > 0.10:
            interp = "moderate — needs decent isolation"
        elif crit > 0.05:
            interp = "fragile — needs good lab conditions"
        else:
            interp = "ultra-fragile — near-perfect isolation"

        print(f"  {n:>12}  {crit:>22.4f}  {interp:>30}")

    print()

    # ── Final summary ─────────────────────────────────────────────
    print("=" * 70)
    print("  WHAT WE LEARNED")
    print("=" * 70)
    print()
    print("  1. MORE PARTICLES = STRONGER SIGNAL (exponential)")
    print("     But also = MORE FRAGILE (exponential decay)")
    print()
    print("  2. IT'S A RACE between two exponentials:")
    print("     Signal grows as:  2^(N/2)")
    print("     Noise kills as:   (1-d)^N")
    print()
    print("  3. For small noise (d < 0.05), adding particles HELPS.")
    print("     The signal growth outpaces the fragility.")
    print("     For large noise (d > 0.20), adding particles HURTS.")
    print("     Each new particle is another thing that can break.")
    print()
    print("  4. THE CROSSOVER is where it gets interesting.")
    print("     There's a sweet spot: enough particles for strong signal,")
    print("     few enough to survive the noise.")
    print()
    print("  5. THE FRONTIER QUESTION:")
    print("     If natural systems have low decoherence (d ~ 0.01-0.05),")
    print("     entanglement of 10-100 particles could produce")
    print("     detectable signals that nobody is measuring.")
    print()
    print("     Photosynthesis, bird navigation, neural microtubules —")
    print("     these are warm, wet, noisy systems. But 'noisy' might")
    print("     not mean 'too noisy' if the entanglement is structured")
    print("     in the right way.")
    print()


if __name__ == "__main__":
    main()
