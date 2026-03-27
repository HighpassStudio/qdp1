"""
Radical Pair Detection Experiment — Full Protocol
===================================================

A complete, executable experiment design for detecting
quantum entanglement in radical pair systems at room temperature.

Three sections:
  WHAT  — equipment, materials, setup
  HOW   — step-by-step protocol with controls
  WHY   — what each step proves and what could go wrong

Then: simulation of the full experiment including
      controls, confounds, and statistical analysis.

Run it:  python radical_pair_experiment.py
"""

import math
import random


# =====================================================================
#  EXPERIMENTAL PARAMETERS
# =====================================================================

# Magnetic field
EARTH_FIELD_UT = 50.0          # Earth's field (microtesla)
APPLIED_FIELD_UT = 50.0        # match Earth's field for relevance
HYPERFINE_MT = 1.0             # millitesla
FIELD_RATIO = APPLIED_FIELD_UT / 1000.0 / HYPERFINE_MT

# Measurement
ANGLES_PER_SWEEP = 36          # every 10 degrees
MOLECULES_PER_MEASUREMENT = 1  # single-molecule level
SWEEPS_PER_CONDITION = 500     # repeat sweeps for statistics

# Noise parameters (realistic lab)
DETECTOR_NOISE = 0.02          # 2% detector error
FIELD_INHOMOGENEITY = 0.03     # 3% field non-uniformity
SAMPLE_DEGRADATION = 0.01      # 1% per hour


# =====================================================================
#  PHYSICS ENGINE (same core as radical_pair.py)
# =====================================================================

def singlet_yield(theta, field_ratio, decoherence=0.0):
    """Singlet yield at angle theta with decoherence."""
    b_eff = field_ratio * math.cos(theta)
    omega = 2 * math.pi * b_eff
    rate = 1.0 + decoherence
    return 0.25 + 0.25 * (rate ** 2) / (rate ** 2 + omega ** 2)


def measure_yield(theta, field_ratio, decoherence=0.0,
                  detector_noise=0.0, field_noise=0.0):
    """Single measurement with realistic noise sources."""
    # Field inhomogeneity: actual angle varies slightly
    actual_theta = theta + random.gauss(0, field_noise)

    # Field strength fluctuation
    actual_field = field_ratio * (1 + random.gauss(0, field_noise))

    # True quantum yield
    true_yield = singlet_yield(actual_theta, actual_field, decoherence)

    # Binary outcome (singlet or triplet)
    result = 1 if random.random() < true_yield else 0

    # Detector can misread
    if random.random() < detector_noise:
        result = 1 - result

    return result


def classical_yield(theta, field_ratio):
    """Classical prediction — essentially flat."""
    effect = 0.5 * (field_ratio ** 2)
    return 0.5 + effect * math.cos(theta) ** 2


# =====================================================================
#  CONTROL CONDITIONS
# =====================================================================

def run_condition(name, field_ratio, decoherence, detector_noise,
                  field_noise, num_angles, num_sweeps, scramble_field=False,
                  kill_entanglement=False):
    """
    Run one experimental condition and return results.

    Controls:
      scramble_field:     randomize field direction each measurement
                          (should destroy angular dependence)
      kill_entanglement:  add massive decoherence
                          (simulates chemically disrupted entanglement)
    """
    angle_step = math.pi / num_angles
    results = {}

    for i in range(num_angles):
        theta = i * angle_step
        deg = math.degrees(theta)
        measurements = []

        for _ in range(num_sweeps):
            if scramble_field:
                # Control: random field angle each time
                actual_theta = random.uniform(0, math.pi)
            else:
                actual_theta = theta

            d = 0.99 if kill_entanglement else decoherence

            m = measure_yield(actual_theta, field_ratio, d,
                              detector_noise, field_noise)
            measurements.append(m)

        avg = sum(measurements) / len(measurements)
        std = math.sqrt(sum((x - avg) ** 2 for x in measurements) / len(measurements))
        se = std / math.sqrt(len(measurements))

        results[deg] = {
            "mean": avg,
            "std": std,
            "se": se,
            "n": len(measurements),
        }

    return results


def angular_contrast(results):
    """Max - min yield across angles."""
    yields = [r["mean"] for r in results.values()]
    return max(yields) - min(yields)


