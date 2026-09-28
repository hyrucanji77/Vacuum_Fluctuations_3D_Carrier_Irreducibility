# Vacuum-fluctuation carrier study — research package v4

The current manuscript is `overleaf/main.pdf` (36 pages), with complete source in `overleaf/main.tex`. Revision v4 closes the Eq. (48)/(49) numerical-check coverage gap, separates four arithmetic and two printed-value checks, and adds the source interaction-ratio trace in Section 8.1. No numbered equation, bibliography entry, or reported numerical result changed.

## Build and run

Compile `overleaf/main.tex` with pdfLaTeX (two passes, or `latexmk -pdf main.tex` from `overleaf/`). All 25 numbered references are embedded; no .bib, external graphics, network or shell escape is required. From the research-package root run `python analysis/reproduce.py`. Python 3.10+ and the standard library suffice. The three outputs are written beside the script.

All 515 named cases pass: 509 analytic/model checks and six separately classified auxiliary checks. Read `analysis/equation_check_map.md` for precise coverage and limits. `analysis/nominal_scales.json` and `analysis/confinement_family.csv` are unchanged from v3. `analysis/analytic_checks.json` contains new dispersion/limit records and category counts.

## Reference-PDF limitation

Six of the 25 cited works have PDFs in the archive: the supplied vacuum-imaging paper and five complete constituent-framework extracts. Nineteen external reference PDFs remain missing. Both complete original compilations are under `sources/`. The existing annotated guide, reference manifest, access index and downloader are retained. No reference PDF is represented by an HTML error page or fabricated substitute.

## Preservation and provenance

Current changes are recorded in `documentation/main_v3_to_v4.diff` and `documentation/reproduce_v3_to_v4.diff`. `documentation/revision_audit.json`, `documentation/build_validation.json`, and `documentation/archive_validation.json` record current validation. Prior v3 active files are retained in `documentation/prior_v3/`, alongside the earlier history. The historical diffs elsewhere under `documentation/` are retained as history, not represented as the current diff.

All original reference/source PDF bytes are preserved. `documentation/SHA256SUMS.txt` records package-file hashes excluding itself. The manuscript's CC BY 4.0 statement does not automatically license third-party references.
