# QDP-1: A Multi-Stage Framework for Detecting Quantum Spin Coherence in Radical Pair Systems

**Brad Loomis, MS, PE, PTOE**
Independent Research

---

## Abstract

We propose QDP-1, an eight-stage detection protocol for identifying quantum spin coherence effects in radical pair systems under ambient conditions. The framework formalizes established radical pair diagnostics (angular dependence, field-strength scaling, temperature sensitivity, RF disruption, negative controls) into a single reproducible scored protocol with explicit control gating. Every individual test is well-established in the spin chemistry literature; the contribution is standardization, not new measurement physics. The protocol also proposes adapting the principle of deliberate noise amplification from zero-noise extrapolation (ZNE) in quantum computing as a decoherence decay diagnostic, though this component requires experimental validation to determine whether the non-linear regime is practically accessible. We validate QDP-1 in simulation (Stages 1--7) across four radical pair candidate systems and one known-negative control (a non-radical-pair fluorophore), demonstrating that the protocol differentiates between systems and that the control gate correctly caps verdicts when artifact contamination is present. Stage 5 (decoherence decay shape) scores 0/1 for all systems in simulation, consistent with the theoretical prediction that Lorentzian and linear decay converge in the small-perturbation regime. Stage 8 (RF disruption) is not simulated and requires experimental validation. To our knowledge, no existing protocol in the quantum biology literature combines these tests into a single scored, system-agnostic framework with control gating, though the individual components are standard. QDP-1 is validated in simulation only; experimental validation is needed.

**Keywords:** radical pair mechanism, quantum biology, zero-noise extrapolation, magnetoreception, detection protocol, spin coherence

**Code availability:** Simulation code is available at https://github.com/HighpassStudio/qdp1

---

## 1. Introduction

The radical pair mechanism is the leading candidate explanation for biological magnetoreception and has been confirmed in cryptochrome systems through fluorescence-detected magnetic field effects [1] and Earth-strength magnetic sensitivity in tightly bound radical pairs [2]. Experimental techniques for detecting radical pair quantum effects have matured considerably: magneto-fluorescence fluctuation microspectroscopy enables investigation of quantum effects in biology at the single-molecule scale [3], and sensing magnetic-field effects at the scale of small molecular ensembles is now achievable [4].

Despite this progress, the field lacks a unified detection framework. Individual techniques -- fluorescence-based magnetic field effect measurement, angular dependence characterization, B_1/2 field-strength analysis, temperature-dependent coherence studies -- are applied independently and evaluated by different criteria across different laboratories. This creates several problems:

1. **No standard for sufficiency.** How many positive indicators constitute evidence for quantum spin coherence? There is no consensus threshold analogous to the 5-sigma standard in particle physics.

2. **No control gating.** Negative controls are used, but there is no formal mechanism to prevent false positives from propagating when controls show contamination.

3. **No cross-disciplinary diagnostic transfer.** Zero-noise extrapolation (ZNE), a technique developed for quantum computing error mitigation [5,6], provides a natural framework for probing quantum coherence effects through deliberate noise scaling. This approach has begun migrating from quantum computing into quantum sensing [7] but has not been applied to quantum biology or radical pair systems.

4. **No system-agnostic protocol.** Each new radical pair candidate is evaluated with ad hoc methods. A reusable detection kit would accelerate the field.

QDP-1 addresses these gaps by combining eight partially independent tests into a scored verdict with explicit control gating. The protocol is designed to be applied identically to any radical pair system, with each application constituting an independent experimental contribution. This work is intended as a starting point for community evaluation and refinement.

### Scope

QDP-1 detects signatures *consistent with* quantum spin coherence in radical pair systems. It does not test for entanglement specifically, nor does it address other quantum biological phenomena (coherent energy transfer, quantum tunneling) without additional stages. The framework provides evidence grades, not binary proof.

---

## 2. Related Work

### 2.1 Radical Pair Detection Methods

The radical pair mechanism and its role in biological magnetoreception have been extensively reviewed [8,9,17]. Key experimental milestones include the detection of magnetic field effects on cryptochrome fluorescence [1], characterization of angular dependence in singlet yield [10], measurement of B_1/2 parameters for field-strength characterization [11], and investigation of temperature effects on spin coherence [12]. These techniques are individually well-established and are not claimed as novel contributions of this work.

### 2.2 Zero-Noise Extrapolation in Quantum Computing

ZNE was introduced as an error-mitigation technique for near-term quantum computers [5,6]. The core idea is to deliberately amplify noise, measure the observable at multiple noise levels, and extrapolate to the zero-noise limit. ZNE is now standard practice in quantum computing and has begun migrating into quantum sensing -- notably, a 2024 study applied ZNE-style extrapolation to mitigate errors in DC magnetometry [7]. However, the use of ZNE as a *diagnostic* (to distinguish quantum from classical behavior based on decay curve shape) rather than as an error-mitigation tool, and its application to biological or chemical radical pair systems, does not appear in the mainstream literature.

### 2.3 The Quantum Biology Detection Gap

The question "How quantum is radical pair magnetoreception?" has been addressed theoretically [13], establishing that radical pair magnetoreception satisfies formal criteria for quantum behavior from a quantum information perspective. However, this assessment is conceptual, not operational -- it does not provide a staged detection protocol for experimental use.

