"""
QDP-1: Quantum Detection Protocol v1 — Formal Specification
=============================================================

A 7-stage framework for detecting quantum coherence effects
in radical pair systems at ambient conditions.

Each stage defines:
  - MATHEMATICAL BASIS: what is being measured and why
  - DECISION CRITERION: pass/fail threshold with justification
  - SCORING: weighted contribution to final verdict

Stages:
  1. BASELINE          — noise floor characterization
  2. DIFFERENTIAL       — angular dependence via (A-B)/(A+B)
  3. CONTROLS           — artifact elimination
  4. ANGULAR SHAPE      — cos^2 fit via Fourier decomposition
  5. NOISE DECAY        — decoherence fingerprint
  6. FIELD SCALING      — power law test
  7. TEMPERATURE        — thermal scaling behavior

Final verdict: weighted score across all stages.

Run:  python qdp1_formal.py
"""

import math
import random


# =====================================================================
#  FOUNDATIONS
# =====================================================================

def poisson(lam):
    if lam <= 0: return 0
    if lam > 100:
        return max(0, int(random.gauss(lam, math.sqrt(lam)) + 0.5))
    L = math.exp(-lam)
    k, p = 0, 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1


class System:
    """A radical pair system to test."""
    def __init__(self, name, field_ratio=0.05, base_photons=1000,
                 description=""):
        self.name = name
        self.field_ratio = field_ratio
        self.base_photons = base_photons
        self.description = description

    def yield_at(self, theta, field_ratio_override=None):
        fr = field_ratio_override if field_ratio_override is not None else self.field_ratio
        b = fr * math.cos(theta)
        w = 2 * math.pi * b
        return 0.25 + 0.25 / (1 + w * w)


class Noise:
    """Realistic noise model."""
    def __init__(self, led_drift=0.005, dark=20, bleach=0.1, read=5.0):
        self.led_drift = led_drift
        self.dark = dark
        self.bleach = bleach
        self.read = read


def pulse(system, theta, noise, progress=0.0, temp_offset=0.0,
          field_ratio_override=None):
    """One fluorescence measurement pulse. Returns photon count."""
    y = system.yield_at(theta, field_ratio_override)
    sig = system.base_photons * y * 2

    # Temperature effect on yield: ~0.2% per degree
    if temp_offset != 0:
        sig *= (1 + 0.002 * temp_offset)

    if noise.led_drift > 0:
        sig *= (1 + random.gauss(0, noise.led_drift))
    sig *= math.exp(-noise.bleach * progress)

    det = poisson(max(0, sig))
    if noise.dark > 0: det += poisson(noise.dark)
    if noise.read > 0: det = max(0, det + int(random.gauss(0, noise.read) + 0.5))
    return det


def pulse_classical(system, noise, progress=0.0, temp_offset=0.0):
    """Measurement with no angular dependence (control)."""
    sig = system.base_photons * 0.5 * 2
    if temp_offset != 0:
        sig *= (1 + 0.002 * temp_offset)
    if noise.led_drift > 0:
        sig *= (1 + random.gauss(0, noise.led_drift))
    sig *= math.exp(-noise.bleach * progress)
    det = poisson(max(0, sig))
    if noise.dark > 0: det += poisson(noise.dark)
    if noise.read > 0: det = max(0, det + int(random.gauss(0, noise.read) + 0.5))
    return det


def differential(system, noise, theta_a, theta_b, n_pulses, block=10,
                 classical=False, field_ratio_override=None, temp_offset=0.0):
    """
    Block-randomized differential measurement.

    Returns (mean_contrast, se, z_score)

    Math:
      For each block of 2*B pulses:
        C_i = (sum_A - sum_B) / (sum_A + sum_B)
      Mean contrast = mean(C_i)
      SE = std(C_i) / sqrt(N_blocks)
      Z = |mean| / SE
    """
    contrasts = []
    total = n_pulses
    done = 0

    while done < total:
        progress = done / total
        sa, sb = 0, 0
        for _ in range(block):
            if classical:
                sa += pulse_classical(system, noise, progress, temp_offset)
                sb += pulse_classical(system, noise, progress, temp_offset)
            else:
                sa += pulse(system, theta_a, noise, progress, temp_offset,
                            field_ratio_override)
                sb += pulse(system, theta_b, noise, progress, temp_offset,
                            field_ratio_override)
        done += 2 * block
        if sa + sb > 0:
            contrasts.append((sa - sb) / (sa + sb))

    if not contrasts:
        return 0, 1, 0

    m = sum(contrasts) / len(contrasts)
    v = sum((c - m) ** 2 for c in contrasts) / len(contrasts)
    se = math.sqrt(v / len(contrasts))
    z = abs(m) / se if se > 0 else 0
    return m, se, z


