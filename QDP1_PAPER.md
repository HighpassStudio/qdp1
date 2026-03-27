# QDP-1: A Multi-Stage Framework for Detecting Quantum Spin Coherence in Radical Pair Systems

**Brad Loomis, MS, PE, PTOE**
Independent Research

---

## Abstract

We propose QDP-1, a seven-stage detection protocol for identifying quantum spin coherence effects in radical pair systems under ambient conditions. The framework makes two methodological contributions: (1) it unifies angular dependence testing, field-strength power-law discrimination, temperature-dependent coherence scaling, and negative control gating into a single scored detection framework for radical pair systems; and (2) it proposes adapting zero-noise extrapolation (ZNE), a proven error-mitigation technique from quantum computing, as a diagnostic fingerprint for distinguishing coherent spin dynamics from classical behavior — though this component remains a hypothesis awaiting theoretical grounding and experimental validation. The protocol borrows structural elements from particle physics discovery criteria (5-sigma thresholds, control gating) and clinical trial methodology (staged evidence, artifact elimination). We validate QDP-1 in simulation across four radical pair candidate systems and one known-negative control (a non-radical-pair fluorophore), demonstrating that the protocol differentiates between systems and that the control gate correctly caps verdicts when artifact contamination is present. The ZNE diagnostic (Stage 5) is proposed but not yet validated: the simulation's decoherence proxy does not produce the exponential decay signature the stage is designed to detect, and experimental validation with physical decoherence mechanisms is required. No existing framework in the quantum biology literature unifies these elements into a single system-agnostic protocol. QDP-1 is validated in simulation only; experimental validation is needed.

**Keywords:** radical pair mechanism, quantum biology, zero-noise extrapolation, magnetoreception, detection protocol, spin coherence

**Code availability:** Simulation code is available at https://github.com/HighpassStudio/qdp1

---

## 1. Introduction

The radical pair mechanism is the leading candidate explanation for biological magnetoreception and has been confirmed in cryptochrome systems through fluorescence-detected magnetic field effects [1], Earth-strength magnetic sensitivity in tightly bound radical pairs [2], and direct observation of long-lived flavin/tryptophan radical pairs [3]. Experimental techniques for detecting radical pair quantum effects have matured considerably: magneto-fluorescence fluctuation microspectroscopy enables investigation of quantum effects in biology at the single-molecule scale [4], and sensing magnetic-field effects at the scale of small molecular ensembles is now achievable [5].

Despite this progress, the field lacks a unified detection framework. Individual techniques — fluorescence-based magnetic field effect measurement, angular dependence characterization, B_1/2 field-strength analysis, temperature-dependent coherence studies — are applied independently and evaluated by different criteria across different laboratories. This creates several problems:

1. **No standard for sufficiency.** How many positive indicators constitute evidence for quantum spin coherence? There is no consensus threshold analogous to the 5-sigma standard in particle physics.

2. **No control gating.** Negative controls are used, but there is no formal mechanism to prevent false positives from propagating when controls show contamination.

3. **No cross-disciplinary diagnostic transfer.** Zero-noise extrapolation (ZNE), a technique developed for quantum computing error mitigation [6,7], provides a natural framework for probing quantum coherence effects through deliberate noise scaling. This approach has begun migrating from quantum computing into quantum sensing [8] but has not been applied to quantum biology or radical pair systems.

4. **No system-agnostic protocol.** Each new radical pair candidate is evaluated with ad hoc methods. A reusable detection kit would accelerate the field.

QDP-1 addresses these gaps by combining seven partially independent tests into a scored verdict with explicit control gating. The protocol is designed to be applied identically to any radical pair system, with each application constituting an independent experimental contribution. This work is intended as a starting point for community evaluation and refinement.

### Scope

QDP-1 detects signatures *consistent with* quantum spin coherence in radical pair systems. It does not test for entanglement specifically, nor does it address other quantum biological phenomena (coherent energy transfer, quantum tunneling) without additional stages. The framework provides evidence grades, not binary proof.

---

## 2. Related Work

### 2.1 Radical Pair Detection Methods

The radical pair mechanism and its role in biological magnetoreception have been extensively reviewed [9,10]. Key experimental milestones include the detection of magnetic field effects on cryptochrome fluorescence [1], characterization of angular dependence in singlet yield [11], measurement of B_1/2 parameters for field-strength characterization [12], and investigation of temperature effects on spin coherence [13]. These techniques are individually well-established and are not claimed as novel contributions of this work.