The most relevant methodological advances are the 2024 magneto-fluorescence fluctuation microspectroscopy technique [3] and the 2019 study on sensing magnetic-field effects at small ensemble scales [4]. Both move toward reusable measurement methodology for quantum biology, but neither constitutes a multi-stage scored framework with control gating and cross-disciplinary diagnostic integration.

A 2024 study on simulating spin biology using a digital quantum computer [14] represents the most direct bridge between quantum computing and quantum biology in the existing literature. However, the connection there is different: the paper uses extrapolation ideas akin to ZNE for simulation accuracy, not as an experimental diagnostic for biological systems.

### 2.4 Contribution

QDP-1 formalizes existing radical pair diagnostics (angular dependence, field-strength scaling, temperature sensitivity, RF disruption, negative controls) into a reproducible scored protocol with explicit control gating. Every individual test in the protocol is well-established in the spin chemistry literature; the contribution is standardization, not new measurement physics. The decoherence decay diagnostic (Stage 5) applies the principle of deliberate noise amplification from quantum computing to biological radical pair systems, which does not appear in the mainstream literature, but remains a speculative proposal requiring experimental validation.

---

## 3. Methods: The QDP-1 Protocol

QDP-1 consists of seven stages, each contributing a weighted score to a final verdict. Stage 3 (negative controls) serves as a gate: if controls fail, the final verdict is capped regardless of total score. The protocol requires a fluorescence-based readout of radical pair reaction yield as a function of applied magnetic field angle and strength.

### 3.1 Stage 1: Baseline Noise Characterization (1 point)

**Purpose.** Determine whether the measurement setup is shot-noise-limited before signal measurement begins.

**Method.** Measure *N* fluorescence pulses with no applied magnetic field. Compute:

- Mean detected counts: μ
- Measured standard deviation: σ_meas
- Predicted shot noise: σ_shot = √μ
- Excess noise ratio: ENR = σ_meas / σ_shot

**Decision.** ENR < 1.5 passes (shot-noise-limited). ENR ≥ 1.5 flags technical noise dominance; subsequent stage interpretations must account for reduced sensitivity.

**Scoring.** 1 point if passed.

### 3.2 Stage 2: Differential Signal Detection (2 points)

**Purpose.** Detect angular dependence of radical pair yield using normalized differential measurement that cancels common-mode drift.

**Method.** Block-randomized alternation between field angle θ_A = 0 and θ_B = π/2. For each block of 2B pulses:

    C_i = (S_A − S_B) / (S_A + S_B)

where S_A, S_B are summed photon counts at each angle. The normalized form cancels common-mode drift (LED intensity variation, photobleaching, detector gain drift).

**Statistics.**
- Mean contrast: C̄ = mean(C_i)
- Standard error: SE = std(C_i) / √N_blocks
- Z-score: Z = |C̄| / SE

**Decision.** Z > 5 for detection (5-sigma, matching the particle physics discovery threshold). Z > 3 for evidence.

**Scoring.** 2 points if Z > 5; 1 point if Z > 3.

### 3.3 Stage 3: Negative Controls -- GATE (2 points)

**Purpose.** Eliminate artifacts. This stage is a gate: if controls fail, the final verdict is capped at "INCONCLUSIVE" regardless of total score.

**Controls.**
- C1: Same angle (θ_A = θ_B = 0). Tests for detector asymmetry or systematic bias unrelated to magnetic field angle.
- C2: No applied field / near-zero field. Tests for field-independent artifacts in the optical detection pathway.
- C3: Killed radical pair (radical scavenger addition or denatured protein). Tests whether the signal requires the spin-correlated radical pair.

**Decision.** Each control must show Z < 2.0 (pass). 2.0 <= Z <= 3.0 is indeterminate: the control neither passes nor fails, but the stage scores 1 point instead of 2 and the run should be flagged for replication. Z > 3.0 is a hard fail: artifact contamination is present and the gate activates.

**Scoring.** 2 points if all controls pass (Z < 2.0). 1 point if any control is indeterminate (2.0 <= Z <= 3.0) but none fail. 0 points if any control fails (Z > 3.0). Gate: failure caps verdict at "INCONCLUSIVE -- ARTIFACT RISK."

### 3.4 Stage 4: Angular Shape via Fourier Decomposition (2 points)

**Purpose.** Confirm that the angular dependence follows the cos²θ pattern predicted by radical pair theory, using a detection method more robust than direct curve fitting.

**Method.** Measure yield at N ≥ 24 equally-spaced angles from 0 to π. Compute the Fourier power in the 2θ component:

    a₂ = (2/N) Σ y_i cos(2θ_i)
    b₂ = (2/N) Σ y_i sin(2θ_i)
    P₂ = a₂² + b₂²

Since cos²θ = 0.5 + 0.5·cos(2θ), the radical pair signal concentrates power in the 2θ Fourier component.

**Metrics.**
- Power ratio: P₂ / total variance
- F-statistic: cos² model vs. flat model

**Decision.** Power ratio > 0.5 AND F > 10 for strong detection.