# =====================================================================
#  STAGE 1: BASELINE
#
#  Purpose: Characterize noise floor before any signal measurement.
#
#  Math:
#    excess_noise_ratio = sigma_measured / sqrt(mean_counts)
#    If ENR < 1.5: shot-noise-limited (ideal)
#    If ENR >= 1.5: technical-noise-limited (need more controls)
#
#  Score: 1 point if shot-noise-limited
# =====================================================================

def stage1(system, noise, n=2000):
    counts = [pulse(system, 0, noise, i / n) for i in range(n)]
    m = sum(counts) / n
    std = math.sqrt(sum((c - m) ** 2 for c in counts) / n)
    shot = math.sqrt(m) if m > 0 else 1
    enr = std / shot

    half = n // 2
    drift = (sum(counts[half:]) / half - sum(counts[:half]) / half) / m * 100

    passed = enr < 1.5
    return {
        "mean": m, "std": std, "shot_predicted": shot,
        "enr": enr, "drift_pct": drift, "passed": passed,
        "score": 1 if passed else 0, "max": 1,
    }


# =====================================================================
#  STAGE 2: DIFFERENTIAL SIGNAL
#
#  Purpose: Detect angular dependence via normalized contrast.
#
#  Math:
#    C = (S_0 - S_90) / (S_0 + S_90)
#    H0: C = 0 (no angular dependence)
#    H1: C != 0 (angular dependence exists)
#    Decision: Z > 5 for detection (5-sigma)
#
#  Score: 2 points if Z > 5, 1 if Z > 3
# =====================================================================

def stage2(system, noise, n=10000):
    c, se, z = differential(system, noise, 0, math.pi / 2, n)
    if z > 5:
        score = 2
    elif z > 3:
        score = 1
    else:
        score = 0
    return {"contrast": c, "se": se, "z": z, "score": score, "max": 2}


# =====================================================================
#  STAGE 3: CONTROLS
#
#  Purpose: Eliminate artifacts. Each control must show Z < 2.
#
#  Controls:
#    C1: Same angle (0 vs 0) — detector artifact test
#    C2: No field (classical) — field artifact test
#    C3: Killed pair (classical) — radical pair requirement test
#
#  Math: Same differential measurement, but conditions that
#        should produce ZERO contrast.
#
#  Score: 2 points if ALL controls clean (Z < 2)
#         0 points if ANY control contaminated (Z > 3)
# =====================================================================

def stage3(system, noise, n=5000):
    controls = {}

    # C1: same angle
    c, se, z = differential(system, noise, 0, 0, n)
    controls["Same angle (0 vs 0)"] = {"c": c, "z": z, "clean": z < 2}

    # C2: no field
    c, se, z = differential(system, noise, 0, math.pi / 2, n, classical=True)
    controls["No field"] = {"c": c, "z": z, "clean": z < 2}

    # C3: killed pair
    c, se, z = differential(system, noise, 0, math.pi / 2, n, classical=True)
    controls["Killed pair"] = {"c": c, "z": z, "clean": z < 2}

    all_clean = all(r["clean"] for r in controls.values())
    score = 2 if all_clean else 0
    return {"controls": controls, "all_clean": all_clean,
            "score": score, "max": 2}


# =====================================================================
#  STAGE 4: ANGULAR SHAPE — Fourier Decomposition
#
#  Purpose: Confirm cos^2 angular dependence (not just two-point diff).
#
#  Math:
#    Measure yield at N angles from 0 to pi.
#    Compute Fourier coefficients:
#      a_k = (2/N) * sum(y_i * cos(k * theta_i))
#    Quantum radical pair predicts dominant 2*theta component (k=2 in
#    the full 0-2pi basis, which maps to k=1 in the 0-pi basis for cos^2).
#
#    Test: ratio of cos^2 component power to total variance.
#    If cos2_power / total_power > 0.5: strong cos^2 shape.
#
#    Also: likelihood ratio test comparing cos^2 model vs flat model.
#
#  Score: 2 points if cos2 power ratio > 0.5 AND F > 10
#         1 point if either condition met
# =====================================================================