### 2.2 Zero-Noise Extrapolation in Quantum Computing

ZNE was introduced as an error-mitigation technique for near-term quantum computers [6,7]. The core idea is to deliberately amplify noise, measure the observable at multiple noise levels, and extrapolate to the zero-noise limit. ZNE is now standard practice in quantum computing and has begun migrating into quantum sensing — notably, a 2024 study applied ZNE-style extrapolation to mitigate errors in DC magnetometry [8]. However, the use of ZNE as a *diagnostic* (to distinguish quantum from classical behavior based on decay curve shape) rather than as an error-mitigation tool, and its application to biological or chemical radical pair systems, does not appear in the mainstream literature.

### 2.3 The Quantum Biology Detection Gap

The question "How quantum is radical pair magnetoreception?" has been addressed theoretically [14], establishing that radical pair magnetoreception satisfies formal criteria for quantum behavior from a quantum information perspective. However, this assessment is conceptual, not operational — it does not provide a staged detection protocol for experimental use.

The most relevant methodological advances are the 2024 magneto-fluorescence fluctuation microspectroscopy technique [4] and the 2024 study on sensing magnetic-field effects at small ensemble scales [5]. Both move toward reusable measurement methodology for quantum biology, but neither constitutes a multi-stage scored framework with control gating and cross-disciplinary diagnostic integration.

A 2024 study on simulating spin biology using a digital quantum computer [15] represents the most direct bridge between quantum computing and quantum biology in the existing literature. However, the connection there is different: the paper uses extrapolation ideas akin to ZNE for simulation accuracy, not as an experimental diagnostic for biological systems.

### 2.4 Novelty Claim

QDP-1 unifies ZNE-style noise scaling (adapted from quantum computing), Fourier angular power analysis (adapted from signal processing), power-law field discrimination, temperature coherence scaling, and negative control gating (adapted from particle physics and clinical trials) into a single scored detection framework for quantum biology. Based on a search across 2005–2025 literature in major journals and arXiv, no mainstream precedent was found for this full combination. The likely novelty is the assembly, not the individual parts.

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

### 3.3 Stage 3: Negative Controls — GATE (2 points)

**Purpose.** Eliminate artifacts. This stage is a gate: if controls fail, the final verdict is capped at "INCONCLUSIVE" regardless of total score.

**Controls.**
- C1: Same angle (θ_A = θ_B = 0). Tests for detector asymmetry or systematic bias unrelated to magnetic field angle.
- C2: No applied field / near-zero field. Tests for field-independent artifacts in the optical detection pathway.
- C3: Killed radical pair (radical scavenger addition or denatured protein). Tests whether the signal requires the spin-correlated radical pair.

**Decision.** Each control must show Z < 2.0 (no significant signal). Any control with Z > 3.0 flags artifact contamination.

**Scoring.** 2 points if all controls pass. 0 points if any control fails. Gate: failure caps verdict at "INCONCLUSIVE — ARTIFACT RISK."

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

### 3.5 Stage 5: Noise Decay Fingerprint — ZNE Diagnostic (1 point)

**Purpose.** Distinguish quantum coherence effects from classical artifacts using the shape of signal decay under controlled decoherence.

**Method.** Deliberately increase decoherence by controlled means (addition of paramagnetic ions, temperature increase, or chemical modification of the radical pair). Measure differential contrast at decoherence levels d = 0.0, 0.1, ..., 0.9. Fit two models:

    Linear:      C(d) = a − b·d           (R²_lin)
    Exponential: C(d) = a · exp(−k·d)     (R²_exp)

**Rationale.** This adapts zero-noise extrapolation (ZNE) from quantum computing [6,7]. In standard ZNE, noise is deliberately amplified and the observable extrapolated to zero noise to mitigate errors. Here, we repurpose the technique as a *diagnostic*: the shape of the decay curve under increasing decoherence distinguishes quantum from classical behavior. Quantum spin coherence effects typically produce non-linear (exponential-like) decay under increasing decoherence, reflecting the exponential sensitivity of coherent superposition to environmental noise. Many classical artifacts (e.g., linear detector drift, proportional field coupling) produce linear decay.

