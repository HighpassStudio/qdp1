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

## 2. The Rate Distribution rho(u): Explicit Series Expansion

The function phi(s) = exp[-(s/tau)^beta] with 0 < beta <= 1 has an inverse
Laplace transform rho_beta(u) that is a positive, normalized density:

    exp[-(d/tau)^beta] = integral_0^inf rho_beta(u) exp(-u d) du

There is no elementary closed-form expression for rho(u), but there is a
well-known explicit infinite series derived via term-by-term inversion of
the Bromwich integral.

### 2.1 Sine series (preferred for numerical evaluation)

This form arises from the reflection formula of the Gamma function and is
numerically stable:

    rho_beta(u) = (1 / pi u) * sum_{n=1}^{inf} (-1)^{n-1} * (u^{n beta} / n!) * sin(pi n beta)

For general scale tau:

    rho(u; tau, beta) = (1/tau) * rho_beta(u/tau)

### 2.2 Gamma-function series (Mainardi-function form)

Equivalent form from direct series expansion of exp(-s^beta):

    rho(u) = u^{-1} * sum_{n=1}^{inf} (-1)^n / (n! * Gamma(1 - n beta)) * u^{-n beta}

The two series are mathematically identical (via Gamma(z) sin(pi z) = pi / Gamma(1-z))
but the sine version is preferred in computation because it avoids poles of the
Gamma function for integer n when beta is rational.

### 2.3 Special case beta = 1

When beta = 1, the sine terms vanish (sin(pi n) = 0 for all integer n) and the
distribution collapses to the Dirac delta:

    rho(u) -> delta(u - 1/tau)

recovering the pure exponential decay C(d) = C_0 exp(-d/tau) derived in
Section 1.

### 2.4 Properties and convergence

- rho(u) > 0 for all u > 0 and integrates to 1.
- For beta < 1 the distribution is broad, asymmetric, and heavy-tailed
  (slow components at small u, fast components at large u).
- The series converges for any u > 0; practical truncation at n ~ 20-100
  terms gives high accuracy (error < 10^{-10} is routine with double precision).
- rho(u) corresponds to one-sided Levy-stable distributions for certain beta
  values.
- In the QDP-1 context, this rho(u) encodes the heterogeneous decoherence
  typical of biological radical pairs (protein sub-states, solvent fluctuations,
  nuclear-spin baths).

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
