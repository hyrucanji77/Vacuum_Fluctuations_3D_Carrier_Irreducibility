Vacuum-Fluctuation Imaging and Three-Dimensional Carrier Irreducibility
Revision v3: four final notation/assumption clarifications; complete 36-page manuscript.

OVERLEAF
Upload this ZIP as a new project and compile main.tex with pdfLaTeX.
All 25 numbered references are embedded in main.tex; no .bib, external figures,
network access, or shell escape is required.

NUMERICAL COMPANION
Run: python analysis/reproduce.py
Requires Python 3.10+ and the standard library only. All 475 named cases pass.
Outputs are written in analysis/: analytic_checks.json, nominal_scales.json,
confinement_family.csv. See analysis/equation_check_map.md for exact coverage.
The script and numerical outputs are unchanged from v2.

CHANGES
See documentation/revision_notes.md and documentation/v3_cosmetic_update.diff.
All section order, label values, numbered equation bodies and bibliography are preserved.