**Important caveat.** Exponential decay alone is not proof of quantum coherence. Some classical processes (photobleaching, thermal relaxation, chemical decay) also produce exponential decay. This stage provides supporting evidence within the multi-stage framework, not standalone proof. The scoring weight (1 point of 10) reflects this limitation.

**Decision.** R²_exp − R²_lin > 0.1 indicates exponential (quantum-consistent) decay.

**Scoring.** 1 point if exponential decay shape detected.

#### 3.5.1 Theoretical Basis: Why Exponential Decay Is Expected

The expectation that quantum spin coherence produces exponential (rather than linear) contrast decay under controlled decoherence follows from the standard open-quantum-system treatment of radical pair spin dynamics.

A radical pair born in a spin-correlated singlet state undergoes coherent singlet-triplet interconversion driven by hyperfine and Zeeman interactions. The differential contrast C (the magnetic field effect) depends on the amplitude of these quantum beats surviving through the pair lifetime. In the closed-system limit, the singlet probability P_S(t) oscillates at frequencies set by hyperfine differences and Zeeman splitting — oscillations that are the direct signature of quantum coherence.

Under Markovian dephasing (modeled via Lindblad operators acting on the spin density matrix), the off-diagonal elements of ρ responsible for singlet-triplet coherence decay as exp(−γt), where γ is the dephasing rate. When integrated against the pair survival probability exp(−k_eff · t), the time-averaged coherent modulation amplitude takes a Lorentzian-like form:

    A(γ) ~ k_eff / (k_eff + γ)

or, in the regime where dephasing dominates the envelope, approximately:

    C(γ) ≈ C₀ · exp(−α γ)

for a constant α related to the effective coherence time.

Since the controlled decoherence parameter d in Stage 5 is designed to scale the physical dephasing rate linearly — γ(d) = γ₀ + c·d (e.g., paramagnetic ion concentration is proportional to relaxation rate) — substitution yields:

    C(d) ≈ C₀ · exp(−β d)

where β = α·c. This is the exponential decay predicted by the Lindblad treatment.

For classical artifacts (detector drift, LED intensity scaling, field-independent chemical quenching), the contrast typically scales proportionally with the perturbation: C(d) ≈ C₀ − b·d (linear), because these processes act additively or multiplicatively on the signal amplitude without involving coherent superposition.

#### 3.5.2 Extension: Stretched Exponential for Heterogeneous Systems

The pure exponential derivation above assumes Markovian (memoryless) dephasing at a single rate γ. Real biological radical pairs embedded in proteins experience heterogeneous environments — conformational sub-states, fluctuating nuclear spin baths, multi-scale solvent dynamics — that produce a *distribution* of dephasing rates rather than a single value.

When the rate distribution P(γ) is broad, the ensemble-averaged contrast becomes a Laplace transform over that distribution. For many disordered systems (including spin relaxation in organic radicals and proteins), this produces the Kohlrausch-Williams-Watts (KWW) stretched exponential:

    C(d) = C₀ · exp[−(d / τ)^β]     where 0 < β ≤ 1

The stretching exponent β encodes the degree of environmental heterogeneity:

- **β = 1:** Pure exponential. Homogeneous Markovian dephasing. The simple case derived above.
- **0.5 < β < 1:** Stretched exponential. Heterogeneous or non-Markovian decoherence — multiple relaxation channels with different timescales. Still a signature of coherence loss (the magnetic field effect requires singlet-triplet coherences), but with distributed character. Quantitative predictions of spin decoherence in radical systems yield β ≈ 0.7–0.9 in certain regimes.
- **β → 0 or linear fit preferred:** No coherent decay structure. Consistent with classical artifact.

Formally, the stretched exponential arises as the Laplace transform of the rate distribution: C(d)/C₀ = ∫₀^∞ ρ(u) exp(−u·d) du, where ρ(u) is the probability density of dephasing rates across the ensemble. When ρ(u) is a delta function (single rate), this yields pure exponential decay; when ρ(u) is broad (as expected in protein-embedded radical pairs with conformational sub-states and multi-channel relaxation), the integral produces the KWW stretched exponential. This connection means the shape of C(d) directly encodes information about the underlying distribution of decoherence pathways — a delta-like distribution yields β = 1, a broad distribution yields β < 1, and a non-Laplace form (linear) suggests classical scaling. The physical origins of rate heterogeneity in radical pair systems include non-Markovian dynamics from slow protein motions, nuclear spin diffusion, fluctuating hyperfine couplings, and multi-channel relaxation (random local fields + singlet-triplet dephasing + g-tensor anisotropy).