def stage4(system, noise, n_per_angle=500, n_angles=24):
    step = math.pi / n_angles
    angles = [i * step for i in range(n_angles + 1)]
    means = []

    for theta in angles:
        total = sum(
            pulse(system, theta, noise, j / n_per_angle)
            for j in range(n_per_angle)
        )
        means.append(total / n_per_angle)

    n = len(means)
    y_mean = sum(means) / n

    # Fourier coefficient for cos(2*theta) component
    # In the 0-to-pi range, cos^2(theta) = 0.5 + 0.5*cos(2*theta)
    # So we look for the k=2 Fourier component (period pi)
    a2 = (2 / n) * sum(means[i] * math.cos(2 * angles[i]) for i in range(n))
    b2 = (2 / n) * sum(means[i] * math.sin(2 * angles[i]) for i in range(n))
    cos2_power = a2 ** 2 + b2 ** 2

    # Total variance
    total_var = sum((means[i] - y_mean) ** 2 for i in range(n))
    power_ratio = cos2_power / total_var if total_var > 0 else 0

    # F-test: cos^2 model vs flat
    cos2_vals = [math.cos(a) ** 2 for a in angles]
    c2_mean = sum(cos2_vals) / n
    num = sum((cos2_vals[i] - c2_mean) * (means[i] - y_mean) for i in range(n))
    den = sum((cos2_vals[i] - c2_mean) ** 2 for i in range(n))
    if den > 0:
        slope = num / den
        intercept = y_mean - slope * c2_mean
        ss_res = sum((means[i] - (intercept + slope * cos2_vals[i])) ** 2
                      for i in range(n))
        ss_tot = sum((means[i] - y_mean) ** 2 for i in range(n))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        ms_m = ss_tot - ss_res
        ms_r = ss_res / (n - 2) if n > 2 else 1
        f_stat = ms_m / ms_r if ms_r > 0 else 0
    else:
        r2, f_stat = 0, 0

    strong_shape = power_ratio > 0.5
    strong_f = f_stat > 10
    score = 2 if (strong_shape and strong_f) else 1 if (strong_shape or strong_f) else 0

    return {
        "a2": a2, "cos2_power": cos2_power, "total_var": total_var,
        "power_ratio": power_ratio, "r2": r2, "f_stat": f_stat,
        "score": score, "max": 2,
    }


# =====================================================================
#  STAGE 5: NOISE DECAY FINGERPRINT
#
#  Purpose: Distinguish quantum from classical decay.
#
#  Math:
#    Measure contrast at decoherence levels d = 0.0, 0.1, ..., 0.9
#    Fit two models:
#      Linear:      C(d) = a - b*d
#      Exponential:  C(d) = a * exp(-k*d)
#
#    Decision metric: R^2 difference.
#      exp_R2 - lin_R2 > 0.1  -> exponential (quantum fingerprint)
#      lin_R2 - exp_R2 > 0.1  -> linear (classical)
#      Otherwise: ambiguous
#
#  IMPORTANT CAVEAT: Exponential decay alone is NOT proof of quantum.
#    Classical processes (bleaching, thermal) also decay exponentially.
#    This test is evidence, not proof. Combined with other stages.
#
#  Score: 1 point if exponential fits better (not 2, because of caveat)
# =====================================================================

def stage5(system, noise, n_pulses=3000):
    decay_data = []
    for d in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        fr = system.field_ratio * (1 - d)
        c, _, _ = differential(system, noise, 0, math.pi / 2, n_pulses,
                                field_ratio_override=fr)
        decay_data.append((d, abs(c)))

    d_vals = [x[0] for x in decay_data]
    c_vals = [x[1] for x in decay_data]
    n = len(d_vals)

    # Linear fit
    d_m = sum(d_vals) / n
    c_m = sum(c_vals) / n
    num = sum((d_vals[i] - d_m) * (c_vals[i] - c_m) for i in range(n))
    den = sum((d_vals[i] - d_m) ** 2 for i in range(n))
    lin_b = num / den if den > 0 else 0
    lin_a = c_m - lin_b * d_m
    ss_res_l = sum((c_vals[i] - (lin_a + lin_b * d_vals[i])) ** 2 for i in range(n))
    ss_tot = sum((c_vals[i] - c_m) ** 2 for i in range(n))
    lin_r2 = 1 - ss_res_l / ss_tot if ss_tot > 0 else 0

    # Exponential fit via log transform
    log_c = [math.log(max(c, 1e-10)) for c in c_vals]
    lc_m = sum(log_c) / n
    e_num = sum((d_vals[i] - d_m) * (log_c[i] - lc_m) for i in range(n))
    e_den = sum((d_vals[i] - d_m) ** 2 for i in range(n))
    exp_k = -(e_num / e_den) if e_den > 0 else 0
    exp_a = math.exp(lc_m + exp_k * d_m)
    exp_pred = [exp_a * math.exp(-exp_k * d) for d in d_vals]
    ss_res_e = sum((c_vals[i] - exp_pred[i]) ** 2 for i in range(n))
    exp_r2 = 1 - ss_res_e / ss_tot if ss_tot > 0 else 0

    if exp_r2 - lin_r2 > 0.1:
        shape = "exponential"
    elif lin_r2 - exp_r2 > 0.1:
        shape = "linear"
    else:
        shape = "ambiguous"

    score = 1 if shape == "exponential" else 0
    return {
        "data": decay_data, "lin_r2": lin_r2, "exp_r2": exp_r2,
        "shape": shape, "score": score, "max": 1,
    }


