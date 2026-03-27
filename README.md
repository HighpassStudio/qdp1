# QDP-1: Quantum Detection Protocol v1

A multi-stage framework for detecting quantum spin coherence signatures in radical pair systems under ambient conditions.

## What is this?

QDP-1 is a seven-stage detection protocol that combines techniques from quantum computing (zero-noise extrapolation), spin chemistry (angular dependence, field scaling), signal processing (Fourier decomposition), and particle physics (5-sigma thresholds, control gating) into a single scored framework for evaluating whether a radical pair system exhibits quantum spin coherence.

This is a **methodological proposal**, not a proven detection kit. It is validated in simulation only and is intended as a starting point for community evaluation and refinement.

## Quick start

```bash
python qdp1_formal.py
```

No dependencies beyond Python 3.6+ standard library.

This runs the full 7-stage protocol across 5 systems (4 radical pair candidates + 1 negative control) and outputs scored verdicts.

## Files

| File | Description |
|------|-------------|
| `qdp1_formal.py` | Complete 7-stage protocol implementation |
| `QDP1_PAPER.md` | Full paper draft |
| `QDP1_SPEC.md` | Formal specification |
| `supporting/` | Development simulations (Bell tests, biological entanglement, radical pair models) |

## The protocol

| Stage | Test | Points |
|-------|------|--------|
| 1 | Baseline noise characterization | 1 |
| 2 | Differential angular detection (5-sigma) | 2 |
| 3 | Negative controls **[GATE]** | 2 |
| 4 | Fourier angular shape (cos^2) | 2 |
| 5 | Noise decay fingerprint (ZNE diagnostic) | 1 |
| 6 | Field-strength power law | 1 |
| 7 | Temperature coherence scaling | 1 |
| | **Total** | **10** |

**Verdicts:** >=8 Consistent | >=6 Strong evidence | >=4 Suggestive | <4 No detection

Stage 3 is a gate: if controls fail, the verdict is capped regardless of score.

## Known limitations

- **Simulation only** -- experimental validation needed
- **Stage 5 (ZNE) scores 0/1 across all systems** -- the decoherence proxy does not trigger the expected exponential decay; this stage is a hypothesis, not a validated diagnostic
- **Scoring thresholds are not empirically calibrated** -- they need validation against known positive and negative systems
- See Section 7 of the paper for full limitations

## Citation

If you use or reference this work:

```
Loomis, B. (2026). QDP-1: A Multi-Stage Framework for Detecting Quantum Spin
Coherence in Radical Pair Systems. arXiv preprint [ID to be added].
```

## License

MIT