**Proposed refinement for Stage 5.** Fit three models instead of two:

    Linear:              C(d) = a − b·d
    Exponential:         C(d) = a · exp(−k·d)
    Stretched exp:       C(d) = a · exp[−(d/τ)^β]

Use AIC (Akaike Information Criterion) or BIC (Bayesian Information Criterion) for model selection rather than raw ΔR², to properly penalize the extra parameter in the stretched exponential. The diagnostic then becomes:

- Stretched exponential preferred with β ∈ [0.6, 1.0]: "quantum-consistent — coherent decay with heterogeneous decoherence"
- Pure exponential preferred (β ≈ 1): "quantum-consistent — Markovian coherent decay"
- Linear preferred: "classical-consistent — no coherent decay structure"

This refinement is more physically grounded for real radical pair systems, where β < 1 is frequently observed in spin relaxation studies, and provides a continuous measure of "how quantum" the decay looks rather than a binary classification.

**Important caveat (retained).** Even with the stretched exponential extension, the decay shape test remains supporting evidence, not standalone proof. Some classical processes with distributed kinetics (e.g., heterogeneous photobleaching in a complex sample) can also produce stretched exponential decay. The multi-stage framework mitigates this — Stage 5 is one of seven tests, weighted at 1 point of 10.

### 3.6 Stage 6: Field-Strength Power Law (1 point)

**Purpose.** Distinguish quantum radical pair response from classical magnetic effects using the scaling of contrast with field strength.

**Method.** Measure differential contrast at field strengths spanning at least two orders of magnitude (e.g., 5 to 1000 μT). Fit power law to the weak-field regime:

    log(C) = α · log(B) + β

**Rationale.** Quantum radical pair theory predicts that the magnetic field effect scales approximately linearly with field strength (α ≈ 1) at weak fields below the hyperfine coupling strength, saturating at stronger fields [12]. Classical diamagnetic or paramagnetic effects scale quadratically (α ≈ 2). The Lorentzian B_1/2 characterization used in existing literature captures field dependence but requires fitting to a specific spin-chemical model. The power-law test is model-free.

**Decision.** α < 1.5 indicates quantum-consistent scaling.

**Scoring.** 1 point if quantum-consistent scaling detected.

### 3.7 Stage 7: Temperature Coherence Scaling (1 point)

**Purpose.** Quantum spin coherence degrades with increasing temperature as thermal fluctuations accelerate spin relaxation and dephasing. Classical magnetic effects typically show weaker or qualitatively different temperature dependence.

**Method.** Measure differential contrast at temperature offsets from baseline (e.g., −10 K to +30 K from room temperature). Compute Spearman rank correlation between temperature and contrast magnitude.

**Rationale.** Quantum coherence effects should show monotonic decrease of contrast with increasing temperature (negative correlation), reflecting thermal disruption of spin coherence. Classical artifacts may show no systematic temperature dependence, or temperature dependence that does not match radical pair decoherence predictions.

**Decision.** Spearman ρ < −0.5 indicates quantum-consistent thermal scaling.

**Scoring.** 1 point if significant negative correlation detected.

---

## 4. Scoring and Verdict

### 4.1 Score Allocation

| Stage | Test | Max |
|-------|------|-----|
| 1 | Baseline noise quality | 1 |
| 2 | Differential signal detection | 2 |
| 3 | Negative controls (GATE) | 2 |
| 4 | Fourier angular shape | 2 |
| 5 | Noise decay fingerprint (ZNE) | 1 |
| 6 | Field-strength power law | 1 |
| 7 | Temperature coherence scaling | 1 |
| | **Total** | **10** |

### 4.2 Verdict Thresholds

- **≥ 8/10:** Consistent with quantum spin coherence
- **≥ 6/10:** Strong evidence — recommend independent replication
- **≥ 4/10:** Suggestive — additional data needed
- **< 4/10:** No detection

### 4.3 Stage Independence

Stages 1–4 provide substantially independent lines of evidence: noise quality (Stage 1), signal existence (Stage 2), artifact elimination (Stage 3), and angular shape (Stage 4) test different physical and methodological properties. Stages 5–7 are partially correlated: temperature (Stage 7) affects decoherence rates (Stage 5), and decoherence affects field-scaling behavior (Stage 6). The scoring weights reflect this asymmetry: Stages 1–4 carry 7 of 10 points, while the correlated Stages 5–7 carry 3 points combined.

