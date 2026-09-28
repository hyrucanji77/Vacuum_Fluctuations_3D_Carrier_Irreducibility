# Revision v3 — final notation and assumption clarifications

Mode B: surgical update of the existing v2 LaTeX source.

Exactly four source hunks changed. The title, abstract, keywords, section order, all 113 v2 label values, all 83 numbered equation/align blocks (including five custom-tag additions), and the complete 25-entry bibliography are preserved. The main equation numbers (1)--(78) and custom equation tags are unchanged. One unnumbered operator display changes only its identity symbol.

## Changes

1. Section 5.1: the transverse identity is now `I_{L^2(\R_z)}`, avoiding a spin-operator reading of `I_z`.
2. Table 2: the status of the derived nominal value 12.96 is now “Derived from reported ratio”; the value and source citation are unchanged.
3. Section 5.1: its unequal-profile paragraph now points to the mean-field equality in Section 7.2.
4. Section 17.6: the sensitivity analysis explicitly assumes a local Banach-manifold structure on admissible source configurations near Xi_0 and Frechet differentiability of the calibrated statistical prediction map there. This is an assumption of that analysis, not a new source-ontology theorem.

## Numerical supplement

`analysis/reproduce.py` is byte-identical to the v2 script and was run again. All 475 named parameter cases pass; its three regenerated outputs are byte-identical to the v2 outputs. The accompanying equation-to-check map separates direct assertions, evaluated outputs, toy-model checks, and formulas not numerically checked. The exported standalone script was also run successfully, without network access or external dependencies.

## Build and preservation

The manuscript compiles to 36 pages with pdfLaTeX/latexmk. The final log has no LaTeX warnings, overfull/underfull boxes, or undefined references. All pages were rendered with PyMuPDF, and the changed operator, table, cross-reference, and assumption text were inspected in the page images. Version v2 records are preserved under `documentation/prior_v2/`; the exact current diff is `documentation/v3_cosmetic_update.diff`.

## Reference archive

The reference collection has not changed. Six of the 25 cited works have PDFs in the archive; nineteen external reference PDFs remain absent. The complete supplied framework compilations are preserved separately. No new external source was added in v3.
