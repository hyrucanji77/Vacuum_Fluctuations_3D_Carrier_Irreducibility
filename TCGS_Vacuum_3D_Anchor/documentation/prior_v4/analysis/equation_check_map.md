# Numerical companion: equation-to-check map (revision v4)

This map accompanies the patched `reproduce.py`. All **515 named parameter-case checks** pass: **509 analytic or model checks**, **4 arithmetic sanity checks**, and **2 printed-value consistency checks**. These are not 515 independent propositions or experimental observations. The six auxiliary checks are counted separately and are not presented as evidence for a scientific claim.

## Run

Save `reproduce.py` in a writable folder and run `python reproduce.py`. From the Overleaf/research package root, run `python analysis/reproduce.py`. Python 3.10 or later is sufficient; only standard-library modules are imported. Outputs are written beside the script. No network, experimental images, or repository credentials are needed.

## Check coverage

| Group | Parameter cases | Category | Manuscript location | What is checked |
|---|---:|---|---|---|
| Harmonic saturation | 1 | `analytic_check` | Eq. (18), using Eqs. (7) and (9) | Compares the ground-state kinetic energy with the finite-width lower bound. |
| Printed-value consistency: aspect ratio | 1 | `printed_value_consistency` | Section 7.1 | Checks only the printed digits 0.0154; not an independent analytic identity. |
| Effective interaction identity | 1 | `analytic_check` | Eq. (13) | Compares the two algebraic expressions for the Gaussian-overlap coupling. |
| Arithmetic sanity: common-factor cancellation | 4 | `arithmetic_sanity` | Proposition 14.1; Eq. (59) | Exercises (lambda*a)/(lambda*ell)=a/ell. This is only an arithmetic sanity check, not an independent test of Proposition 14.1; see the scale_row-based matched-carrier family below. |
| Mode covariance and readout | 180 | `analytic_check` | Eqs. (26), (31), (34), (36), (39), (40), (64), (65), and (71) | Uses w=sqrt(a*(a+2)) and tests the specified covariance, readout and quench identities. Eq. (48) and the Josephson limit are now tested in separate named groups. |
| Quench determinant | 144 | `analytic_check` | Appendix A, Eqs. (67)--(69) | Evaluates the displayed covariance components and checks determinant preservation on the finite parameter grid. |
| Local spectral slope | 5 | `analytic_check` | Eqs. (45)--(46) | Compares the analytic slope with a centred logarithmic finite difference at five positive values. |
| Fixed-scattering confinement scaling | 8 | `analytic_check` | Eqs. (63), (75); Table 4 | Checks square-root width scaling and linear kinetic-energy scaling. |
| Scaled readout-to-gap ratio | 1 | `analytic_check` | Eq. (21a); Table 2 | Checks the nominal 12.96 value from the declared inputs. |
| Printed-value consistency: unscaled Rabi ratio | 1 | `printed_value_consistency` | Eq. (21a); Table 2 | Checks only the printed digits 11.0, not a separate analytic identity. |
| Conditional axial thermal benchmark | 8 | `analytic_check` | Eq. (21b) | Checks normalization, the excited tail, p1/p0, and the mean of an independent canonical oscillator at 6 and 12 nK. |
| Mean-field balance | 18 | `analytic_check` | Section 7.2, unnumbered mean-field equations | Checks the imbalance-dependent potential difference and the balanced common potential; does not certify actual transverse profiles. |
| Transverse profile overlaps | 14 | `analytic_check` | Section 5.1, unnumbered overlap formulas | Compares explicit Gaussian-profile overlaps with Simpson quadrature and checks complementary overlap bounds. |
| Matched-carrier feasibility | 29 | `analytic_check` | Eqs. (59), (59a); finite-resource scaling | Checks finite matching transformations, the lambda-squared spin/gap ratio, localization cost, and the illustrative lambda <= 1/3 screen. |
| Finite-pulse bound | 60 | `analytic_check` | Appendix B, Eq. (74a) | Checks the amplitude inequality for exactly solvable two-sector constant toy Hamiltonians, not the actual experimental pulse. |
| Expanded versus factorized dispersion | 16 | `dispersion_identity` | Eq. (48), compared with Eqs. (24) and (26) | Computes all three SI terms of Eq. (48), divides by (mu_s_prime/hbar)^2, and compares with (e+q)(e+q+2); e=epsilon_k/mu_s_prime, q=hbar*Omega_prime/mu_s_prime. Includes a polynomial zero-mode check, not a normalizable-vacuum claim. |
| Josephson-limit relative error and convergence | 24 | `josephson_limit` | Eq. (49), compared with the exact dispersion in Eqs. (26)/(48) | On four rays at scales 0.1, 0.01, 0.001, checks squared-frequency relative error (e+q)/(2+e+q), its upper bound (e+q)/2, and nonincrease relative to the preceding scale. Twelve error-identity checks and twelve bound/convergence checks; finite cases, not proof of the asymptote. |