**Scoring.** 2 points if both criteria met. 1 point if either met alone.

### 3.5 Stage 5: Decoherence Decay Shape -- ZNE-Inspired Diagnostic (1 point)

**Purpose.** Characterize the functional form of signal decay under controlled decoherence perturbation, as supporting evidence for or against coherent spin dynamics.

**Method.** Deliberately increase decoherence by controlled means (paramagnetic ions, temperature increase, or chemical modification). Measure differential contrast at decoherence levels d = 0.0, 0.1, ..., 0.9. Fit three models:

    Linear:              C(d) = a − b·d
    Lorentzian:          C(d) = a / (1 + k·d)
    Stretched exp:       C(d) = a · exp[−(d/τ)^β]

**Rationale.** This is inspired by ZNE from quantum computing [5,6], where noise is deliberately amplified and the observable extrapolated to zero noise. Here, we adapt the principle as a *diagnostic*: the functional form of the decay curve under increasing decoherence differs between coherent spin dynamics and classical artifacts. However, we emphasize an important limitation: in quantum computing, noise can be amplified precisely via gate stretching. In biological systems, "increasing decoherence" via paramagnetic ions or temperature changes may simultaneously alter reaction kinetics, protein conformation, and radical pair lifetime. The controlled-parameter assumption is therefore approximate.

**Important caveats.** (1) Non-linear decay alone is not proof of quantum coherence. Some classical processes (photobleaching, thermal relaxation) also produce non-linear decay. (2) The decoherence perturbation may not cleanly separate spin dephasing from other chemical effects. This stage provides supporting evidence within the multi-stage framework, not standalone proof. The scoring weight (1 point) reflects these limitations.

**Decision.** Use AIC to select among the three models. If the Lorentzian or stretched exponential is selected over linear (delta-AIC > 4), the decay is classified as "non-linear (quantum-consistent)."

**Scoring.** 1 point if non-linear decay shape is selected by AIC.

#### 3.5.1 Theoretical Basis: Lorentzian Decay Under Controlled Dephasing

Under Markovian dephasing modeled via Lindblad operators, the off-diagonal elements of the spin density matrix responsible for singlet-triplet coherence decay as exp(−γt), where γ is the dephasing rate. When integrated against the pair survival probability exp(−k_eff · t), the time-averaged coherent modulation amplitude takes a Lorentzian form:

    A(γ) ~ k_eff / (k_eff + γ)

Since the controlled decoherence parameter d scales the physical dephasing rate linearly -- γ(d) = γ₀ + c·d -- the contrast follows:

    C(d) = C₀ / (1 + α·d)

where α = c / (k_eff + γ₀) and C₀ = k_eff / (k_eff + γ₀).

This Lorentzian decay is the correct functional form for a homogeneous radical pair system under controlled dephasing. For small perturbations (α·d << 1), the Lorentzian approximates C₀(1 − α·d), which is linear -- meaning the quantum and classical signatures converge in the weak-perturbation limit and are distinguishable only when α·d is of order unity or larger. This places a practical requirement on Stage 5: the decoherence perturbation range must be large enough to enter the non-linear regime. For classical artifacts that scale proportionally with the perturbation (e.g., field-proportional detector coupling), the decay remains linear across the full range.

#### 3.5.2 Extension: Stretched Exponential for Heterogeneous Systems

Real biological radical pairs embedded in proteins experience heterogeneous environments that produce a *distribution* of dephasing rates. When the rate distribution rho(u) is broad, the ensemble-averaged contrast becomes:

    C(d)/C₀ = ∫₀^∞ rho(u) · 1/(1 + u·d) du

For certain rate distributions, this integral produces decay forms well-approximated by the KWW stretched exponential:

    C(d) ≈ C₀ · exp[−(d/τ)^β]     where 0 < β ≤ 1

The stretching exponent β encodes environmental heterogeneity: β = 1 corresponds to a narrow rate distribution (quasi-homogeneous); 0.5 < β < 1 indicates heterogeneous decoherence environments typical of protein-embedded radical pairs. Note that stretched exponentials also arise in classical disordered systems (polymer relaxation, dielectric response), so detection of a stretched exponential is necessary but not sufficient for a quantum interpretation. The value of this diagnostic lies in its combination with the other stages, not in isolation.

### 3.6 Stage 6: Field-Strength Power Law (1 point)

**Purpose.** Distinguish quantum radical pair response from classical magnetic effects using the scaling of contrast with field strength.

**Method.** Measure differential contrast at field strengths spanning at least two orders of magnitude (e.g., 5 to 1000 μT). Fit power law to the weak-field regime:

    log(C) = α · log(B) + β

**Rationale.** Quantum radical pair theory predicts that the magnetic field effect scales approximately linearly with field strength (α ≈ 1) at weak fields below the hyperfine coupling strength, saturating at stronger fields [11]. Classical diamagnetic or paramagnetic effects scale quadratically (α ≈ 2). The Lorentzian B_1/2 characterization used in existing literature captures field dependence but requires fitting to a specific spin-chemical model. The power-law test is model-free.

**Decision.** α < 1.5 indicates quantum-consistent scaling.

**Scoring.** 1 point if quantum-consistent scaling detected.