### 4.4 Control Gate

Stage 3 (Negative Controls) must pass for any positive verdict. If controls fail, the verdict is capped at "INCONCLUSIVE — ARTIFACT RISK" regardless of total score. This mechanism is adapted from blind-analysis protocols in particle physics, where data is not unblinded until control checks pass, and from clinical trial gating, where efficacy results are discounted if safety criteria are not met.

---

## 5. Simulation Validation

### 5.1 Systems Tested

QDP-1 was validated in simulation across four radical pair candidate systems and one known-negative control:

1. **Avian Cryptochrome Cry4a** — The primary magnetoreception candidate in migratory birds. Parameters: field ratio 0.05 (Earth-strength field relative to hyperfine coupling), 1000 detected photons per pulse.

2. **Flavin-Tryptophan Model Compound** — A synthetic radical pair benchmark with controlled spin chemistry. Parameters: field ratio 0.05, 2000 photons per pulse (higher yield from optimized fluorescence).

3. **Plant Cryptochrome Cry1** — An Arabidopsis cryptochrome with less-characterized magnetosensitivity. Parameters: field ratio 0.05, 800 photons per pulse (lower yield).

4. **Enzyme Radical Pair** — A donor-bridge-acceptor system with potential spin-correlated tunneling. Parameters: field ratio 0.03 (weaker coupling), 500 photons per pulse (low yield).

5. **Rhodamine B (Negative Control)** — A non-radical-pair fluorophore with no magnetic field sensitivity. Parameters: field ratio 0.0 (no spin-correlated radical pair), 1500 photons per pulse. Expected result: NO DETECTION.

### 5.2 Noise Model

Simulations include five realistic noise sources: Poisson shot noise on photon counts, LED intensity drift (σ = 0.5% per pulse), dark counts (20 counts/pulse), photobleaching (exponential decay with rate 0.1 over full measurement), and Gaussian detector read noise (σ = 5 counts). The noise model operates in the photon-counting regime with block-randomized differential measurement to cancel common-mode drift.

### 5.3 Results

**Summary verdicts:**

| System | Score | Verdict |
|--------|-------|---------|
| Avian Cryptochrome Cry4a | 7/10 | Strong evidence — recommend independent replication |
| Flavin-Tryptophan Model | 5/10 | Suggestive — additional data needed |
| Plant Cryptochrome Cry1 | 7/10 | Strong evidence — recommend independent replication |
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

3. **Stage 5 (ZNE diagnostic) scores 0/1 for all systems, including RP candidates.** The simulation's decoherence proxy (linear field-ratio reduction) does not produce the exponential decay signature the stage is designed to detect. This means the paper's most novel contribution — ZNE as a quantum biology diagnostic — is not validated even in simulation. Experimental validation with physical decoherence mechanisms (paramagnetic quenchers, temperature-driven relaxation) is essential.

4. **Stages 6–7 are stochastic across runs.** The field power law exponent (α) and temperature correlation (ρ) vary between runs for the same system, reflecting sensitivity to measurement noise. These stages provide supporting evidence but are not individually reliable.

5. **The scoring spread differentiates systems.** The range from 3/10 (negative control) to 9/10 (best RP candidate) demonstrates that the protocol produces meaningful variation, though the stochastic variation within systems (±1–2 points between runs) indicates that the verdict thresholds should be interpreted as approximate ranges rather than sharp boundaries.

### 5.4 Simulation Limitations

The simulation uses a simplified decoherence model: linear reduction of field ratio as a proxy for decoherence (Stage 5), uniform temperature coefficient (Stage 7), and power-law scaling derived from the Lorentzian singlet yield model (Stage 6). Real experimental validation would use physical decoherence mechanisms (paramagnetic quenchers, controlled temperature variation), which may produce different decay shapes. The simulation validates the *protocol logic* (scoring, gating, stage interactions), not the *physical predictions* of each stage.

---

## 6. Discussion

### 6.1 The Cross-Disciplinary Bridge

QDP-1 sits at the intersection of three established fields — quantum computing (ZNE), spin chemistry (radical pair detection), and signal processing (Fourier analysis) — and imports methodology from two additional fields (particle physics discovery criteria, clinical trial gating). The contribution is the assembly of existing techniques into a unified framework, not the invention of new measurement physics. This type of methodological contribution — where the novelty lies in the combination rather than the components — has precedent in cross-disciplinary science and is particularly valuable when it enables standardization across a fragmented experimental landscape.