def fit_cos2(results):
    """
    Test if data fits cos^2 pattern (quantum) vs flat (classical).

    Returns:
      amplitude:  strength of cos^2 component
      r_squared:  goodness of fit (1.0 = perfect cos^2)
      f_stat:     F-statistic for cos^2 vs flat model
    """
    angles = sorted(results.keys())
    yields = [results[a]["mean"] for a in angles]
    n = len(yields)

    # Mean yield
    y_mean = sum(yields) / n

    # cos^2 fit: y = a + b * cos^2(theta)
    # Compute via least squares
    cos2_vals = [math.cos(math.radians(a)) ** 2 for a in angles]
    cos2_mean = sum(cos2_vals) / n

    numerator = sum((cos2_vals[i] - cos2_mean) * (yields[i] - y_mean) for i in range(n))
    denominator = sum((cos2_vals[i] - cos2_mean) ** 2 for i in range(n))

    if denominator == 0:
        return 0, 0, 0

    b = numerator / denominator  # slope
    a = y_mean - b * cos2_mean   # intercept

    # R-squared
    ss_res = sum((yields[i] - (a + b * cos2_vals[i])) ** 2 for i in range(n))
    ss_tot = sum((yields[i] - y_mean) ** 2 for i in range(n))

    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    # F-statistic: is cos^2 model significantly better than flat?
    ms_model = (ss_tot - ss_res)  # improvement from adding cos^2
    ms_resid = ss_res / (n - 2) if n > 2 else 1
    f_stat = ms_model / ms_resid if ms_resid > 0 else 0

    return b, r_squared, f_stat


def significance_test(results_exp, results_ctrl):
    """
    Compare experimental vs control condition.

    Uses the angular contrast difference and its uncertainty
    to compute a z-score.
    """
    exp_contrast = angular_contrast(results_exp)
    ctrl_contrast = angular_contrast(results_ctrl)

    # Uncertainty in contrast (propagated from endpoint SEs)
    exp_yields = [(a, r["mean"], r["se"]) for a, r in results_exp.items()]
    ctrl_yields = [(a, r["mean"], r["se"]) for a, r in results_ctrl.items()]

    exp_max = max(exp_yields, key=lambda x: x[1])
    exp_min = min(exp_yields, key=lambda x: x[1])
    ctrl_max = max(ctrl_yields, key=lambda x: x[1])
    ctrl_min = min(ctrl_yields, key=lambda x: x[1])

    exp_se = math.sqrt(exp_max[2] ** 2 + exp_min[2] ** 2)
    ctrl_se = math.sqrt(ctrl_max[2] ** 2 + ctrl_min[2] ** 2)

    diff = exp_contrast - ctrl_contrast
    diff_se = math.sqrt(exp_se ** 2 + ctrl_se ** 2)

    z = diff / diff_se if diff_se > 0 else 0

    return diff, z


# =====================================================================
#  THE FULL EXPERIMENT
# =====================================================================