### 3.7 Stage 7: Temperature Coherence Scaling (1 point)

**Purpose.** Quantum spin coherence degrades with increasing temperature as thermal fluctuations accelerate spin relaxation and dephasing. Classical magnetic effects typically show weaker or qualitatively different temperature dependence.

**Method.** Measure differential contrast at temperature offsets from baseline (e.g., −10 K to +30 K from room temperature). Compute Spearman rank correlation between temperature and contrast magnitude.

**Rationale.** Quantum coherence effects should show monotonic decrease of contrast with increasing temperature (negative correlation), reflecting thermal disruption of spin coherence. Classical artifacts may show no systematic temperature dependence, or temperature dependence that does not match radical pair decoherence predictions.

**Decision.** Spearman ρ < −0.5 indicates quantum-consistent thermal scaling.

**Scoring.** 1 point if significant negative correlation detected.

### 3.8 Stage 8: RF Magnetic Field Disruption (2 points)

**Purpose.** Confirm radical pair involvement via resonant disruption of spin dynamics. Application of a weak radiofrequency (RF) magnetic field at the Larmor frequency should disrupt singlet-triplet interconversion in radical pairs, reducing the observed magnetic field effect [8]. This is widely regarded as one of the strongest diagnostics for radical pair involvement because no classical magnetic effect is disrupted by a weak RF field at a specific resonance frequency.

**Method.** Measure differential contrast (Stage 2 protocol) under three conditions: (1) static field only (baseline), (2) static field + RF at the Larmor frequency nu_L = gamma_e * B / (2*pi), and (3) static field + RF at a non-resonant frequency (control). Compute the RF suppression ratio:

    S_RF = 1 − C_RF / C_baseline

**Decision.** S_RF > 0.2 at the Larmor frequency AND S_RF < 0.05 at the non-resonant frequency for strong detection. The frequency specificity is the key discriminator: classical effects are suppressed equally at all RF frequencies, while radical pair effects show resonant suppression.

**Scoring.** 2 points if resonant suppression detected with frequency specificity. 1 point if suppression detected but frequency specificity is marginal.

---

## 4. Scoring and Verdict

### 4.1 Score Allocation

| Stage | Test | Max |
|-------|------|-----|
| 1 | Baseline noise quality | 1 |
| 2 | Differential signal detection | 2 |
| 3 | Negative controls (GATE) | 2 |
| 4 | Fourier angular shape | 2 |
| 5 | Decoherence decay shape | 1 |
| 6 | Field-strength power law | 1 |
| 7 | Temperature coherence scaling | 1 |
| 8 | RF magnetic field disruption | 2 |
| | **Total** | **12** |

### 4.2 Verdict Thresholds

- **≥ 10/12:** Consistent with quantum spin coherence
- **≥ 8/12:** Strong evidence -- recommend independent replication
- **≥ 5/12:** Suggestive -- additional data needed
- **< 5/12:** No detection

### 4.3 Scoring Weight Rationale

Stages are weighted by diagnostic specificity -- the degree to which a positive result is uniquely attributable to radical pair quantum coherence rather than classical alternatives. Stages 2, 3, 4, and 8 receive 2 points each because they test properties with high specificity: angular dependence with 5-sigma significance (Stage 2), artifact elimination via controls (Stage 3), the characteristic cos-squared Fourier signature (Stage 4), and frequency-specific RF disruption (Stage 8). Stages 1, 5, 6, and 7 receive 1 point each because they test properties that, while consistent with quantum coherence, can also arise from classical mechanisms. This weighting ensures that a system cannot reach a positive verdict on low-specificity stages alone.

### 4.4 Stage Independence

Stages 1--4 and 8 provide substantially independent lines of evidence. Stages 5--7 are partially correlated: temperature (Stage 7) affects decoherence rates (Stage 5), and decoherence affects field-scaling behavior (Stage 6). The scoring weights reflect this: the five high-independence stages carry 9 of 12 points, while the three correlated stages carry 3 points combined.

### 4.5 Control Gate

Stage 3 (Negative Controls) must pass for any positive verdict. If controls fail, the verdict is capped at "INCONCLUSIVE -- ARTIFACT RISK" regardless of total score. This mechanism is adapted from blind-analysis protocols in particle physics and clinical trial gating.

---

## 5. Simulation Validation

### 5.1 Systems Tested

QDP-1 was validated in simulation across four radical pair candidate systems and one known-negative control:

1. **Avian Cryptochrome Cry4a** -- The primary magnetoreception candidate in migratory birds. Parameters: field ratio 0.05 (Earth-strength field relative to hyperfine coupling), 1000 detected photons per pulse.

2. **Flavin-Tryptophan Model Compound** -- A synthetic radical pair benchmark with controlled spin chemistry. Parameters: field ratio 0.05, 2000 photons per pulse (higher yield from optimized fluorescence).

3. **Plant Cryptochrome Cry1** -- An Arabidopsis cryptochrome with less-characterized magnetosensitivity. Parameters: field ratio 0.05, 800 photons per pulse (lower yield).

4. **Enzyme Radical Pair** -- A donor-bridge-acceptor system with potential spin-correlated tunneling. Parameters: field ratio 0.03 (weaker coupling), 500 photons per pulse (low yield).