# =====================================================================
#  STAGE 6: FIELD SCALING — Power Law Test
#
#  Purpose: Quantum radical pairs respond differently to field strength
#           than classical systems.
#
#  Math:
#    Measure contrast at field ratios spanning 2 orders of magnitude.
#    Fit power law: log(C) = alpha * log(B) + beta
#
#    Quantum prediction: alpha ~ 1 at weak fields (linear in B)
#    Classical prediction: alpha ~ 2 at weak fields (quadratic in B)
#
#    Decision: alpha < 1.5 -> quantum-like
#              alpha > 1.5 -> classical-like
#
#  Score: 1 point if alpha < 1.5
# =====================================================================

def stage6(system, noise, n_pulses=3000):
    mults = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
    data = []

    for mult in mults:
        fr = system.field_ratio * mult
        c, _, _ = differential(system, noise, 0, math.pi / 2, n_pulses,
                                field_ratio_override=fr)
        data.append((fr, abs(c)))

    # Power law fit on the weak-field portion (first 5 points)
    weak = data[:5]
    # Guard against zero field ratio (e.g., non-RP controls)
    if any(x[0] <= 0 for x in weak):
        return {
            "data": data, "alpha": float('nan'),
            "interpretation": "N/A (no field coupling)",
            "quantum_like": False, "score": 0, "max": 1,
        }
    log_f = [math.log(x[0]) for x in weak]
    log_c = [math.log(max(x[1], 1e-10)) for x in weak]
    n = len(log_f)
    lf_m = sum(log_f) / n
    lc_m = sum(log_c) / n
    num = sum((log_f[i] - lf_m) * (log_c[i] - lc_m) for i in range(n))
    den = sum((log_f[i] - lf_m) ** 2 for i in range(n))
    alpha = num / den if den > 0 else 0

    score = 1 if alpha < 1.5 else 0
    return {
        "data": data, "alpha": alpha,
        "interpretation": f"B^{alpha:.2f}",
        "quantum_like": alpha < 1.5,
        "score": score, "max": 1,
    }


# =====================================================================
#  STAGE 7: TEMPERATURE SCALING
#
#  Purpose: Quantum coherence effects typically degrade with temperature.
#           Classical magnetic effects often don't (or scale differently).
#
#  Math:
#    Measure contrast at temperature offsets from baseline.
#    Quantum prediction: contrast decreases as thermal energy
#      disrupts spin coherence. Rate depends on system but generally
#      monotonic decrease.
#    Classical prediction: weak or no temperature dependence for
#      direct magnetic effects. Fluorescence changes are symmetric
#      (up or down depending on direction).
#
#    Test: Does contrast decrease monotonically with temperature?
#    Metric: Spearman rank correlation between T and |contrast|.
#      Negative correlation = quantum-like (hotter = less coherence)
#      No correlation = classical-like
#
#  Score: 1 point if significant negative correlation
# =====================================================================

