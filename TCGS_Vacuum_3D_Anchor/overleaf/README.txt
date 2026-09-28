Vacuum-Fluctuation Imaging and Three-Dimensional Carrier Irreducibility
Publication revision v5 — 37 pages; 83 continuously numbered equations.

OVERLEAF
Upload the separate Overleaf ZIP as a project and compile main.tex with pdfLaTeX.
In the full research package, main.tex is under overleaf/.
All 25 numbered references are embedded. No separate .bib, external graphics,
network access, or shell escape is required.

NUMERICAL COMPANION
From the extracted project root, run:
    python analysis/reproduce.py
Keep the analysis/ directory. The canonical script name is reproduce.py.
Python 3.10+; standard library only. Three outputs are written next to the script.
All 515 cases pass: 509 analytic/model checks and six auxiliary checks.
See analysis/equation_check_map.md for exact coverage and limits.

EQUATION NUMBERS
Equations now run from (1) to (83); every LaTeX label and formula is preserved.
See documentation/equation_numbering_v4_to_v5.md for the full concordance.
Former dispersion equations (48)/(49) are now (51)/(52), also in the script.
Only textual equation references changed in the code, not numerical computations.

CHANGES AND SCOPE
See documentation/revision_notes.md and the v4_to_v5 diffs.
The affiliation accent, isotope-mass wording, and complete roadmap are corrected.
No external posting was performed. External reference PDFs are not part of the
small Overleaf ZIP; the full research package still lacks 19 cited PDFs.