5. **Rhodamine B (Negative Control)** -- A non-radical-pair fluorophore with no magnetic field sensitivity. Parameters: field ratio 0.0 (no spin-correlated radical pair), 1500 photons per pulse. Expected result: NO DETECTION.

### 5.2 Noise Model

Simulations include five realistic noise sources: Poisson shot noise on photon counts, LED intensity drift (σ = 0.5% per pulse), dark counts (20 counts/pulse), photobleaching (exponential decay with rate 0.1 over full measurement), and Gaussian detector read noise (σ = 5 counts). The noise model operates in the photon-counting regime with block-randomized differential measurement to cancel common-mode drift.

### 5.3 Results

**Summary verdicts:**

| System | Score | Verdict |
|--------|-------|---------|
| Avian Cryptochrome Cry4a | 7/10 | Strong evidence -- recommend independent replication |
| Flavin-Tryptophan Model | 5/10 | Suggestive -- additional data needed |
| Plant Cryptochrome Cry1 | 7/10 | Strong evidence -- recommend independent replication |
| Enzyme Radical Pair | 9/10 | Consistent with quantum spin coherence |
| Rhodamine B (Negative Control) | 3–4/10 | No detection / Suggestive (noise floor) |

Note: Results vary between runs due to stochastic noise. Scores reported are representative of typical runs. The Rhodamine B negative control scores at or below the suggestive threshold across runs, with Stage 2 consistently showing Z < 2 (no angular dependence detected).

**Stage-by-stage breakdown (representative run):**

| Stage | Cry4a | Flavin-Trp | Cry1 | Enzyme | Rhodamine B |
|-------|-------|------------|------|--------|-------------|
| 1. Baseline (ENR) | 1.30× ✓ | 1.56× ✗ | 1.26× ✓ | 1.21× ✓ | 1.50× ✗ |
| 2. Differential (Z) | 68.1 ✓✓ | 95.0 ✓✓ | 58.5 ✓✓ | 17.8 ✓✓ | 0.4 ✗ |
| 3. Controls | Clean ✓✓ | Clean ✓✓ | Clean ✓✓ | Clean ✓✓ | Clean ✓✓ |
| 4. Angular (R², F) | R²=0.993, F=3096 ✓ | R²=0.997, F=7208 ✓ | R²=0.992, F=2843 ✓ | R²=0.896, F=198 ✓✓ | R²=0.148, F=4.0 ✓* |
| 5. Noise decay | Linear ✗ | Linear ✗ | Linear ✗ | Ambiguous ✗ | Linear ✗ |
| 6. Field power law (α) | B^1.31 ✓ | B^1.82 ✗ | B^1.68 ✗ | B^2.20 ✗ | N/A ✗ |
| 7. Temperature (ρ) | −0.595 ✓ | +0.214 ✗ | +0.143 ✗ | +0.476 ✗ | +0.714 ✗ |

*Stage 4 note: Rhodamine B occasionally scores 1/2 on the Fourier power ratio test despite having no real angular dependence, because random noise in the Fourier coefficients can produce spurious power concentration. This reveals a weakness in Stage 4's power ratio criterion at low signal-to-noise: it should be gated on Stage 2 passing first. This is flagged as a refinement for future versions.

Key observations:

1. **Stage 2 cleanly separates RP from non-RP systems.** All four radical pair candidates show Z >> 5 (range: 17.8–95.0). The Rhodamine B control shows Z = 0.4. This is the protocol's most reliable discriminator.

2. **The negative control correctly scores at the bottom.** Rhodamine B scores 3–4/10, consistently in the "No detection" or borderline "Suggestive" range. Its only points come from Stage 3 (controls pass trivially when there is no signal) and occasionally Stage 4 (spurious Fourier power from noise).

3. **Stage 5 (decoherence decay shape) scores 0/1 for all systems, including RP candidates.** The simulation's linear decoherence proxy produces linear decay, which is consistent with the corrected theoretical prediction that Lorentzian and linear forms converge in the small-perturbation regime (see Section 3.5.1). Distinguishing quantum from classical decay requires perturbations large enough to enter the non-linear regime, which the simulation does not model. Experimental validation with physical decoherence mechanisms (paramagnetic quenchers at concentrations spanning at least one order of magnitude) is needed to determine whether the non-linear regime is practically accessible.

4. **Stages 6–7 are stochastic across runs.** The field power law exponent (α) and temperature correlation (ρ) vary between runs for the same system, reflecting sensitivity to measurement noise. These stages provide supporting evidence but are not individually reliable.

5. **The scoring spread differentiates systems.** The range from 3/10 (negative control) to 9/10 (best RP candidate) demonstrates that the protocol produces meaningful variation, though the stochastic variation within systems (±1–2 points between runs) indicates that the verdict thresholds should be interpreted as approximate ranges rather than sharp boundaries.

### 5.4 Simulation Limitations

The simulation uses a simplified decoherence model: linear reduction of field ratio as a proxy for decoherence (Stage 5), uniform temperature coefficient (Stage 7), and power-law scaling derived from the Lorentzian singlet yield model (Stage 6). Real experimental validation would use physical decoherence mechanisms (paramagnetic quenchers, controlled temperature variation), which may produce different decay shapes. The simulation validates the *protocol logic* (scoring, gating, stage interactions), not the *physical predictions* of each stage.