### 6.2 The ZNE Adaptation: Status and Limitations

The proposed use of ZNE as a diagnostic rather than an error-mitigation tool represents the most specific novel element of QDP-1 — and also its least validated component. In standard quantum computing applications, ZNE extrapolates to zero noise to recover the ideal result. In QDP-1 Stage 5, we propose examining the *shape* of the decay curve under increasing noise as a classifier: exponential decay as a quantum-consistent signature, linear decay as classical-consistent.

**This stage is currently a hypothesis, not a validated diagnostic.** In the simulation results presented here, Stage 5 scores 0/1 across all four systems. The simulation's decoherence proxy (linear reduction of field ratio) does not produce the exponential decay signature the stage is designed to detect. This means the paper's most original contribution has not been demonstrated even in simulation.

There are additional concerns with the exponential-vs-linear classifier:

1. **Many classical processes also produce exponential decay.** Photobleaching, first-order chemical decay, and thermal relaxation are all exponential. The claim that "quantum = exponential, classical = linear" is a simplification that requires empirical validation against real systems.

2. **Deliberate decoherence perturbation may alter chemistry.** Adding paramagnetic ions or modifying the radical pair changes the chemical system, not just the spin coherence. The observed decay shape may reflect chemical changes rather than decoherence dynamics.

3. **The theoretical basis needs strengthening.** A derivation from spin dynamics showing why quantum spin coherence in radical pairs should produce a specific decay functional form under controlled decoherence — distinct from classical alternatives — would substantially strengthen this stage.

Despite these limitations, the *concept* of repurposing noise-scaling techniques from quantum computing as diagnostics for quantum biology remains promising. ZNE has already migrated from quantum computing into quantum sensing [8]; extending it to quantum biology is a natural next step. Stage 5 should be treated as a proposed diagnostic awaiting theoretical grounding and experimental validation, not as a proven technique. Its scoring weight (1 point of 10) reflects this provisional status.

### 6.3 Practical Application

To apply QDP-1 to a new radical pair system, an experimentalist defines four parameters: excitation wavelength (to create the radical pair), field ratio (applied field strength relative to hyperfine coupling), detected photons per pulse (fluorescence yield), and observable type (fluorescence intensity, transient absorption, or similar). The protocol then runs identically regardless of the specific system. Equipment requirements for the optical and magnetic components are modest: a blue LED source (~450 nm for flavin-based systems), Helmholtz coils for controlled magnetic field application, a photodetector with single-photon sensitivity, and standard temperature control. Estimated equipment cost for these components: $1,500–$4,000. However, this estimate does not include the substantial infrastructure required for biological sample preparation — purified protein expression (e.g., Cry4a), anaerobic or low-oxygen handling (O₂ quenches radical pairs), electromagnetic shielding, and sample stability management (photobleaching, batch-to-batch variability). A laboratory already equipped for radical pair biochemistry could implement QDP-1 with the listed optical/magnetic components; a lab starting from scratch would face significantly higher costs and setup time.

Each application of QDP-1 to a new radical pair candidate constitutes an independent experimental contribution. Priority targets for experimental validation include: (1) avian cryptochrome Cry4a, as the system with the strongest existing evidence base; (2) synthetic flavin-tryptophan model compounds, as controlled benchmarks; (3) plant cryptochromes, which are less studied but express in accessible organisms; and (4) enzyme radical pairs involved in oxidative stress pathways, which connect to biomedical applications.

### 6.4 Broader Implications

If QDP-1 validates experimentally and enables systematic scanning of radical pair systems, several research directions open:

**Quantum biology survey.** A standardized protocol allows direct comparison of quantum coherence signatures across systems — comparing avian, plant, and fungal cryptochromes under identical criteria, for example, or screening enzyme families for unexpected magnetosensitivity.

**Pharmacological screening.** Some pharmaceuticals (notably lithium [16]) are hypothesized to affect radical pair dynamics. QDP-1 could provide a standardized test for radical pair involvement in drug mechanisms.

**Oxidative stress and reactive oxygen species.** The radical pair mechanism governs aspects of cellular reactive oxygen species (ROS) production under magnetic field exposure [17]. Understanding which cellular processes are magnetically sensitive through radical pair mechanisms has implications for environmental electromagnetic exposure assessment.