## Exact dispersion and Josephson-limit checks

The new `dispersion_checks()` block uses the dimensionless variables

`e = epsilon_k / mu_s_prime`, `q = hbar*Omega_prime / mu_s_prime`,

and independently evaluates the SI expansion

`Omega_prime*(Omega_prime + 2*mu_s_prime/hbar) + (mu_s_prime + hbar*Omega_prime)*k^2/m + hbar^2*k^4/(4*m^2)`.

After division by `(mu_s_prime/hbar)^2`, it is compared with `(e+q)*(e+q+2)` at 16 pairs: `e in [0, 0.02, 0.5, 2]`, `q in [0, 0.04, 1, 20]`. The joint zero is an algebraic polynomial identity only; it is not included in the oscillator-vacuum covariance calculation.

For Eq. (49), the code computes the SI gap-plus-sound expression and compares it with the exact squared frequency on rays `(e0,q0)=(1,0),(0,1),(1,1),(1,2)`, each multiplied by `0.1, 0.01, 0.001`. With `s=e+q>0`, the relative **squared-frequency** error is `s/(2+s)`, bounded by `s/2`. The successive-scale checks require nonincreasing error as well as that bound. All new cases use the existing tolerance `2e-11` (relative for identities; absolute slack for upper bounds).

## Source-to-code traceability

Zhang et al., arXiv:2608.20311v1, Supplementary Materials, p. 5, report scattering lengths approximately `31 a0`, `-53 a0`, and `220 a0` at `B approximately 58.1 G`. Under the common-profile reduction the coupling ratios are the same. Section 8.1 now states these values explicitly. In `revision_checks()` an arbitrary common coupling prefactor is set to one: `guu,gud,gdd = 31,-53,220`. The derived value is `Z0=(220-31)/(31+220-2*(-53))=9/17`, approximately `0.5294117647`. The code's exact ratio is an algebraic consequence of rounded source inputs, not an exact measured imbalance. It does not replace the explicitly rounded `ALPHA=0.72` source convention.

## Outputs and limits

`analytic_checks.json` contains every named case, category, actual and expected values or bounds, error, tolerance, and pass status. It retains `checks` as the total record count for compatibility and adds `analytic_or_model_checks`, `auxiliary_checks`, and `counts_by_category`. Its `max_relative_error` is a reporting summary; absolute-tolerance and upper-bound cases must be read using their declared metrics, not as relative-tolerance tests.

`nominal_scales.json` and `confinement_family.csv` are byte-identical to v3. All 475 earlier assertion values, errors, tolerances and pass statuses are unchanged. Only six old case names were corrected and the category field added; forty direct dispersion/limit cases were appended. The actual matched-carrier implementation checks still pass through `scale_row(FZ/lambda**2)` in `revision_checks()`.

The nominal widths, gap and zero-point values are model calculations, not new measured thicknesses. The standard-error examples for M=70/120 and the finite-readout value sqrt(1.1) are computed outputs, not additional counted assertions.

The script does not independently test every manuscript result. It contains no direct numerical check of the transverse form factor in Eq. (60), binomial thinning in Eq. (52), Horava's spectral-dimension formula, the general operator assumptions behind the Feshbach or Duhamel bounds, the full metrological covariance formulas in Eqs. (76)--(77), or a constructed Counterspace response. It does not fit raw images, determine experimental transverse populations, or certify common profiles during the pulse. These remain analytic arguments, source claims, or stated construction requirements in the manuscript.