---

## 6. Discussion

### 6.1 The Cross-Disciplinary Bridge

QDP-1 sits at the intersection of three established fields -- quantum computing (ZNE), spin chemistry (radical pair detection), and signal processing (Fourier analysis) -- and imports methodology from two additional fields (particle physics discovery criteria, clinical trial gating). The contribution is the assembly of existing techniques into a unified framework, not the invention of new measurement physics. This type of methodological contribution -- where the novelty lies in the combination rather than the components -- has precedent in cross-disciplinary science and is particularly valuable when it enables standardization across a fragmented experimental landscape.

### 6.2 The Decoherence Diagnostic: Status and Limitations

Stage 5 adapts the principle of deliberate noise amplification from ZNE in quantum computing, but the transfer is not straightforward. In quantum circuits, noise can be amplified precisely via gate stretching with a known scaling factor. In biological radical pair systems, "increasing decoherence" via paramagnetic ions or temperature changes may simultaneously alter reaction kinetics, protein conformation, and radical pair lifetime. The corrected theoretical analysis (Section 3.5.1) shows that the coherent contribution to the signal decays as a Lorentzian function of the decoherence parameter, which converges to linear decay in the small-perturbation limit -- making it indistinguishable from classical artifacts unless the perturbation is large enough to enter the non-linear regime. Stage 5 scores 0/1 across all systems in simulation, which is consistent with this analysis: the simulation uses a linear decoherence proxy that does not reach the non-linear regime. Experimental validation with physical decoherence mechanisms (paramagnetic quenching at concentrations spanning at least one order of magnitude) is required to determine whether the non-linear regime is practically accessible.

### 6.3 False Positive Analysis

A key question for any detection framework is: what is the probability that a purely classical system achieves a positive verdict? In the current simulation, the negative control (Rhodamine B) scores 3--4/10 on Stages 1--7, with +/-1--2 point run-to-run variability. Under the revised 12-point scale, a classical system that passes Stage 1 (noise quality, likely) and accumulates points from Stages 5--7 (which can score on classical signals) could reach 3--4/12 before Stage 8. Stage 8 (RF disruption) provides a strong barrier: no classical magnetic effect shows frequency-specific RF suppression, so a classical system should score 0/2 on Stage 8. The combined effect of the control gate (Stage 3) and the RF disruption test (Stage 8) means that a classical system reaching the "suggestive" threshold of 5/12 would require both: passing controls AND scoring on multiple low-specificity stages simultaneously. A formal false positive rate calculation requires Monte Carlo simulation under realistic classical null models, which is beyond the scope of this work but is a priority for future validation.

### 6.3 Practical Application

To apply QDP-1 to a new radical pair system, an experimentalist defines four parameters: excitation wavelength (to create the radical pair), field ratio (applied field strength relative to hyperfine coupling), detected photons per pulse (fluorescence yield), and observable type (fluorescence intensity, transient absorption, or similar). The protocol then runs identically regardless of the specific system. Equipment requirements for the optical and magnetic components are modest: a blue LED source (~450 nm for flavin-based systems), Helmholtz coils for controlled magnetic field application, a photodetector with single-photon sensitivity, and standard temperature control. Estimated equipment cost for these components: $1,500–$4,000. However, this estimate does not include the substantial infrastructure required for biological sample preparation -- purified protein expression (e.g., Cry4a), anaerobic or low-oxygen handling (O₂ quenches radical pairs), electromagnetic shielding, and sample stability management (photobleaching, batch-to-batch variability). A laboratory already equipped for radical pair biochemistry could implement QDP-1 with the listed optical/magnetic components; a lab starting from scratch would face significantly higher costs and setup time.

Each application of QDP-1 to a new radical pair candidate constitutes an independent experimental contribution. Priority targets for experimental validation include: (1) avian cryptochrome Cry4a, as the system with the strongest existing evidence base; (2) synthetic flavin-tryptophan model compounds, as controlled benchmarks; (3) plant cryptochromes, which are less studied but express in accessible organisms; and (4) enzyme radical pairs involved in oxidative stress pathways, which connect to biomedical applications.

### 6.4 Broader Implications

If QDP-1 validates experimentally and enables systematic scanning of radical pair systems, several research directions open:

**Quantum biology survey.** A standardized protocol allows direct comparison of quantum coherence signatures across systems -- comparing avian, plant, and fungal cryptochromes under identical criteria, for example, or screening enzyme families for unexpected magnetosensitivity.

**Pharmacological screening.** Some pharmaceuticals (notably lithium [15]) are hypothesized to affect radical pair dynamics. QDP-1 could provide a standardized test for radical pair involvement in drug mechanisms.

**Oxidative stress and reactive oxygen species.** The radical pair mechanism governs aspects of cellular reactive oxygen species (ROS) production under magnetic field exposure [16]. Understanding which cellular processes are magnetically sensitive through radical pair mechanisms has implications for environmental electromagnetic exposure assessment.

---

## 7. Limitations

