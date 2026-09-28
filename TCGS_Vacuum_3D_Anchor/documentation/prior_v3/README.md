# Vacuum-fluctuation carrier study — research package v3

The current manuscript is `overleaf/main.pdf` (36 pages); its complete source is `overleaf/main.tex`. Revision v3 applies only the four final notation/assumption clarifications described in `documentation/revision_notes.md`. All numbered mathematics and bibliography entries are unchanged from v2.

## Build and run

Compile `overleaf/main.tex` using pdfLaTeX (two passes, or `latexmk -pdf main.tex` from the `overleaf` directory). No .bib file or external graphics are needed. Run `python analysis/reproduce.py` from this research-package root. The script requires Python 3.10+ and only standard-library modules. It writes its outputs alongside itself.

The numerical companion is unchanged from v2. All 475 named parameter cases pass. `analysis/equation_check_map.md` explains exactly which formulas are checked and which are only evaluated, discussed analytically, or left outside the code's scope.

## Reference-PDF limitation

The archive includes six of the 25 cited reference PDFs: the supplied vacuum-imaging paper and five complete constituent-framework extracts. Nineteen external reference PDFs remain missing. The two complete original framework compilations are included under `sources/`. No new external PDF was obtained in this revision. The eight-page annotated reference guide, manifest, access index, downloader and previous download-status record are retained.

## Preservation and provenance

`documentation/v3_cosmetic_update.diff` gives the exact v2-to-v3 source change. `documentation/revision_audit.json` and `documentation/build_validation.json` record the current checks. Historical material for the original and v2 versions remains under `documentation/prior_version/` and `documentation/prior_v2/`. The older `documentation/main_surgical_update.diff` records the original-to-v2 revision and is retained for provenance; it is not the v2-to-v3 diff.

All original reference/source PDF bytes are preserved. `documentation/SHA256SUMS.txt` records current package-file hashes (excluding itself). The CC BY 4.0 statement applies as specified in the manuscript, not automatically to third-party references.
