# Revision v4 — code/manuscript traceability correction

MODE B: surgical update of the complete v3 source and numerical supplement.

## Implemented corrections

1. Added `dispersion_checks()`: 16 named tests of the exact Eq. (48) expansion against the factorized dispersion and 24 Eq. (49) squared-frequency error/convergence tests. The latter comprise two checks at each of twelve finite ray/scale pairs. This closes the coverage gap in Appendix C.
2. Kept the four elementary cancellation calculations, but renamed them `arithmetic sanity: common-factor cancellation` and classified them `arithmetic_sanity`. They are not presented as independent evidence for Proposition 14.1. The original `scale_row`-based family remains intact.
3. Renamed the two rounded-digit assertions `printed-value consistency` and classified them `printed_value_consistency`.
4. Added a cited paragraph in Section 8.1 giving the source scattering lengths, bias field, and resulting common-profile coupling ratios. The script comment points to p. 5 of the supplied Zhang v1 PDF.
5. Added one paragraph in Appendix C identifying the new exact-dispersion/Josephson checks and separate reporting of the auxiliary cases.

## Preservation

No existing LaTeX line was removed. The manuscript has exactly two additive source hunks. The title, abstract, keywords, section order, all 113 labels and their reference values, all 77 equation and six align environments, all other mathematical displays, and the complete 25-entry bibliography are unchanged. The compiled manuscript remains 36 pages. Existing numbered equation values (1)--(78) and the five custom tags remain unchanged.

All 475 old assertion actual/expected values, errors, tolerances, and pass statuses remain unchanged. Six names are corrected and a category field is added to each report record. The 40 new cases bring the report to 515 cases: 509 analytic/model checks plus six auxiliary checks. The nominal JSON and confinement CSV are byte-identical to v3. `analytic_checks.json` is intentionally updated; its total `checks` field includes all records, while new count fields distinguish the auxiliary categories.

## Validation

The script runs with only the standard library. Baseline and patched versions were both executed; the detailed audit records the comparisons. No new tolerance was relaxed. Two separate mutation controls confirm that the new block detects omission of the quartic term and a wrong sound-speed coefficient; these controls are not counted among the 515 manuscript-companion cases.

A clean pdfLaTeX/latexmk build has no warnings, overfull/underfull boxes, or undefined references. Page bounds were checked, and the four pixel-changed pages (15, 34, 35, 36) were rendered and visually inspected. A fresh extraction of each deliverable archive is run/built separately in the packaging validation.

## Version history and reference coverage

The v3 script, manuscript and active reports are retained in `documentation/prior_v3/`; the existing older provenance directories and diffs are retained. The current diffs are `documentation/reproduce_v3_to_v4.diff` and `documentation/main_v3_to_v4.diff`.

No new external reference PDF was requested or collected in this code-focused revision. The full research archive still includes six of the 25 cited reference PDFs and both complete supplied framework compilations; nineteen external reference PDFs remain absent. The manuscript license is not automatically a license for third-party PDFs.
