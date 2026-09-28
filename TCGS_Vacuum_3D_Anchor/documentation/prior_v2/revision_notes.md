# Surgical revision of the vacuum-fluctuation carrier paper

## Scope and preservation

MODE B — SURGICAL UPDATE OF EXISTING .TEX. The existing title is retained. Explicit sentences in the abstract and introduction identify the theorem as a dimension-independent non-collapse result applied to the independently specified three-dimensional carrier; the number three is not inferred from the one-coordinate uncertainty bound.

All 105 original label values, all 78 original equation numbers, all original section and subsection headings in their original order, four propositions, four tables, the author block, keywords, and the complete 25-entry bibliography are preserved. The bodies of equations (50) and (78) receive only the necessary notation/typing correction; the other 76 existing displayed equation bodies are byte-identical. Added tagged equations use suffixes rather than renumbering.

## Resolution of the review

1. **Dimension versus non-collapse.** The abstract, introduction, and proof discussion distinguish dimension-independent finite-energy persistence from A3's carrier-dimensional assignment. No title change or universal dimensional theorem is introduced.

2. **Source-normal direction.** New Section 3.5 separates a spatial massive-particle mode projection from an immersion/pullback and constitutive Counterduction. Merely being non-temporal is not the reason for the distinction: the atomic z coordinate is itself spatial. The relevant absence is a specified source-normal canonical pair, kinetic-energy operator, normalized profile, and reduction theorem. Source dependence may still survive in induced fields and extrinsic data. Section 17.6 makes the positive candidate a calibrated, source-derived statistical response, not an assumed Gaussian source width.

3. **Strong readout.** Table 2 and equation (21a) show the scaled ratio 12.96 and unscaled ratio approximately 11.0. Section 5.1 gives the exact common-profile RF selection rule and its unequal-profile overlap replacement. Section 7.2 distinguishes that rule from full interacting-pulse inertness. It also records an important qualification: unequal interaction coefficients do not by themselves destroy common equilibrium profiles at Z0, because the differential mean-field interaction potential vanishes there. Actual deviations and finite-pulse coupling require a bound or measurement. Appendix B adds a Duhamel leakage-amplitude bound without assuming that the bare trap gap is the full dressed spectral gap.

4. **Map composition.** Equation (4a) defines Pi_sigma = M o R_eff o Ctd. Constitutive output is the physical atomic carrier state. The optical stage alone is M_OD in (50). Equation (78) uses the same maps. Section 13.1 additionally distinguishes an actual-outcome map, which permits the inverse-image probability in (58), from a density-matrix measurement kernel, which returns a probability law. The differentiable response in Section 17.6 acts on statistical predictions, not discontinuous individual outcomes.

5. **Singular set.** Section 3.1 explicitly retains S as source background but notes that no explicit S-dependent contribution is used in the carrier-energy or oscillator calculation. No singular signature is claimed as measured.

6. **Conditional axial thermal estimate.** Equation (21b) gives the canonical independent-oscillator tail, conditional on T_z = T_spin: 3.36e-4 at 6 nK and 1.83e-2 at 12 nK. The mean oscillator excitation is distinguished from that tail. Neither value is presented as a measured many-body Bose-gas transverse excited fraction, and 12 nK is not asserted to be a certified upper bound.

7. **Feasible matching direction.** Equation (59a) gives ratios 0.900 lambda^2 and 0.648 lambda^2. Finite lambda < 1 improves the hierarchy but does not automatically make it asymptotic. For a screening threshold epsilon_star=0.1, lambda <= 1/3 is required for the unscaled spin/gap ratio. Matrix-element checks remain necessary. The lambda -> 0 infinite-resource limit is excluded from the empirical construction.

8. **Numerical companion.** The original script was present at analysis/reproduce.py in the preceding full research archive, but not in the smaller Overleaf ZIP. Both new ZIPs now include the executable supplement and generated reports. No unverified repository pointer is introduced. The same standard-library script preserves the 344 original test records exactly and adds 131 checks.

## Source verification

The supplied arXiv:2608.20311v1 PDF remains the authority for the nominal 1 kHz transverse confinement, 900/120 Hz interaction scales, alpha approximately 0.72, the readout factor 20, and the 6 +/- 6 nK spin fit. The added 12.96 and 11.0 ratios are calculations from these rounded inputs.

The primary precursor, arXiv:2603.08840v2, explicitly states that the interaction chemical potentials coincide at Z=Z0 and that this decouples density and spin fluctuations to leading order. Its full HTML was consulted for that qualification:
https://arxiv.org/html/2603.08840v2
The experimental paper was also checked in primary-source HTML:
https://arxiv.org/html/2608.20311v1
No precursor dataset is substituted for the nominal values in the vacuum-imaging paper.

The source-map hierarchy follows the independently cited foundation paper, DOI 10.20944/preprints202511.1472.v2, retained intact in the supplied framework compilation and as a complete constituent extract.

## Validation and limitations

The final PDF has 36 pages. All 36 pages were rendered and visually inspected in page contact sheets, with detailed inspection of the revised numerical table and map chain. The final LaTeX log contains no unresolved citations/references, duplicate labels, overfull/underfull box messages, or other LaTeX warnings. Numerical checks test named analytic identities and toy models only. No raw image data, measured axial profile, actual readout leakage, or source-derived covariance correction has been newly inferred.

The reference-PDF collection remains at 6 of 25 cited works; nineteen external reference PDFs are still absent. All original supplied PDFs and their filenames are preserved.