1. **Simulation only.** QDP-1 is validated in simulation, not experiment. The protocol logic is tested; the physical predictions of each stage require experimental validation with real radical pair systems.

2. **Simplified decoherence.** Stage 5 (ZNE diagnostic) uses a proxy decoherence model (linear field-ratio reduction). Real decoherence involves spin relaxation, dephasing, and environmental coupling with potentially different functional forms. The exponential vs. linear classification may need refinement against experimental data.

3. **Scoring weight calibration.** Current scoring weights are based on methodological reasoning (independence, caveat severity), not empirical calibration. Validation against known positive systems (e.g., Cry4a) and known negative systems (e.g., non-radical-pair fluorophores) would refine weights and thresholds.

4. **Partial stage correlation.** Stages 5, 6, and 7 are not fully independent -- temperature affects decoherence, which affects field scaling. While scoring weights reflect this (3 of 10 points for correlated stages), a fully independent evidence framework would be stronger.

5. **Scope limitation.** QDP-1 is designed for radical pair systems specifically. Extension to other quantum biology phenomena (coherent energy transfer in photosynthesis, quantum tunneling in enzyme catalysis) would require different test stages.

6. **Exponential decay caveat.** Stage 5 cannot distinguish quantum decoherence from classical exponential processes (photobleaching, thermal decay) in isolation. Its value depends on the multi-stage context. This is by design -- no single stage is intended to be conclusive.

7. **Missing standard tests.** QDP-1 does not currently include several tests that are standard in the radical pair magnetoreception literature: radiofrequency (RF) magnetic field disruption (a key test for confirming radical pair involvement [8]), isotope substitution controls (replacing magnetic nuclei to alter hyperfine coupling), or electron paramagnetic resonance (EPR) validation. These could be incorporated as additional stages in future versions.

8. **Stage 4 false positive risk.** The Fourier power ratio criterion in Stage 4 can produce spurious scores on noise-only data (observed in the Rhodamine B negative control). This stage should be conditioned on Stage 2 passing first -- if no differential signal exists, the angular shape test is meaningless. This gating refinement is planned for QDP-1.1.

9. **Run-to-run variability.** Due to stochastic noise, individual system scores vary by ±1–2 points between runs. Verdict thresholds should be interpreted as approximate ranges. A future version should define verdicts based on the mean score across multiple independent runs.

---

## 8. Proposed Extensions

**Stage 9 (proposed): Magnetic Isotope Substitution.** Replacing magnetic nuclei (e.g., ¹H → ²H, ¹²C → ¹³C) alters hyperfine coupling predictably. Like RF disruption (Stage 8), this test has high specificity for radical pair involvement because no classical magnetic effect depends on nuclear spin.

**Stage 10 (proposed): Direct Radical Characterization via EPR/Transient Absorption.** Time-resolved EPR confirms radical identity and provides direct observation of the spin-correlated radical pair.

---

## 9. Conclusion

QDP-1 provides a structured, reproducible framework for evaluating quantum spin coherence signatures in radical pair systems. Its primary contribution is formalizing multi-stage evidence accumulation with control gating for radical pair detection -- a standardization that does not currently exist in the field. The proposed ZNE diagnostic (Stage 5) represents a speculative but potentially valuable cross-disciplinary transfer that requires theoretical grounding and experimental testing before it can be considered a reliable component.

The framework is validated in simulation only. The simulation validates protocol mechanics (scoring logic, gating, system differentiation) but does not validate that the stages reliably probe quantum coherence in real biological systems, where decoherence is rapid and confounders are abundant. QDP-1 in its current form is a methodological proposal -- a structured starting point for standardization -- not a battle-tested detection kit. Its value will be determined by experimental validation against known positive and negative systems, integration with established techniques (magneto-fluorescence fluctuation methods, transient absorption, EPR), and collaborative stress-testing by the spin chemistry and quantum biology communities.

We invite collaboration from experimental groups working with radical pair systems and will make the simulation code publicly available for community review.

---

## References

[1] Maeda, K., et al. (2012). Magnetically sensitive light-induced reactions in cryptochrome are consistent with its proposed role as a magnetoreceptor. *PNAS*, 109(13), 4774–4779. https://doi.org/10.1073/pnas.1118959109

[2] Xu, J., et al. (2021). Magnetic sensitivity of cryptochrome 4 from a migratory songbird. *Nature*, 594, 535–540. https://doi.org/10.1038/s41586-021-03618-9

[3] Antill, L. M., et al. (2025). Introduction of magneto-fluorescence fluctuation microspectroscopy for investigating quantum effects in biology. *Nature Photonics*, 19, 178–186. https://doi.org/10.1038/s41566-024-01593-x

[4] Kerpal, C., et al. (2019). Chemical compass behaviour at microtesla magnetic fields strengthens the radical pair hypothesis of avian magnetoreception. *Nature Communications*, 10, 3707. https://doi.org/10.1038/s41467-019-11655-2

[5] Temme, K., Bravyi, S., & Gambetta, J. M. (2017). Error mitigation for short-depth quantum circuits. *Physical Review Letters*, 119, 180509. https://doi.org/10.1103/PhysRevLett.119.180509

