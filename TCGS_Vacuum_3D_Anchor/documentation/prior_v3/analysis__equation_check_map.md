# Numerical companion: equation-to-check map

This map accompanies the unchanged `reproduce.py` from revision v2, redistributed with revision v3. All 475 named parameter-case checks pass. The count is not a count of independent propositions, and finite-grid testing is not a proof of the general formulas.

## Run

Save `reproduce.py` in a writable folder and run:

```bash
python reproduce.py
```

From the Overleaf/research package root, use `python analysis/reproduce.py`. Python 3.10 or later is sufficient; only standard-library modules are imported. Outputs are written beside the script. No network, experimental images, or repository credentials are needed.

## Check coverage

| Group | Parameter cases | Manuscript location | What is checked |
|---|---:|---|---|
| Harmonic saturation | 1 | Eq. (18), using Eqs. (7) and (9) | Compares the ground-state kinetic energy with the finite-width lower bound. |
| Rounded aspect ratio | 1 | Section 7.1 | Checks the manuscript's rounded oscillator-length-to-box-side ratio. |
| Effective interaction identity | 1 | Eq. (13) | Compares the two algebraic expressions for the Gaussian-overlap coupling. |
| Planar coupling degeneracy | 4 | Proposition 14.1; Eq. (59) | Checks a/ell invariance for four finite matching transformations. |
| Mode covariance and readout | 180 | Eqs. (26), (31), (34), (36), (39), (40), (64), (65), and (71) | Evaluates the dimensionless dispersion and tests covariance/readout identities over specified a, N, and angle values. The dispersion is an input formula, not independently derived by the script. |
| Quench determinant | 144 | Appendix A, Eqs. (67)--(69) | Evaluates the displayed covariance components and checks determinant preservation on the finite parameter grid. |
| Local spectral slope | 5 | Eqs. (45)--(46) | Compares the analytic slope with a centred logarithmic finite difference at five positive values. |
| Fixed-scattering confinement scaling | 8 | Eqs. (63), (75); Table 4 | Checks square-root width scaling and linear kinetic-energy scaling. |
| Readout-to-gap ratios | 2 | Eq. (21a); Table 2 | Checks 12.96 and the rounded unscaled ratio 11.0 from the declared inputs. |
| Conditional axial thermal benchmark | 8 | Eq. (21b) | Checks normalization, the excited tail, p1/p0, and the mean of an independent canonical oscillator at 6 and 12 nK. |
| Mean-field balance | 18 | Section 7.2, unnumbered mean-field equations | Checks the imbalance-dependent potential difference and the balanced common potential; does not certify actual transverse profiles. |
| Transverse profile overlaps | 14 | Section 5.1, unnumbered overlap formulas | Compares explicit Gaussian-profile overlaps with Simpson quadrature and checks complementary overlap bounds. |
| Matched-carrier feasibility | 29 | Eqs. (59), (59a); finite-resource scaling | Checks finite matching transformations, the lambda-squared spin/gap ratio, localization cost, and the illustrative lambda <= 1/3 screen. |
| Finite-pulse bound | 60 | Appendix B, Eq. (74a) | Checks the amplitude inequality for exactly solvable two-sector constant toy Hamiltonians, not the actual experimental pulse. |

## Outputs and limits

`analytic_checks.json` contains each named check, actual and expected values or bounds, error, tolerance, and pass status. `nominal_scales.json` contains the declared inputs, nominal oscillator quantities, readout ratios, conditional thermal estimates, profile-overlap examples, and illustrative feasibility cases. `confinement_family.csv` reproduces the harmonic sweep used for Table 4.

The nominal widths, gap and zero-point values are model calculations, not new measured thicknesses. The standard-error examples for M=70/120 and the finite-readout value sqrt(1.1) are computed outputs, not additional counted assertions. The dimensionless dispersion is evaluated as sqrt(a*(a+2)) when forming the covariance tests.

The script does not independently test every manuscript result. In particular, it contains no direct numerical check of the transverse form factor in Eq. (60), binomial thinning in Eq. (52), Hořava's spectral-dimension formula, the general operator assumptions behind the Feshbach or Duhamel bounds, the full metrological covariance formulas in Eqs. (76)--(77), or a constructed Counterspace response. It does not fit raw images, determine experimental transverse populations, or certify common profiles during the pulse. These remain analytic arguments, source claims, or stated construction requirements in the manuscript.

The 344 earlier parameter cases and all 131 cases added in v2 are preserved, with no changes to the executable file or its three regenerated outputs in v3.
