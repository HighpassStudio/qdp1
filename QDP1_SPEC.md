# QDP-1: A Multi-Stage Framework for Detecting Quantum Coherence Effects in Radical Pair Systems

## Abstract

We propose QDP-1, a detection protocol for identifying quantum spin coherence effects in radical pair systems under ambient conditions. The framework adapts zero-noise extrapolation (ZNE), a proven error-mitigation technique from quantum computing, as a diagnostic fingerprint for distinguishing coherent spin dynamics from classical behavior in biological and chemical radical pair systems. QDP-1 combines seven tests — providing partially independent lines of evidence — into a scored verdict with control gating, borrowing from particle physics discovery criteria and clinical trial methodology. No existing framework unifies these elements: ZNE-style noise scaling as a quantum biology diagnostic, Fourier angular power analysis, field-strength power-law discrimination, and temperature-dependent coherence scaling, within a single scored protocol. We validate QDP-1 in simulation across four radical pair systems and define the conditions under which each stage provides evidence for or against quantum spin coherence.

**Scope note:** QDP-1 detects signatures consistent with quantum spin coherence in radical pair systems. It does not test for entanglement specifically, nor does it address other quantum biological phenomena (coherent energy transfer, quantum tunneling) without additional stages. Stages 5, 6, and 7 are partially correlated — temperature affects decoherence rates, which in turn affect field-scaling behavior — and should not be treated as fully independent evidence.

## 1. Motivation

The radical pair mechanism is the leading candidate for biological magnetoreception and has been confirmed in cryptochrome systems (Maeda et al. 2012, Xu et al. 2021, Wedge et al. 2024). Individual detection techniques exist: fluorescence-based magnetic field effect measurement (Kerpal et al. 2019), magneto-fluorescence microspectroscopy (Lindner et al. 2024), and in vivo magnetic resonance control (Gupta et al. 2026). However, no unified protocol exists that:

1. Combines multiple partially independent lines of evidence into a single verdict
2. Uses control gating to prevent false positives from reaching publication
3. Imports noise-scaling diagnostics from quantum computing
4. Applies system-agnostically to any radical pair candidate

QDP-1 addresses this gap.

## 2. Prior Art and Novelty Claim

### Directly overlapping (established, not novel)
- Magnetic field effects on radical pair fluorescence
- Angular dependence of singlet yield
- Lorentzian B_1/2 field-strength characterization
- Temperature effects on spin coherence
- Negative controls (no field, denatured protein, radical scavenger)

### Adjacent (exists in one field, not applied to another)
- Zero-noise extrapolation: standard in quantum computing (Temme et al. 2017, Giurgica-Tiron et al. 2020), not applied to quantum biology
- Multi-stage scored verdicts: standard in particle physics and clinical diagnostics, not used in radical pair detection
- Fourier decomposition of angular response: standard in signal processing, not used as a radical pair diagnostic
- Control gating: standard in blind analysis protocols, not formalized in quantum biology

### Novel claim
QDP-1 unifies ZNE-style noise scaling, Fourier angular analysis, power-law field discrimination, and temperature coherence scaling into a control-gated, scored detection framework for quantum biology. No mainstream precedent found for this full package (search conducted across 2005-2025 literature).

## 3. The Protocol

### Stage 1: Baseline Noise Characterization (1 point)

**Purpose:** Determine whether the measurement setup is shot-noise-limited or technical-noise-limited before any signal measurement.

**Method:** Measure N pulses with no applied field. Compute:
- Mean detected counts: mu
- Measured standard deviation: sigma_meas
- Predicted shot noise: sigma_shot = sqrt(mu)
- Excess noise ratio: ENR = sigma_meas / sigma_shot

**Decision:** ENR < 1.5 passes (shot-noise-limited). ENR >= 1.5 flags technical noise dominance; subsequent stages must account for this.

**Scoring:** 1 point if passed.

### Stage 2: Differential Signal Detection (2 points)

**Purpose:** Detect angular dependence of the radical pair reaction yield using normalized differential measurement.

**Method:** Block-randomized alternation between field angle theta_A = 0 and theta_B = pi/2. For each block of 2B pulses:

    C_i = (S_A - S_B) / (S_A + S_B)

where S_A, S_B are summed photon counts at each angle. The normalized form cancels common-mode drift (LED intensity, photobleaching, detector gain).