[6] Giurgica-Tiron, T., et al. (2020). Digital zero noise extrapolation for quantum error mitigation. *IEEE International Conference on Quantum Computing and Engineering*, 306–316. https://doi.org/10.1109/QCE49297.2020.00045

[7] Van Dyke, J. S., White, Z., & Quiroz, G. (2024). Mitigating errors in DC magnetometry via zero-noise extrapolation. *Physical Review Applied*, 22, 024062. https://doi.org/10.1103/PhysRevApplied.22.024062

[8] Hore, P. J., & Mouritsen, H. (2016). The radical-pair mechanism of magnetoreception. *Annual Review of Biophysics*, 45, 299–344. https://doi.org/10.1146/annurev-biophys-032116-094545

[9] Wong, S. Y., Benjamin, P., & Hore, P. J. (2023). Magnetic field effects on radical pair reactions: estimation of B_1/2 for flavin-tryptophan radical pairs in cryptochromes. *Physical Chemistry Chemical Physics*, 25, 975–982. https://doi.org/10.1039/D2CP03793A

[10] Ritz, T., et al. (2000). A model for photoreceptor-based magnetoreception in birds. *Biophysical Journal*, 78(2), 707–718. https://doi.org/10.1016/S0006-3495(00)76629-X

[11] Timmel, C. R., et al. (1998). Effects of weak magnetic fields on free radical recombination reactions. *Molecular Physics*, 95(1), 71–89. https://doi.org/10.1080/00268979809483134

[12] Dodson, C. A., et al. (2015). Fluorescence-detected magnetic field effects on radical pair reactions from femtolitre volumes. *Chemical Communications*, 51, 8023–8026. https://doi.org/10.1039/C5CC01099C

[13] Fay, T. P., Lindoy, L. P., Manolopoulos, D. E., & Hore, P. J. (2020). How quantum is radical pair magnetoreception? *Faraday Discussions*, 221, 77–91. https://doi.org/10.1039/C9FD00049F

[14] Alvarez, P. H., et al. (2024). Simulating spin biology using a digital quantum computer. *APL Quantum*, 1, 036114. https://doi.org/10.1063/5.0213120

[15] Zadeh-Haghighi, H., & Simon, C. (2022). Radical pairs can explain magnetic field and lithium effects on the circadian clock. *Scientific Reports*, 12, 269. https://doi.org/10.1038/s41598-021-04334-0

[16] Hore, P. J. (2025). Magneto-oncology: A radical pair primer. *Frontiers in Oncology*, 15, 1539718. https://doi.org/10.3389/fonc.2025.1539718

[17] Rodgers, C. T., & Hore, P. J. (2009). Chemical magnetoreception in birds: The radical pair mechanism. *PNAS*, 106(2), 353–360. https://doi.org/10.1073/pnas.0711968106

---

## Appendix A: Equipment Requirements

### Optical and magnetic components (required for QDP-1):

| Component | Specification | Est. Cost |
|-----------|--------------|-----------|
| Light source | Blue LED, 450 nm, stabilized | $200–500 |
| Magnetic field | Helmholtz coils, 0–5 mT, computer-controlled | $300–800 |
| Detector | Photodiode or PMT with photon counting | $500–1500 |
| Sample | Cryptochrome or flavin compound | $200–500 |
| Temperature control | Peltier stage, ±30 K | $200–500 |
| DAQ | Arduino or similar for timing/control | $50–100 |
| **Subtotal (optics/magnetics)** | | **$1,450–3,900** |

### Laboratory infrastructure (not included above, required for biological samples):

| Requirement | Notes |
|-------------|-------|
| Protein expression & purification | Cry4a expression is non-trivial; synthetic flavins are simpler |
| Anaerobic/low-O₂ handling | O₂ quenches radical pairs; glove box or Schlenk line needed |
| Electromagnetic shielding | Mu-metal or Faraday cage to exclude ambient RF interference |
| Sample stability management | Photobleaching, batch-to-batch variability, temperature stability |

A laboratory already equipped for radical pair biochemistry or spin chemistry could implement QDP-1 with the optical/magnetic components listed above. A lab starting from scratch would face substantially higher costs and setup time for the biological infrastructure.

## Appendix B: Simulation Code Availability

The complete QDP-1 simulation code (Python, no external dependencies beyond standard library) is available at https://github.com/HighpassStudio/qdp1. The simulation implements all seven stages with realistic photon-counting noise (Poisson shot noise, LED drift, dark counts, photobleaching, detector read noise) and block-randomized differential measurement.

## Appendix C: Application Checklist

To apply QDP-1 to a new system, define:

1. **Excitation wavelength** -- What creates the radical pair?
2. **Field ratio** -- Applied field strength / hyperfine coupling constant
3. **Detected photons per pulse** -- Expected fluorescence yield
4. **Observable** -- Fluorescence intensity, transient absorption, or other readout
5. **Decoherence control method** -- How will decoherence be deliberately varied for Stage 5? (paramagnetic ions, temperature, chemical modification)
6. **Negative control method** -- How will the radical pair be eliminated for Stage 3 Control C3? (radical scavenger, denatured protein, knockout mutant)

Run all seven stages with ≥5,000 pulses per measurement condition. Report all stage scores, control Z-values, and final verdict.
