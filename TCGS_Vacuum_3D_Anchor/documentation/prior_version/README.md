# Vacuum-Fluctuation Imaging and Three-Dimensional Carrier Irreducibility

**MODE A — FROM SCRATCH**  
Henry Arellano-Peña · 27 September 2026

## Delivery status

The new analytical manuscript is complete as a **32-page, compiled LaTeX article** with 25 numbered references, four tables, four propositions, four technical appendices, and a CC BY 4.0 license block. The 8-page annotated reference guide documents the role and version of every cited work.

**The external-PDF collection is incomplete: 6 of the 25 cited works are included as actual PDFs. Nineteen external reference PDFs could be read through the browser, or through full HTML in the precursor's case, but their bytes could not be downloaded into the working filesystem.** No reference summaries or HTML error pages are passed off as the missing articles. Versioned PDF targets, a clickable access index, and a downloader are included.

The archive contains **10 actual PDFs**: the new manuscript, the reference guide, the original seven-page experimental paper, two complete original framework compilations, and five complete constituent-framework-paper extracts. The original supplied filenames and bytes are preserved. Each PDF is listed in `documentation/pdf_validation.json`.

## Main files

| Path | Content |
|---|---|
| `overleaf/main.tex` | Complete standalone manuscript, including all 25 bibliography entries. No external figures or BibTeX file are required. |
| `overleaf/main.pdf` | Compiled 32-page manuscript. |
| `documentation/reference_guide.pdf` | Annotated 8-page reference list and explicit availability record. |
| `documentation/reference_guide.tex` | Editable guide source. |
| `references/REFERENCE_ACCESS.html` | Clickable index of included PDFs and missing online PDF targets. |
| `references/reference_manifest.json` | Bibliographic metadata, role, version, PDF target, and original-delivery availability for all 25 works. |
| `references/download_references.py` | Optional downloader and structural/title checker for the missing PDFs. |
| `references/download_report.json` | Offline verification result: six valid existing reference PDFs, nineteen missing. |
| `references/test_downloader_offline.py` | Tests existing PDFs and rejection of HTML, truncation, and a recognizable wrong article; no live-network success is asserted. |
| `analysis/reproduce.py` | Standard-library Python script for nominal scales and 344 analytic-identity checks. |
| `analysis/nominal_scales.json` | Source inputs separated from derived values and illustrative calculations. |
| `analysis/confinement_family.csv` | Calculated confinement-sensitivity table, not experimental observations. |
| `analysis/analytic_checks.json` | Results and tolerances of the 344 numerical checks. |
| `sources/` | Both original framework compilations, unchanged. |
| `references/framework/` | Five unchanged constituent-paper extracts. |
| `documentation/framework_extract_provenance.json` | Exact extraction boundaries within the supplied compilations. |
| `documentation/build_validation.json` | LaTeX cross-reference, citation, page-count, and warning checks. |
| `documentation/SHA256SUMS.txt` | Integrity hashes for the delivered files other than the checksum file itself. |

## Overleaf and local compilation

Create a blank Overleaf project and upload `overleaf/main.tex`. Select **pdfLaTeX** and make `main.tex` the main document. The source includes the entire manuscript and the numbered bibliography; no `.bib`, image, external URL retrieval, or shell escape is needed for compilation. Compile twice after making changes that affect cross-references.

On a computer with a normal TeX Live or MiKTeX installation:

```sh
cd overleaf
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The delivered PDF was compiled successfully with no undefined citations, undefined cross-references, duplicate labels, or overfull/underfull box warnings. The paper uses ordinary 11-point A4 article formatting and 26 mm margins; the page count is not produced by forced section breaks or oversized spacing.

## Retrieve the missing reference PDFs

This step requires a separate internet-connected Python environment. The downloader's parsing and rejection paths were tested offline; live transfer could not be tested successfully in the creation environment. The script does not bypass access controls.

From the extracted package root:

```sh
python -m pip install pypdf
python references/download_references.py --create-zip
```

On Windows, `py` may be used instead of `python`:

```powershell
py -m pip install pypdf
py references/download_references.py --create-zip
```

A successful run creates `TCGS_Vacuum_3D_All_25_Reference_PDFs.zip` beside the package directory **only after all 25 referenced PDFs validate**. Failed targets are recorded; an incomplete run exits with status 2 and does not create a misleading complete-reference ZIP. Downloaded files retain their own licenses. The original-delivery guide is a dated availability record; `download_report.json` records the updated local status.

To check existing files without network access:

```sh
python references/download_references.py --verify-only
python references/test_downloader_offline.py
```

## Reproduce the numerical analysis

```sh
python analysis/reproduce.py
```

Python 3.10 or later is required; this calculation uses only the standard library. The nominal inputs are the reported 1 kHz transverse confinement, 33 micrometre box side, and rounded interaction scales, together with a deliberately rounded `39u` isotope mass. The script returns an oscillator length of about 0.509 micrometres, RMS width of about 0.360 micrometres, and an axial gap equivalent to 48.0 nK.

Those are **model-derived nominal values**, not new measurements of the condensate thickness. The script checks algebraic and numerical identities; it does not reproduce the raw-image processing or refit the reported spin temperature.

## Source discipline and scope

`TCGS-SEQUENTION_core19(3).pdf` governs the source–shadow terminology. The supplemental `TCGS-SEQUENTION_core20(6).pdf` supplies the specified September Planck dimensionality paper. Relevant constituent papers are cited independently in the manuscript; packaging provenance is kept outside the publication text.

The empirical anchor is finite-width three-dimensional atomic realization of effective two-dimensional spin-field behaviour. The paper does not identify the atomic transverse direction with the fourth Counterspace direction. Nor does it claim that a vacuum spectrum is, by itself, a universal dimensionality theorem or a refutation of technical holographic duality. The finite-energy obstruction is stated within the massive-atom model, and all additional framework-level inference is distinguished from that result.

## Submission package versus research archive

Use the small Overleaf package, or `overleaf/main.tex`, for manuscript work. The full research archive also contains the supplied internal framework compilations and packaging records; it is not intended to be uploaded wholesale as a journal submission. The publication text cites the relevant constituent works independently.

## Rights

The newly authored manuscript and original analytical material are licensed under CC BY 4.0 as stated in the article. Original supplied PDFs and external papers retain their individual licenses. Nothing in this package re-licenses third-party articles or authorizes unrelated republication.