---

## 7. Limitations

1. **Simulation only.** QDP-1 is validated in simulation, not experiment. The protocol logic is tested; the physical predictions of each stage require experimental validation with real radical pair systems.

2. **Simplified decoherence.** Stage 5 (ZNE diagnostic) uses a proxy decoherence model (linear field-ratio reduction). Real decoherence involves spin relaxation, dephasing, and environmental coupling with potentially different functional forms. The exponential vs. linear classification may need refinement against experimental data.

3. **Scoring weight calibration.** Current scoring weights are based on methodological reasoning (independence, caveat severity), not empirical calibration. Validation against known positive systems (e.g., Cry4a) and known negative systems (e.g., non-radical-pair fluorophores) would refine weights and thresholds.

4. **Partial stage correlation.** Stages 5, 6, and 7 are not fully independent — temperature affects decoherence, which affects field scaling. While scoring weights reflect this (3 of 10 points for correlated stages), a fully independent evidence framework would be stronger.

5. **Scope limitation.** QDP-1 is designed for radical pair systems specifically. Extension to other quantum biology phenomena (coherent energy transfer in photosynthesis, quantum tunneling in enzyme catalysis) would require different test stages.

6. **Exponential decay caveat.** Stage 5 cannot distinguish quantum decoherence from classical exponential processes (photobleaching, thermal decay) in isolation. Its value depends on the multi-stage context. This is by design — no single stage is intended to be conclusive.

7. **Missing standard tests.** QDP-1 does not currently include several tests that are standard in the radical pair magnetoreception literature: radiofrequency (RF) magnetic field disruption (a key test for confirming radical pair involvement [9]), isotope substitution controls (replacing magnetic nuclei to alter hyperfine coupling), or electron paramagnetic resonance (EPR) validation. These could be incorporated as additional stages in future versions.

8. **Stage 4 false positive risk.** The Fourier power ratio criterion in Stage 4 can produce spurious scores on noise-only data (observed in the Rhodamine B negative control). This stage should be conditioned on Stage 2 passing first — if no differential signal exists, the angular shape test is meaningless. This gating refinement is planned for QDP-1.1.

9. **Run-to-run variability.** Due to stochastic noise, individual system scores vary by ±1–2 points between runs. Verdict thresholds should be interpreted as approximate ranges. A future version should define verdicts based on the mean score across multiple independent runs.

---

## 8. Proposed Extensions

The following stages are not included in QDP-1 v1.0 but are standard tests in the radical pair literature and should be incorporated in future versions:

**Stage 8 (proposed): RF Magnetic Field Disruption.** Application of a weak radiofrequency magnetic field at the Larmor frequency should disrupt singlet-triplet interconversion in radical pairs, reducing the observed magnetic field effect [9]. This is one of the strongest diagnostic tests for radical pair involvement. A system that passes Stages 1–4 but shows no RF sensitivity would cast doubt on a radical pair interpretation.

**Stage 9 (proposed): Magnetic Isotope Substitution.** Replacing magnetic nuclei (e.g., ¹H → ²H, ¹²C → ¹³C) alters the hyperfine coupling and should change the angular dependence and field sensitivity in a predictable way. Agreement between predicted and observed isotope effects would provide strong evidence for spin-correlated radical pair involvement.

**Stage 10 (proposed): Direct Radical Characterization via EPR/Transient Absorption.** Time-resolved EPR or transient absorption spectroscopy can directly confirm the existence and identity of radical intermediates. While more equipment-intensive than fluorescence-based stages, this provides ground-truth evidence that complements the statistical approach of Stages 1–7.

These extensions would strengthen QDP-1 considerably but require more specialized equipment and expertise. The current seven-stage framework is designed as a first-pass screening tool; the proposed extensions would convert positive screening results into confirmatory evidence.

---

## 9. Conclusion

QDP-1 provides a structured, reproducible framework for evaluating quantum spin coherence signatures in radical pair systems. Its primary contribution is formalizing multi-stage evidence accumulation with control gating for radical pair detection — a standardization that does not currently exist in the field. The proposed ZNE diagnostic (Stage 5) represents a speculative but potentially valuable cross-disciplinary transfer that requires theoretical grounding and experimental testing before it can be considered a reliable component.

