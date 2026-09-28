# Publication revision v5

Basis: exact v4 manuscript and its 515-case numerical companion.

## Requested changes

1. All current delivery archives carry the executable at `analysis/reproduce.py`. The numerical supplement is no longer a flattened root-level script. The independently downloadable file is named `reproduce.py`, not `reproduce_v4.py`. All three outputs are generated beside the canonical script.
2. The introduction roadmap now includes the claim-status ledger (Section 16), discussion (Section 18), and conclusion (Section 19).
3. The five manual tags were removed. Equations now run continuously from (1) to (83); all original LaTeX labels and mathematical contents are preserved. The v4 tags (4a), (21a), (21b), (59a), and (74a) become (5), (23), (24), (63), and (79). See the complete equation-number concordance.
4. Section 7.1 now reads “The error from the isotope-mass approximation is far smaller than the uncertainty…”.
5. The affiliation reads “Nuevo Estándar Biotropical NEBIOT S.A.S.”.

## Numerical synchronization

The script's calculations, input constants, test grids, classifications, tolerances and numerical values are unchanged. Only its local-equation docstring and 40 dispersion/limit record names were synchronized: former (48)/(49) are now (51)/(52). The equation-to-check map and check-group metadata use the same current numbers. All 515 cases pass: 509 analytic/model checks and six auxiliary checks. Nominal JSON and confinement CSV remain byte-identical to v4.

## Build and preservation

The manuscript compiles to 37 pages under the unchanged article format; the small editorial addition changes pagination. No manual page expansion, font reduction, margin change, or altered mathematical content was introduced. All 113 label keys, all 83 numbered mathematical displays (apart from tag commands), all unnumbered displays, the section order, the external links, and the 25-entry bibliography are preserved. PDF build and rendering checks are recorded separately. Prior active v4 files are retained in `documentation/prior_v4/` in the full research archive. Historical diffs retain their original equation numbers and are not current instructions.

No external repository or preprint service has been modified. Reference coverage remains six included cited PDFs out of 25; nineteen external reference PDFs are still absent.