def stage7(system, noise, n_pulses=3000):
    # Temperature offsets from baseline (Kelvin)
    temp_offsets = [-10, -5, 0, 5, 10, 15, 20, 30]
    data = []

    for dt in temp_offsets:
        c, _, _ = differential(system, noise, 0, math.pi / 2, n_pulses,
                                temp_offset=dt)
        data.append((dt, abs(c)))

    # Spearman rank correlation
    n = len(data)
    t_rank = rank_data([x[0] for x in data])
    c_rank = rank_data([x[1] for x in data])

    d_sq = sum((t_rank[i] - c_rank[i]) ** 2 for i in range(n))
    rho = 1 - 6 * d_sq / (n * (n * n - 1))

    # Significant negative correlation? (rho < -0.5)
    quantum_like = rho < -0.5
    score = 1 if quantum_like else 0

    return {
        "data": data, "spearman_rho": rho,
        "quantum_like": quantum_like,
        "score": score, "max": 1,
    }


def rank_data(values):
    """Simple ranking (no tie handling needed for this use)."""
    indexed = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0] * len(values)
    for rank, (idx, _) in enumerate(indexed):
        ranks[idx] = rank + 1
    return ranks


# =====================================================================
#  FINAL VERDICT
#
#  Scoring:
#    Stage 1 (Baseline):     1 point  — quality gate
#    Stage 2 (Differential): 2 points — primary detection
#    Stage 3 (Controls):     2 points — artifact elimination
#    Stage 4 (Angular):      2 points — shape confirmation
#    Stage 5 (Noise decay):  1 point  — quantum fingerprint (caveated)
#    Stage 6 (Field scale):  1 point  — power law test
#    Stage 7 (Temperature):  1 point  — thermal scaling
#                           ----------
#                           10 points total
#
#  Verdict thresholds:
#    >= 8/10: QUANTUM COHERENCE DETECTED
#    >= 6/10: STRONG EVIDENCE — recommend follow-up
#    >= 4/10: SUGGESTIVE — needs more data
#    <  4/10: NO DETECTION
#
#  CRITICAL REQUIREMENT:
#    Stage 3 (Controls) MUST pass for any positive verdict.
#    If controls fail, verdict is capped at "INCONCLUSIVE — ARTIFACT RISK"
#    regardless of score.
# =====================================================================

def verdict(scores, controls_passed):
    total = sum(s["score"] for s in scores.values())
    maximum = sum(s["max"] for s in scores.values())
    pct = total / maximum * 100

    if not controls_passed:
        return total, maximum, "INCONCLUSIVE — ARTIFACT RISK (controls failed)"

    if pct >= 80:
        v = "CONSISTENT WITH QUANTUM SPIN COHERENCE"
    elif pct >= 60:
        v = "STRONG EVIDENCE — recommend independent replication"
    elif pct >= 40:
        v = "SUGGESTIVE — additional data needed"
    else:
        v = "NO DETECTION"

    return total, maximum, v


# =====================================================================
#  RUN FULL PROTOCOL
# =====================================================================