**Statistics:**
- Mean contrast: C_bar = mean(C_i)
- Standard error: SE = std(C_i) / sqrt(N_blocks)
- Z-score: Z = |C_bar| / SE

**Decision:** Z > 5 for detection (5-sigma, matching particle physics discovery threshold).

**Scoring:** 2 points if Z > 5; 1 point if Z > 3.

### Stage 3: Negative Controls — GATE (2 points)

**Purpose:** Eliminate artifacts. This stage is a gate: if controls fail, the final verdict is capped at "INCONCLUSIVE" regardless of score.

**Controls:**
- C1: Same angle (theta_A = theta_B = 0). Tests for detector asymmetry.
- C2: No field / near-zero field. Tests for field-independent artifacts.
- C3: Killed radical pair (radical scavenger or denatured protein). Tests whether the signal requires the spin-correlated radical pair.

**Decision:** Each control must show Z < 2.0. Any control with Z > 3.0 flags artifact contamination.

**Scoring:** 2 points if all controls pass. 0 points if any control fails. Gate: failure caps verdict.

### Stage 4: Angular Shape via Fourier Decomposition (2 points)

**Purpose:** Confirm that the angular dependence follows the cos^2 pattern predicted by radical pair theory, using a method more robust than direct curve fitting.

**Method:** Measure yield at N >= 24 equally-spaced angles from 0 to pi. Compute the Fourier coefficient for the 2-theta component:

    a_2 = (2/N) * sum(y_i * cos(2 * theta_i))
    b_2 = (2/N) * sum(y_i * sin(2 * theta_i))
    P_2 = a_2^2 + b_2^2

cos^2(theta) = 0.5 + 0.5*cos(2*theta), so the radical pair signal concentrates power in the 2-theta Fourier component.

**Metrics:**
- Power ratio: P_2 / total_variance
- F-statistic: cos^2 model vs. flat model

**Decision:** Power ratio > 0.5 AND F > 10 for strong detection.

**Scoring:** 2 points if both criteria met. 1 point if either met.

### Stage 5: Noise Decay Fingerprint — ZNE Diagnostic (1 point)

**Purpose:** Distinguish quantum coherence effects from classical artifacts using the shape of signal decay under controlled decoherence.

**Method:** Deliberately increase decoherence (add paramagnetic ions, increase temperature, or reduce coherence time through chemical modification). Measure contrast at decoherence levels d = 0.0, 0.1, ..., 0.9. Fit two models:

    Linear:      C(d) = a - b*d          (R^2_lin)
    Exponential: C(d) = a * exp(-k*d)    (R^2_exp)

**Rationale:** This adapts zero-noise extrapolation (ZNE) from quantum computing. In ZNE, noise is deliberately amplified and the result extrapolated to zero noise. Here, we use the decay curve shape as a diagnostic: quantum coherence effects typically produce non-linear (exponential-like) decay under increasing decoherence, while many classical artifacts produce linear decay.

**Important caveat:** Exponential decay alone is not proof of quantum coherence. Classical processes (photobleaching, thermal relaxation) can also produce exponential decay. This stage provides supporting evidence, not standalone proof. Weight is reduced to 1 point to reflect this.

**Decision:** R^2_exp - R^2_lin > 0.1 indicates exponential (quantum-like) decay.

**Scoring:** 1 point if exponential decay detected.

### Stage 6: Field-Strength Power Law (1 point)

**Purpose:** Distinguish quantum radical pair mechanism from classical magnetic effects using the scaling of contrast with field strength.

**Method:** Measure contrast at field strengths spanning 2+ orders of magnitude (e.g., 5 to 1000 microtesla). Fit power law to weak-field regime:

    log(C) = alpha * log(B) + beta

**Rationale:**
- Quantum radical pair: contrast scales approximately linearly with B at weak fields (alpha ~ 1), saturating at B ~ hyperfine coupling
- Classical magnetic: contrast scales quadratically (alpha ~ 2)
- The Lorentzian B_1/2 characterization used in existing literature captures field dependence but requires fitting to a specific spin-chemical model. The power-law test is model-free.

**Decision:** alpha < 1.5 indicates quantum-like scaling.

**Scoring:** 1 point if quantum-like scaling detected.

### Stage 7: Temperature Coherence Scaling (1 point)

**Purpose:** Quantum spin coherence degrades with increasing temperature as thermal motion disrupts the radical pair. Classical magnetic effects typically show weaker or different temperature dependence.

