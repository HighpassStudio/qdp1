# QDP-1: A Multi-Stage Framework for Detecting Quantum Spin Coherence in Radical Pair Systems

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue) ![Status: Simulation Only](https://img.shields.io/badge/Status-Simulation%20Only-orange)

**Methodological proposal** — simulation-validated only. Not yet an experimentally proven detection kit.

---

**Contents:** [Overview](#overview) | [Quick Start](#quick-start) | [The Protocol](#the-protocol) | [What You'll See](#what-youll-see) | [Limitations](#current-status--limitations) | [Apply to Your System](#applying-qdp-1-to-a-new-radical-pair-system) | [Collaborate](#collaboration-welcome) | [Citation](#citation)

QDP-1 unifies angular dependence testing, field scaling, temperature dependence, negative control gating, and a proposed ZNE-based noise-decay diagnostic into a single scored 10-point protocol. Stage 3 (negative controls) acts as a hard gate.

## Overview

QDP-1 provides a standardized, system-agnostic protocol for evaluating signatures *consistent with* quantum spin coherence in radical pair (RP) systems under ambient conditions. It draws techniques from quantum computing (ZNE), spin chemistry, signal processing, and particle physics.

The framework is designed to be reproducible and directly applicable to cryptochromes, synthetic flavin-tryptophan models, or other RP candidates.

## Quick Start

```bash
git clone https://github.com/HighpassStudio/qdp1.git
cd qdp1
python qdp1_formal.py
```

No external dependencies. Python 3.6+ standard library only. Runs in ~2 minutes.

## Repository Contents

| File | Description |
|------|-------------|
| `qdp1_formal.py` | Complete 7-stage protocol implementation |
| `QDP1_PAPER.md` | Full paper draft (rev02, 17 references, 3 appendices) |
| `QDP1_SPEC.md` | Formal specification |
| `sample_output.txt` | Example output from a full run |
| `LICENSE` | MIT License |
| `supporting/STAGE5_THEORY.md` | Full theoretical derivation for Stage 5 (Lindblad, KWW, Laplace transform) |
| `supporting/*.py` | Development simulations (Bell tests, radical pair models, experiment design) |

## The Protocol

| Stage | Test | Points |
|-------|------|--------|
| 1 | Baseline noise characterization | 1 |
| 2 | Differential angular detection (5-sigma) | 2 |
| 3 | Negative controls **[GATE]** | 2 |
| 4 | Fourier angular shape (cos^2 via 2-theta power) | 2 |
| 5 | Noise decay fingerprint (ZNE diagnostic) | 1 |
| 6 | Field-strength power law | 1 |
| 7 | Temperature coherence scaling | 1 |
| | **Total** | **10** |

**Verdicts:** >=8 Consistent | >=6 Strong evidence | >=4 Suggestive | <4 No detection

**Key innovations:**
- **Control gate (Stage 3):** If negative controls fail, the verdict is capped at "INCONCLUSIVE" regardless of score — adapted from particle physics blind-analysis protocols.
- **ZNE diagnostic (Stage 5):** Proposes adapting zero-noise extrapolation from quantum computing as a quantum biology diagnostic. *Caveat: this stage is a hypothesis — it scores 0/1 in simulation and awaits theoretical and experimental validation.*
- **Fourier angular analysis (Stage 4):** Uses 2-theta Fourier power to detect cos^2 angular dependence, more robust than direct curve fitting.

## What You'll See

### Summary table

```
QDP-1 SUMMARY — ALL SYSTEMS

System                            Score  Verdict
------------------------------  -------  ------------------------------
Avian Cryptochrome Cry4a         8/10   CONSISTENT WITH QUANTUM SPIN COHERENCE
Flavin-Tryptophan Model          5/10   SUGGESTIVE — additional data needed
Plant Cryptochrome Cry1          7/10   STRONG EVIDENCE — recommend independent replication
Enzyme Radical Pair              7/10   STRONG EVIDENCE — recommend independent replication
Rhodamine B (Negative Control)   3/10   NO DETECTION
```

### Stage-by-stage breakdown (one system)

```
QDP-1: Avian Cryptochrome Cry4a
field_ratio=0.05  photons=1000

[1/7] BASELINE      ENR=1.30x  drift=-4.8%  shot-limited     [1/1]
[2/7] DIFFERENTIAL  contrast=-0.022631  Z=66.1               [2/2]
[3/7] CONTROLS      ALL CLEAN                                [2/2]
       Same angle (0 vs 0)       z=1.2
       No field                  z=1.0
       Killed pair               z=0.1
[4/7] ANGULAR SHAPE  cos2_power=0.527  R2=0.988  F=1943.6    [2/2]
[5/7] NOISE DECAY    linear  linR2=0.965  expR2=0.361        [0/1]
[6/7] FIELD SCALING  B^1.31  quantum-like                     [1/1]
[7/7] TEMPERATURE    rho=-0.595  quantum-like                 [1/1]

SCORE: 8/10 (80%)
VERDICT: CONSISTENT WITH QUANTUM SPIN COHERENCE
```

Scores vary +/-1-2 points between runs due to stochastic noise (realistic). Full output with decay curves and field scaling data is in [sample_output.txt](sample_output.txt).

## Current Status & Limitations

- **Simulation-only validation.** The code correctly implements protocol *logic*, but physical predictions require real experiments.
- **Stage 5 (ZNE diagnostic)** scores 0/1 in the current simulation because the linear decoherence proxy does not produce exponential or stretched-exponential decay. This stage remains a hypothesis awaiting theoretical refinement and experimental testing.
- Scoring thresholds and verdict cutoffs are provisional and need empirical calibration against known positive and negative systems.
- Stage 4 (Fourier power) can occasionally produce spurious partial scores on noise-only data.

Full discussion is in Section 7 of [QDP1_PAPER.md](QDP1_PAPER.md).

## Applying QDP-1 to a New Radical Pair System

1. Modify the system parameters in `qdp1_formal.py` (or create a new configuration):
   - Excitation wavelength / radical pair creation method
   - Field ratio (B / hyperfine coupling)
   - Expected photons per pulse (fluorescence yield)
   - Decoherence control method for Stage 5 (paramagnetic ions, temperature, etc.)

2. Implement the fluorescence (or transient absorption) readout.

3. Run >= 5,000 pulses per condition as recommended.

See [QDP1_SPEC.md](QDP1_SPEC.md) and Appendix C of the paper for the full application checklist.

### Decoherence controls for Stage 5

| Method | Mechanism | Notes |
|--------|-----------|-------|
| Paramagnetic ions (Gd3+, Mn2+) | Increases spin relaxation | May alter chemistry |
| Temperature variation | Accelerates thermal fluctuations | +/- 10-30 K; watch for denaturation |
| Viscosity variation (glycerol) | Modulates molecular tumbling | Less invasive |

### Negative controls for Stage 3

| Method | Use case |
|--------|----------|
| Radical scavenger (ascorbic acid) | General |
| Protein denaturation | Protein-based systems |
| Knockout mutant | In vivo |
| Non-RP fluorophore (Rhodamine B) | Benchmark |

## Collaboration Welcome

We particularly seek:
- Experimental runs of **Stage 2** (differential angular detection) on real cryptochrome or flavin-tryptophan samples.
- Feedback on Stage 5 (better decoherence models or alternative fingerprints).
- Suggestions for incorporating standard RP tests (RF disruption, isotope effects, EPR).

Feel free to open issues, submit pull requests, or contact the author for potential joint experiments.

Priority experimental targets: synthetic FAD-Trp models (easiest entry point) and avian/plant cryptochromes.

## Citation

If you use QDP-1 or the simulation code, please cite:

```
Loomis, B. (2026). QDP-1: A Multi-Stage Framework for Detecting Quantum Spin
Coherence in Radical Pair Systems. arXiv preprint [arXiv ID to be added after upload].
```

Paper draft: [QDP1_PAPER.md](QDP1_PAPER.md) | Formal spec: [QDP1_SPEC.md](QDP1_SPEC.md) | Stage 5 theory: [supporting/STAGE5_THEORY.md](supporting/STAGE5_THEORY.md)

## Built With

Written in pure Python (standard library only). Designed to be easy to extend or port to lab control software.

## License

MIT — see [LICENSE](LICENSE)
