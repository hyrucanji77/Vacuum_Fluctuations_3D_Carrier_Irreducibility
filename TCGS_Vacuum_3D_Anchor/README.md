# Vacuum-fluctuation carrier study — publication package v5

Current paper: `overleaf/main.pdf` (37 pages). Complete LaTeX: `overleaf/main.tex`. Canonical numerical companion: `analysis/reproduce.py`.

## Compile and run

From this project root, run:

```bash
python analysis/reproduce.py
```

Python 3.10+; standard library only. The generated files are `analysis/nominal_scales.json`, `analysis/confinement_family.csv`, and `analysis/analytic_checks.json`. All 515 cases pass: 509 analytic/model cases and six separately classified auxiliary cases. Run the script from the project root; do not flatten the archive or rename it to an iteration-specific filename.

Compile by running `latexmk -pdf main.tex` from `overleaf/`, or compile `main.tex` with pdfLaTeX until references settle. All 25 numbered references are embedded; no `.bib`, external graphic, network access or shell escape is required. The separate Overleaf ZIP has `main.tex` at its root and the same `analysis/reproduce.py` path.

## Publication edits and equation numbers

See `documentation/revision_notes.md` and `documentation/main_v4_to_v5.diff`. The roadmap, isotope-mass wording and affiliation accent are corrected. All mathematical expressions are retained. Equation numbers are now continuous (1)--(83); every label key is preserved. `documentation/equation_numbering_v4_to_v5.md` maps old numbers to new ones. `analysis/equation_check_map.md` and the script's textual references use current numbers.

## Source PDFs and limitations

The supplied vacuum-imaging PDF and five complete constituent-framework PDFs are in `references/`; both original framework compilations are in `sources/`. These original bytes and filenames are unchanged. Nineteen of the 25 cited works do not have a PDF in this archive. The existing reference guide, manifest, access index and downloader remain available; no missing PDF is represented by an error page or fabricated substitute. The guide is retained as a bibliographic source record, not as a newly fetched PDF collection.

## Provenance

The full research package keeps earlier source versions in `documentation/prior_v4/` and the previous history directories. Old diffs, reports and archived sources are historical records. Current validation is in `documentation/revision_audit.json`, `build_validation.json`, `archive_validation.json`, and `pdf_validation.json`. SHA-256 hashes for active package files are recorded in `documentation/SHA256SUMS.txt` (excluding itself). No external posting was performed.

The manuscript's CC BY 4.0 statement applies to original analytical material; it does not automatically license third-party publications.