def run_qdp1(system, noise=None):
    if noise is None:
        noise = Noise()

    print(f"\n  {'=' * 60}")
    print(f"  QDP-1: {system.name}")
    print(f"  {system.description}")
    print(f"  {'=' * 60}")
    print(f"  field_ratio={system.field_ratio}  photons={system.base_photons}")
    print()

    scores = {}

    # Stage 1
    print("  [1/7] BASELINE ", end="", flush=True)
    s1 = stage1(system, noise)
    scores["baseline"] = s1
    regime = "shot-limited" if s1["passed"] else "technical-limited"
    print(f"  ENR={s1['enr']:.2f}x  drift={s1['drift_pct']:.1f}%  "
          f"{regime}  [{s1['score']}/{s1['max']}]")

    # Stage 2
    print("  [2/7] DIFFERENTIAL ", end="", flush=True)
    s2 = stage2(system, noise)
    scores["differential"] = s2
    print(f"  contrast={s2['contrast']:+.6f}  Z={s2['z']:.1f}  "
          f"[{s2['score']}/{s2['max']}]")

    # Stage 3
    print("  [3/7] CONTROLS ", end="", flush=True)
    s3 = stage3(system, noise)
    scores["controls"] = s3
    status = "ALL CLEAN" if s3["all_clean"] else "CONTAMINATED"
    print(f"  {status}  [{s3['score']}/{s3['max']}]")
    for name, r in s3["controls"].items():
        flag = "  " if r["clean"] else "!!"
        print(f"    {flag} {name:<25} z={r['z']:.1f}")

    # Stage 4
    print("  [4/7] ANGULAR SHAPE ", end="", flush=True)
    s4 = stage4(system, noise)
    scores["angular"] = s4
    print(f"  cos2_power={s4['power_ratio']:.3f}  R2={s4['r2']:.3f}  "
          f"F={s4['f_stat']:.1f}  [{s4['score']}/{s4['max']}]")

    # Stage 5
    print("  [5/7] NOISE DECAY ", end="", flush=True)
    s5 = stage5(system, noise)
    scores["noise_decay"] = s5
    print(f"  {s5['shape']}  linR2={s5['lin_r2']:.3f}  "
          f"expR2={s5['exp_r2']:.3f}  [{s5['score']}/{s5['max']}]")
    for d, c in s5["data"]:
        bar = "#" * min(int(c * 2000), 35)
        print(f"      d={d:.1f}  |{bar}| {c:.6f}")

    # Stage 6
    print("  [6/7] FIELD SCALING ", end="", flush=True)
    s6 = stage6(system, noise)
    scores["field_scale"] = s6
    print(f"  {s6['interpretation']}  "
          f"{'quantum-like' if s6['quantum_like'] else 'classical-like'}  "
          f"[{s6['score']}/{s6['max']}]")
    for b, c in s6["data"]:
        bar = "#" * min(int(c * 200), 35)
        print(f"      B={b:.4f}  |{bar}| {c:.6f}")

    # Stage 7
    print("  [7/7] TEMPERATURE ", end="", flush=True)
    s7 = stage7(system, noise)
    scores["temperature"] = s7
    print(f"  rho={s7['spearman_rho']:+.3f}  "
          f"{'quantum-like' if s7['quantum_like'] else 'classical-like'}  "
          f"[{s7['score']}/{s7['max']}]")
    for dt, c in s7["data"]:
        bar = "#" * min(int(c * 2000), 35)
        print(f"      T{dt:+.0f}K  |{bar}| {c:.6f}")

    # Verdict
    total, maximum, v = verdict(scores, s3["all_clean"])
    print()
    print(f"  {'=' * 60}")
    print(f"  SCORE: {total}/{maximum} ({total/maximum*100:.0f}%)")
    print(f"  VERDICT: {v}")
    print(f"  {'=' * 60}")

    return total, maximum, v


# =====================================================================
#  MAIN
# =====================================================================

def main():
    print("=" * 64)
    print("  QDP-1: QUANTUM DETECTION PROTOCOL v1")
    print("  Formal 7-Stage Framework")
    print("=" * 64)

    systems = [
        System("Avian Cryptochrome Cry4a", 0.05, 1000,
               "Bird retina magnetoreceptor"),
        System("Flavin-Tryptophan Model", 0.05, 2000,
               "Synthetic radical pair benchmark"),
        System("Plant Cryptochrome Cry1", 0.05, 800,
               "Arabidopsis magnetosensitivity candidate"),
        System("Enzyme Radical Pair", 0.03, 500,
               "Donor-bridge-acceptor tunneling"),
        System("Rhodamine B (Negative Control)", 0.0, 1500,
               "Non-radical-pair fluorophore — expected: NO DETECTION"),
    ]

    noise = Noise()
    results = []

    for sys in systems:
        total, maximum, v = run_qdp1(sys, noise)
        results.append((sys.name, total, maximum, v))

    # Summary
    print()
    print("=" * 64)
    print("  QDP-1 SUMMARY — ALL SYSTEMS")
    print("=" * 64)
    print()
    print(f"  {'System':<30}  {'Score':>7}  {'Verdict'}")
    print(f"  {'-'*30}  {'-'*7}  {'-'*30}")
    for name, t, m, v in results:
        print(f"  {name:<30}  {t:>2}/{m:<3}  {v}")

    print()
    print("  PROTOCOL SPECIFICATION:")
    print("  Stage 1: Baseline noise characterization    (1 pt)")
    print("  Stage 2: Differential angular detection     (2 pts)")
    print("  Stage 3: Negative controls [GATE]           (2 pts)")
    print("  Stage 4: Fourier angular shape              (2 pts)")
    print("  Stage 5: Noise decay fingerprint            (1 pt)")
    print("  Stage 6: Field-strength power law           (1 pt)")
    print("  Stage 7: Temperature scaling                (1 pt)")
    print("                                             -------")
    print("                                             10 pts")
    print()
    print("  >= 8: CONSISTENT  |  >= 6: STRONG  |  >= 4: SUGGESTIVE  |  < 4: NONE")
    print("  Stage 3 is a gate: controls must pass for any positive verdict.")
    print()


if __name__ == "__main__":
    main()
