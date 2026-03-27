# Stage 5 Theoretical Foundation: Stretched Exponential Derivation

## Supplementary material for QDP-1

This document provides the full mathematical derivation of the stretched exponential
(Kohlrausch-Williams-Watts) decay form used in QDP-1 Stage 5. The main paper
(Section 3.5.1-3.5.2) contains a condensed version; this is the complete treatment.

---

## 1. Superposition of Exponentials via Laplace Transform

Consider a heterogeneous ensemble of radical pairs. Each sub-ensemble relaxes
with its own dephasing rate u:

    C_u(d) = C_0 exp(-u d)

where d is the controlled decoherence parameter in Stage 5.

If rates u follow a probability density rho(u), the ensemble-averaged contrast is:

    C(d) = C_0 integral_0^inf rho(u) exp(-u d) du

This is the Laplace transform of rho(u) evaluated at s = d:

    C(d) / C_0 = L{rho}(d)

The stretched exponential emerges when the inverse Laplace transform of
exp[-(s/tau)^beta] yields a physically plausible rho(u) for disordered systems.

## 2. The Rate Distribution rho(u)

The function phi(s) = exp[-(s/tau)^beta] with 0 < beta <= 1 has an inverse
Laplace transform rho_beta(u) that is a positive, normalized density:

    exp[-(d/tau)^beta] = integral_0^inf rho_beta(u) exp(-u d) du

For beta = 1: rho(u) = delta(u - 1/tau), recovering pure exponential.

For beta < 1: rho_beta(u) is a broad, asymmetric distribution with:
- A peak at lower rates (slow-decaying components)
- A long tail toward higher rates (fast-decaying components)

This corresponds to one-sided Levy-stable distributions for certain beta values.

## 3. Physical Origin in Radical Pair Systems

Decoherence in biological radical pairs arises from multiple channels:
- Random local magnetic fields (nuclear spins, solvent)
- Conformational fluctuations modulating hyperfine/exchange couplings
- Singlet-triplet dephasing
- T1/T2 relaxation processes

These channels are heterogeneous: different protein sub-states experience
different local environments, producing a distribution of rates rather than
a single gamma. When the control parameter d linearly increases noise strength
across the ensemble, the observed contrast follows the Laplace transform of rho(u).

This is why stretched exponentials (beta ~ 0.6-0.9) frequently appear in
experimental spin relaxation and magnetization decay in organic radicals
and proteins.

## 4. Connection to CTRW and Fractional Dynamics

Alternative derivation from continuous-time random walk (CTRW) models:
- Waiting times between relaxation events follow psi(tau) ~ tau^{-(1+alpha)}
- The survival probability satisfies a fractional master equation
- In the long-time limit: stretched exponential with beta related to alpha

In radical pairs, slow conformational modes or nuclear spin diffusion induce
such anomalous (non-Markovian) dynamics, yielding stretched-exponential
coherence loss.

## 5. Implications for Stage 5

The Laplace-transform origin explains why the decay shape diagnostic works
in principle:

- Delta-like rho(u) -> pure exponential (homogeneous quantum dephasing)
- Broad rho(u) -> stretched exponential (disordered quantum system)
- Non-Laplace form (linear) -> classical scaling

The inverse problem (recovering rho(u) from C(d) via numerical inverse
Laplace transform) is ill-posed but feasible and has been applied in
luminescence and NMR relaxation studies.

## References

- Kohlrausch, R. (1854). Theorie des elektrischen Ruckstandes in der Leidener Flasche.
- Williams, G. & Watts, D. C. (1970). Non-symmetrical dielectric relaxation behaviour
  arising from a simple empirical decay function. Trans. Faraday Soc., 66, 80-85.
- Montroll, E. W. & Weiss, G. H. (1965). Random walks on lattices. II. J. Math. Phys., 6, 167.
- Metzler, R. & Klafter, J. (2000). The random walk's guide to anomalous diffusion.
  Physics Reports, 339, 1-77.