def main():
    num_angles = 18
    num_sweeps = 1000

    print("=" * 72)
    print("  RADICAL PAIR EXPERIMENT — FULL PROTOCOL")
    print("=" * 72)
    print()

    # ── WHAT ──────────────────────────────────────────────────────
    print("=" * 72)
    print("  SECTION 1: WHAT — Equipment and Materials")
    print("=" * 72)
    print()
    print("  MATERIALS:")
    print("    1. Cryptochrome protein (Cry1 or Cry4)")
    print("       - Source: recombinant expression or commercial supplier")
    print("       - Cry4 preferred (found in bird retina, magnetically sensitive)")
    print("       - Dissolved in pH 7.4 phosphate buffer")
    print("       - Concentration: ~10-50 uM")
    print("       - Cost: ~$200-500 for purified protein")
    print()
    print("    2. FAD cofactor (flavin adenine dinucleotide)")
    print("       - Already bound in cryptochrome")
    print("       - This is what absorbs blue light and creates the radical pair")
    print()
    print("  EQUIPMENT:")
    print("    3. Blue LED (450nm)")
    print("       - Excites FAD -> creates radical pair")
    print("       - Pulsed: 10ns pulses (so you know when pair is created)")
    print("       - Cost: $20-50 for laser diode, $2 for basic LED")
    print()
    print("    4. Helmholtz coil pair")
    print("       - Generates uniform magnetic field (50 uT, Earth-strength)")
    print("       - Must be rotatable OR use 3-axis coils")
    print("       - Uniformity: better than 1% over sample volume")
    print("       - Cost: ~$200 DIY, ~$2000 commercial")
    print()
    print("    5. Mu-metal magnetic shield")
    print("       - Blocks Earth's field so you control the only field")
    print("       - Without this, Earth's field adds uncontrolled background")
    print("       - Cost: ~$500-1000")
    print()
    print("    6. Fluorescence detector")
    print("       - Measures singlet yield via fluorescence")
    print("       - Singlet radical pairs -> fluorescent product")
    print("       - Triplet radical pairs -> non-fluorescent product")
    print("       - Photodiode + bandpass filter (detect emission, block excitation)")
    print("       - Cost: ~$500 for PMT or good photodiode setup")
    print()
    print("    7. Data acquisition")
    print("       - Arduino/RPi + ADC for photon counting")
    print("       - Time-stamp each measurement")
    print("       - Cost: ~$50-100")
    print()
    print("  TOTAL ESTIMATED COST: $1,500 - $4,000")
    print("  (Lower end: DIY coils + basic LED + used PMT)")
    print("  (Upper end: commercial coils + pulsed laser + new PMT)")
    print()

    # ── HOW ───────────────────────────────────────────────────────
    print("=" * 72)
    print("  SECTION 2: HOW — Step-by-Step Protocol")
    print("=" * 72)
    print()
    print("  PREPARATION:")
    print("    Step 0: Zero the field")
    print("      - Place sample inside mu-metal shield")
    print("      - Use gaussmeter to verify < 1 uT residual field")
    print("      - This is your baseline: zero field = no compass signal")
    print()
    print("  THE EXPERIMENT (5 conditions):")
    print()
    print("  Condition A: QUANTUM TEST (the actual experiment)")
    print("    - Apply 50 uT field via Helmholtz coils")
    print("    - Rotate field in 10-degree steps (0 to 180 degrees)")
    print("    - At each angle: pulse blue light, measure fluorescence")
    print("    - Record: (angle, fluorescence_intensity, timestamp)")
    print("    - Repeat 1000x per angle")
    print("    - PREDICTION: cos^2 pattern in fluorescence vs angle")
    print()
    print("  Condition B: CONTROL 1 — No field")
    print("    - Same protocol, but Helmholtz coils OFF")
    print("    - Only residual field (< 1 uT)")
    print("    - PREDICTION: flat line (no angular dependence)")
    print("    - WHY: proves the signal comes from YOUR applied field")
    print()
    print("  Condition C: CONTROL 2 — Scrambled field")
    print("    - Field ON at 50 uT, but direction RANDOMIZED each pulse")
    print("    - Proves angular dependence isn't a detector artifact")
    print("    - PREDICTION: flat line")
    print("    - WHY: same field strength, no consistent direction = no pattern")
    print()
    print("  Condition D: CONTROL 3 — Killed entanglement")
    print("    - Add scavenger molecule (e.g., ascorbic acid)")
    print("    - Scavenger reacts with one radical before S-T mixing occurs")
    print("    - Same field, same angles, same protein")
    print("    - PREDICTION: flat line (no angular dependence)")
    print("    - WHY: proves the signal requires the radical PAIR")
    print("           (not just single-radical magnetic effects)")
    print()
    print("  Condition E: CONTROL 4 — Strong field")
    print("    - Apply 1000 uT (20x Earth) at same angles")
    print("    - PREDICTION: angular dependence EXISTS but weaker contrast")
    print("    - WHY: at strong fields, classical effects also appear")
    print("           quantum advantage is specifically at WEAK fields")
    print("           seeing the contrast DECREASE at strong fields")
    print("           confirms the quantum mechanism")
    print()
    print("  CONFOUNDING VARIABLES TO ELIMINATE:")
    print()
    print("    C1: Photobleaching")
    print("      - Problem: protein degrades under blue light over time")
    print("      - Solution: randomize angle order (don't always go 0->180)")
    print("      - Solution: fresh sample every 2 hours")
    print("      - Solution: monitor total fluorescence for decay trend")
    print()
    print("    C2: Temperature drift")
    print("      - Problem: reaction rates change with temperature")
    print("      - Solution: temperature-controlled sample holder (310K)")
    print("      - Solution: log temperature with each measurement")
    print()
    print("    C3: Solvent effects")
    print("      - Problem: buffer composition affects radical lifetime")
    print("      - Solution: same buffer for all conditions")
    print("      - Solution: degas buffer (oxygen quenches triplets)")
    print()
    print("    C4: Detector orientation")
    print("      - Problem: rotating field might move detector alignment")
    print("      - Solution: rotate SAMPLE, not field")
    print("      - Solution: OR use 3-axis coils (electronic rotation)")
    print()
    print("    C5: Earth's field leakage")
    print("      - Problem: mu-metal shield isn't perfect")
    print("      - Solution: measure residual field at start/end")
    print("      - Solution: run Condition B to quantify baseline")
    print()

    # ── WHY (run the simulation) ──────────────────────────────────
    print("=" * 72)
    print("  SECTION 3: WHY — Simulated Results and Analysis")
    print("=" * 72)
    print()

    print("  Running all 5 conditions...")
    print()

    # Condition A: Quantum test
    print("  --- Condition A: QUANTUM TEST (50 uT, cryptochrome) ---")
    results_a = run_condition(
        "Quantum", FIELD_RATIO, decoherence=0.0,
        detector_noise=DETECTOR_NOISE, field_noise=FIELD_INHOMOGENEITY,
        num_angles=num_angles, num_sweeps=num_sweeps
    )
    contrast_a = angular_contrast(results_a)
    amp_a, r2_a, f_a = fit_cos2(results_a)
    print(f"    Angular contrast: {contrast_a:.6f}")
    print(f"    cos^2 amplitude:  {amp_a:.6f}")
    print(f"    R-squared:        {r2_a:.4f}")
    print(f"    F-statistic:      {f_a:.2f}")
    print()

    # Condition B: No field
    print("  --- Condition B: CONTROL — No field ---")
    results_b = run_condition(
        "No field", FIELD_RATIO * 0.01, decoherence=0.0,
        detector_noise=DETECTOR_NOISE, field_noise=FIELD_INHOMOGENEITY,
        num_angles=num_angles, num_sweeps=num_sweeps
    )
    contrast_b = angular_contrast(results_b)
    amp_b, r2_b, f_b = fit_cos2(results_b)
    print(f"    Angular contrast: {contrast_b:.6f}")
    print(f"    cos^2 amplitude:  {amp_b:.6f}")
    print(f"    R-squared:        {r2_b:.4f}")
    print(f"    F-statistic:      {f_b:.2f}")
    print()

    # Condition C: Scrambled field
    print("  --- Condition C: CONTROL — Scrambled field ---")
    results_c = run_condition(
        "Scrambled", FIELD_RATIO, decoherence=0.0,
        detector_noise=DETECTOR_NOISE, field_noise=FIELD_INHOMOGENEITY,
        num_angles=num_angles, num_sweeps=num_sweeps,
        scramble_field=True
    )
    contrast_c = angular_contrast(results_c)
    amp_c, r2_c, f_c = fit_cos2(results_c)
    print(f"    Angular contrast: {contrast_c:.6f}")
    print(f"    cos^2 amplitude:  {amp_c:.6f}")
    print(f"    R-squared:        {r2_c:.4f}")
    print(f"    F-statistic:      {f_c:.2f}")
    print()

    # Condition D: Killed entanglement
    print("  --- Condition D: CONTROL — Entanglement killed ---")
    results_d = run_condition(
        "Killed", FIELD_RATIO, decoherence=0.0,
        detector_noise=DETECTOR_NOISE, field_noise=FIELD_INHOMOGENEITY,
        num_angles=num_angles, num_sweeps=num_sweeps,
        kill_entanglement=True
    )
    contrast_d = angular_contrast(results_d)
    amp_d, r2_d, f_d = fit_cos2(results_d)
    print(f"    Angular contrast: {contrast_d:.6f}")
    print(f"    cos^2 amplitude:  {amp_d:.6f}")
    print(f"    R-squared:        {r2_d:.4f}")
    print(f"    F-statistic:      {f_d:.2f}")
    print()

    # Condition E: Strong field
    print("  --- Condition E: CONTROL — Strong field (1000 uT) ---")
    strong_ratio = 1000.0 / 1000.0 / HYPERFINE_MT
    results_e = run_condition(
        "Strong", strong_ratio, decoherence=0.0,
        detector_noise=DETECTOR_NOISE, field_noise=FIELD_INHOMOGENEITY,
        num_angles=num_angles, num_sweeps=num_sweeps
    )
    contrast_e = angular_contrast(results_e)
    amp_e, r2_e, f_e = fit_cos2(results_e)
    print(f"    Angular contrast: {contrast_e:.6f}")
    print(f"    cos^2 amplitude:  {amp_e:.6f}")
    print(f"    R-squared:        {r2_e:.4f}")
    print(f"    F-statistic:      {f_e:.2f}")
    print()

    # ── COMPARISON TABLE ──────────────────────────────────────────
    print("  --- RESULTS COMPARISON ---")
    print()
    print(f"  {'Condition':<35} {'Contrast':>10} {'cos2 R^2':>10} {'F-stat':>10}")
    print(f"  {'---------':<35} {'--------':>10} {'--------':>10} {'------':>10}")

    conditions = [
        ("A: Quantum (50 uT)", contrast_a, r2_a, f_a),
        ("B: No field (control)", contrast_b, r2_b, f_b),
        ("C: Scrambled field (control)", contrast_c, r2_c, f_c),
        ("D: Entanglement killed (control)", contrast_d, r2_d, f_d),
        ("E: Strong field (1000 uT)", contrast_e, r2_e, f_e),
    ]

    for name, contrast, r2, f in conditions:
        print(f"  {name:<35} {contrast:>10.6f} {r2:>10.4f} {f:>10.2f}")

    print()

    # ── STATISTICAL TESTS ─────────────────────────────────────────
    print("  --- STATISTICAL SIGNIFICANCE ---")
    print()
    print("  Comparing Condition A (quantum) against each control:")
    print()

    for ctrl_name, ctrl_results in [
        ("B (no field)", results_b),
        ("C (scrambled)", results_c),
        ("D (killed)", results_d),
    ]:
        diff, z = significance_test(results_a, ctrl_results)
        if z > 5:
            verdict = "SIGNIFICANT (5-sigma)"
        elif z > 3:
            verdict = "EVIDENCE (3-sigma)"
        elif z > 2:
            verdict = "SUGGESTIVE"
        else:
            verdict = "NOT SIGNIFICANT"

        print(f"    A vs {ctrl_name:<20}  diff={diff:+.6f}  z={z:.2f}  {verdict}")

    print()

    # ── DATA ANALYSIS PIPELINE ────────────────────────────────────
    print("=" * 72)
    print("  SECTION 4: DATA ANALYSIS PIPELINE")
    print("=" * 72)
    print()
    print("  After collecting data, run these analyses in order:")
    print()
    print("  STEP 1: QUALITY CHECKS")
    print("    - Plot total fluorescence vs time (detect photobleaching)")
    print("    - Plot temperature vs time (detect drift)")
    print("    - Remove outliers (> 3 sigma from local mean)")
    print("    - Verify angle randomization worked (no order effects)")
    print()
    print("  STEP 2: ANGULAR DEPENDENCE")
    print("    - Plot yield vs angle for each condition")
    print("    - Fit cos^2 model to each")
    print("    - Compare: does Condition A show cos^2 while controls don't?")
    print("    - Report: amplitude, R^2, F-statistic for each")
    print()
    print("  STEP 3: QUANTUM vs CLASSICAL DISCRIMINATION")
    print("    - The KEY test: angle dependence at WEAK fields")
    print("    - Classical: contrast proportional to B^2 (negligible at 50 uT)")
    print("    - Quantum:   contrast proportional to B (detectable at 50 uT)")
    print("    - Measure contrast at 5, 10, 25, 50, 100, 500, 1000 uT")
    print("    - Plot contrast vs field strength")
    print("    - Quantum: linear rise then saturation")
    print("    - Classical: quadratic rise (much weaker at low fields)")
    print()
    print("  STEP 4: NOISE EXTRAPOLATION (your insight)")
    print("    - Add controlled decoherence (vary temperature or add paramagnetic ions)")
    print("    - Measure contrast at each decoherence level")
    print("    - Quantum prediction: exponential decay (1-d)^2")
    print("    - Classical prediction: linear decay or flat")
    print("    - The SHAPE of the decay curve is the fingerprint")
    print()
    print("  STEP 5: PUBLICATION CRITERIA")
    print("    - Condition A shows cos^2 pattern (R^2 > 0.8)")
    print("    - All controls show flat (R^2 < 0.1)")
    print("    - A vs each control: z > 5 (5-sigma)")
    print("    - Contrast vs field strength: fits quantum model, not classical")
    print("    - Noise extrapolation: exponential decay confirmed")
    print("    - Results reproducible across 3+ independent preparations")
    print()

    # ── FIELD STRENGTH SWEEP ──────────────────────────────────────
    print("  --- STEP 3 SIMULATION: Contrast vs Field Strength ---")
    print()
    print(f"  {'Field (uT)':>12}  {'Q Contrast':>12}  {'C Contrast':>12}  {'Ratio':>8}  {'Scaling':>12}")
    print(f"  {'----------':>12}  {'----------':>12}  {'----------':>12}  {'-----':>8}  {'-------':>12}")

    prev_q, prev_c = None, None
    for field_uT in [5, 10, 25, 50, 100, 250, 500, 1000]:
        ratio = field_uT / 1000.0 / HYPERFINE_MT
        res = run_condition(
            "", ratio, 0.0, DETECTOR_NOISE, FIELD_INHOMOGENEITY,
            num_angles=10, num_sweeps=300
        )
        qc = angular_contrast(res)

        # Classical contrast
        c_yields = [classical_yield(math.radians(a), ratio)
                     for a in sorted(res.keys())]
        cc = max(c_yields) - min(c_yields)

        qc_ratio = qc / cc if cc > 1e-10 else float('inf')

        # Detect scaling: linear (quantum) vs quadratic (classical)
        if prev_q is not None and field_uT > 5:
            field_jump = field_uT / prev_field
            q_jump = qc / prev_q if prev_q > 1e-10 else 0
            if q_jump > 0:
                scaling = f"~B^{math.log(q_jump)/math.log(field_jump):.1f}"
            else:
                scaling = "n/a"
        else:
            scaling = ""

        print(f"  {field_uT:>12}  {qc:>12.6f}  {cc:>12.8f}  {qc_ratio:>7.0f}x  {scaling:>12}")
        prev_q, prev_c, prev_field = qc, cc, field_uT

    print()
    print("  Expected: quantum scales as ~B^1 at low fields (linear)")
    print("  Expected: classical scales as ~B^2 at low fields (quadratic)")
    print("  At 50 uT, quantum is ~18x stronger than classical")
    print()

    # ── WHAT MAKES THIS PUBLISHABLE ──────────────────────────────
    print("=" * 72)
    print("  SECTION 5: WHAT MAKES THIS PUBLISHABLE")
    print("=" * 72)
    print()
    print("  A publishable result requires ALL of these:")
    print()
    print("  [1] POSITIVE RESULT:")
    print("      Condition A shows statistically significant cos^2 pattern")
    print("      at Earth-strength field (50 uT)")
    print()
    print("  [2] NEGATIVE CONTROLS:")
    print("      All 3 controls (B, C, D) show NO angular dependence")
    print("      This eliminates: detector artifacts, field artifacts,")
    print("      single-radical effects")
    print()
    print("  [3] FIELD SCALING:")
    print("      Contrast scales linearly with B (not quadratically)")
    print("      This distinguishes quantum from classical mechanism")
    print()
    print("  [4] NOISE RESPONSE:")
    print("      Signal decays exponentially with added decoherence")
    print("      This confirms quantum coherence, not classical correlation")
    print()
    print("  [5] REPRODUCIBILITY:")
    print("      Same result with independent protein preparations")
    print("      Same result on different days")
    print("      Same result with different field generation methods")
    print()
    print("  WHERE TO PUBLISH:")
    print("    - Journal of Chemical Physics (if mechanism-focused)")
    print("    - PNAS (if broader biological implications)")
    print("    - Physical Review Letters (if novel quantum detection method)")
    print("    - Nature Communications (if bird navigation angle)")
    print()
    print("  WHAT WOULD BE NOVEL:")
    print("    Not the radical pair effect itself (known since 2000s)")
    print("    But: systematic quantum detection protocol applied to it")
    print("    The noise extrapolation method as a general quantum biomarker")
    print("    The field-scaling test as quantum vs classical discriminator")
    print()


if __name__ == "__main__":
    main()