**Method:** Measure contrast at temperature offsets from baseline (e.g., -10K to +30K). Compute Spearman rank correlation between temperature and contrast magnitude.

**Rationale:** Quantum coherence: contrast should decrease monotonically with increasing temperature (negative correlation). Classical artifact: no systematic temperature dependence, or dependence that doesn't match radical pair decoherence predictions.

**Decision:** Spearman rho < -0.5 indicates quantum-like thermal scaling.

**Scoring:** 1 point if significant negative correlation detected.

## 4. Scoring and Verdict

| Stage | Test | Max Points |
|-------|------|------------|
| 1 | Baseline noise quality | 1 |
| 2 | Differential signal detection | 2 |
| 3 | Negative controls (GATE) | 2 |
| 4 | Fourier angular shape | 2 |
| 5 | Noise decay fingerprint (ZNE) | 1 |
| 6 | Field power law | 1 |
| 7 | Temperature scaling | 1 |
| | **Total** | **10** |

### Verdict thresholds:
- **>= 8/10:** CONSISTENT WITH QUANTUM SPIN COHERENCE
- **>= 6/10:** STRONG EVIDENCE — recommend independent replication
- **>= 4/10:** SUGGESTIVE — needs additional data
- **< 4/10:** NO DETECTION

### Independence note:
Stages 1-4 provide substantially independent evidence (noise quality, signal detection, artifact elimination, and angular shape test different properties). Stages 5-7 are partially correlated: temperature (Stage 7) affects decoherence rates (Stage 5), and decoherence affects field-scaling behavior (Stage 6). The scoring weights reflect this: Stages 1-4 carry 7 of 10 points, while the correlated Stages 5-7 carry 3 points combined.

### Critical gate:
Stage 3 (Controls) must pass for any positive verdict. If controls fail, the verdict is capped at "INCONCLUSIVE — ARTIFACT RISK" regardless of total score.

## 5. Validation

QDP-1 was validated in simulation across four systems:

| System | Score | Verdict |
|--------|-------|---------|
| Avian Cryptochrome Cry4a | 7/10 | STRONG EVIDENCE |
| Flavin-Tryptophan Model | 5/10 | SUGGESTIVE |
| Plant Cryptochrome Cry1 | 5/10 | INCONCLUSIVE (control gate) |
| Enzyme Radical Pair | 7/10 | STRONG EVIDENCE |

The control gate correctly caught a noisy run in the Cry1 system (one control at Z=2.5), demonstrating the framework's self-validation capability.

Simulation limitations: Stages 5 and 7 are constrained by the simplified decoherence model used (linear field-ratio reduction as proxy for decoherence). Real experimental validation would use physical decoherence mechanisms (paramagnetic quenchers, temperature variation), which may produce different decay shapes.

## 6. Application

QDP-1 is designed as a reusable detection kit. To apply it to a new system, define:

1. **Excitation wavelength** (what creates the radical pair)
2. **Field ratio** (applied field / hyperfine coupling)
3. **Detected photons per pulse** (fluorescence yield)
4. **Observable** (fluorescence intensity, transient absorption, etc.)

The protocol runs identically regardless of the specific system. Each application to a new radical pair candidate constitutes an independent experimental contribution.

### Priority targets for experimental application:
1. Avian Cryptochrome Cry4a (strongest existing evidence)
2. Synthetic flavin-tryptophan model compounds (controlled benchmark)
3. Plant cryptochromes (less studied, potential magnetosensitivity)
4. Enzyme radical pairs (donor-bridge-acceptor systems)

## 7. Limitations and Future Work

1. **Simulation vs. experiment:** QDP-1 is validated in simulation only. Experimental validation is needed.
2. **Decoherence model:** The ZNE diagnostic (Stage 5) requires validation with physical decoherence mechanisms, not proxy models.
3. **Scoring weights:** Current weights are based on methodological reasoning, not empirical calibration. Validation against known positive and negative systems would refine weights.
4. **Scope:** QDP-1 is designed for radical pair systems specifically. Extension to other quantum biology phenomena (coherent energy transfer, quantum tunneling) would require additional stages.
5. **Exponential decay caveat:** Stage 5 must not be overinterpreted. Exponential decay is necessary but not sufficient for quantum coherence. The multi-stage framework mitigates this risk.