The framework is validated in simulation only. The simulation validates protocol mechanics (scoring logic, gating, system differentiation) but does not validate that the stages reliably probe quantum coherence in real biological systems, where decoherence is rapid and confounders are abundant. QDP-1 in its current form is a methodological proposal — a structured starting point for standardization — not a battle-tested detection kit. Its value will be determined by experimental validation against known positive and negative systems, integration with established techniques (magneto-fluorescence fluctuation methods, transient absorption, EPR), and collaborative stress-testing by the spin chemistry and quantum biology communities.

We invite collaboration from experimental groups working with radical pair systems and will make the simulation code publicly available for community review.

---

## References

[1] Maeda, K., et al. (2012). Magnetically sensitive light-induced reactions in cryptochrome are consistent with its proposed role as a magnetoreceptor. *PNAS*, 109(13), 4774–4779.

[2] Xu, J., et al. (2021). Magnetic sensitivity of cryptochrome 4 from a migratory songbird. *Nature*, 594, 535–540.

[3] Wedge, C. J., et al. (2025). Direct observation of a long-lived flavin/tryptophan radical pair in cryptochrome. *Communications Chemistry*, 8, 45.

[4] Lindner, S., et al. (2024). Magneto-fluorescence fluctuation microspectroscopy for investigating quantum effects in biology. *Nature Photonics*, 19, 177–183.

[5] Kerpal, C., et al. (2019). Chemical compass behaviour at microtesla magnetic fields strengthens the radical pair hypothesis of avian magnetoreception. *Nature Communications*, 10, 3707.

[6] Temme, K., Bravyi, S., & Gambetta, J. M. (2017). Error mitigation for short-depth quantum circuits. *Physical Review Letters*, 119, 180509.

[7] Giurgica-Tiron, T., et al. (2020). Digital zero noise extrapolation for quantum error mitigation. *IEEE International Conference on Quantum Computing and Engineering*, 306–316.

[8] Van Dyke, J. S., White, Z., & Quiroz, G. (2024). Mitigating errors in DC magnetometry via zero-noise extrapolation. *Physical Review Applied*, 22, 024062. arXiv:2402.16949.

[9] Hore, P. J., & Mouritsen, H. (2016). The radical-pair mechanism of magnetoreception. *Annual Review of Biophysics*, 45, 299–344.

[10] Bradlaugh, A. A., et al. (2023). Magnetic field effects on radical pair reactions: estimation of B_1/2 for flavin-tryptophan radical pairs in cryptochromes. *Physical Chemistry Chemical Physics*, 25, 3468–3477. DOI: 10.1039/D2CP03793A.

[11] Ritz, T., et al. (2000). A model for photoreceptor-based magnetoreception in birds. *Biophysical Journal*, 78(2), 707–718.

[12] Timmel, C. R., et al. (1998). Effects of weak magnetic fields on free radical recombination reactions. *Molecular Physics*, 95(1), 71–89.

[13] Dodson, C. A., et al. (2013). Fluorescence-detected magnetic field effects on radical pair reactions from femtolitre volumes. *Chemical Communications*, 49, 1732–1734.

[14] Cai, J., Guerreschi, G. G., & Briegel, H. J. (2020). How quantum is radical pair magnetoreception? *Faraday Discussions*.

[15] Chee, J., et al. (2024). Simulating spin biology using a digital quantum computer. *APL Quantum*, 1, 036117.

[16] Zadeh-Haghighi, H., & Simon, C. (2021). Radical pairs can explain magnetic field and lithium effects on the circadian clock. *Scientific Reports*, 12, 269.

[17] Hore, P. J. (2025). Magneto-oncology: A radical pair primer. *Frontiers in Oncology*, 15, 1539718. DOI: 10.3389/fonc.2025.1539718.

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

1. **Excitation wavelength** — What creates the radical pair?
2. **Field ratio** — Applied field strength / hyperfine coupling constant
3. **Detected photons per pulse** — Expected fluorescence yield
4. **Observable** — Fluorescence intensity, transient absorption, or other readout
5. **Decoherence control method** — How will decoherence be deliberately varied for Stage 5? (paramagnetic ions, temperature, chemical modification)
6. **Negative control method** — How will the radical pair be eliminated for Stage 3 Control C3? (radical scavenger, denatured protein, knockout mutant)

Run all seven stages with ≥5,000 pulses per measurement condition. Report all stage scores, control Z-values, and final verdict.
