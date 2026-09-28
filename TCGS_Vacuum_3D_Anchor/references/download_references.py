#!/usr/bin/env python3
"""Retrieve missing reference PDFs from the versioned targets in the manifest.

Python 3.10+ and pypdf are required. This script has been tested offline; live
network transfer was unavailable in the creation environment. It never treats an
HTML response as a PDF, never overwrites a valid existing paper, and does not
bypass authentication or publisher access controls.

Usage:
  python -m pip install pypdf
  python references/download_references.py --create-zip
  python references/download_references.py --verify-only
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zipfile import ZIP_DEFLATED, ZipFile

try:
    from pypdf import PdfReader
except ImportError as exc:
    raise SystemExit('Install the PDF parser first: python -m pip install pypdf') from exc

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name('reference_manifest.json')
STOP = {'the', 'and', 'of', 'in', 'a', 'an', 'to', 'as', 'at', 'for', 'is', 'with',
        'by', 'from', 'on', 'its', 'via', 'within', 'without'}
MAX_BYTES = 100 * 1024 * 1024


def words(text: str) -> set[str]:
    # Normalize common PDF ligatures and accents before a conservative identity check.
    text = unicodedata.normalize('NFKD', text.replace('ﬁ', 'fi').replace('ﬂ', 'fl'))
    text = ''.join(c for c in text if not unicodedata.combining(c)).lower()
    return {w for w in re.findall(r'[a-z0-9]+', text) if len(w) > 2 and w not in STOP}


def validate_pdf(data: bytes, reference: dict) -> dict:
    if len(data) < 500 or not data.lstrip().startswith(b'%PDF-'):
        raise ValueError('Response is not a PDF; possible HTML error or access page.')
    if b'%%EOF' not in data[-8192:]:
        raise ValueError('PDF has no final EOF marker; possible truncated download.')
    reader = PdfReader(io.BytesIO(data), strict=False)
    if reader.is_encrypted:
        raise ValueError('Encrypted PDF was not accepted as a usable reference.')
    n = len(reader.pages)
    if n < 1:
        raise ValueError('PDF has no readable pages.')
    # Touch every page dictionary and content stream, not only the trailer.
    for page in reader.pages:
        _ = page.mediabox
        stream = page.get_contents()
        if stream is not None:
            _ = stream.get_data()
    excerpt = ' '.join((reader.pages[i].extract_text() or '') for i in range(min(3, n)))
    expected = words(reference['title'])
    actual = words(excerpt)
    overlap = len(expected & actual) / max(1, len(expected))
    if overlap < 0.45:
        raise ValueError(f'PDF title check failed (token overlap {overlap:.2f}); manual review required.')
    warnings = []
    if reference.get('expected_pages') and n != reference['expected_pages']:
        warnings.append(f"Page count {n} differs from expected {reference['expected_pages']}; review the version.")
    return {'pages': n, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'title_token_overlap': overlap, 'warnings': warnings}


def retrieve(url: str, timeout: float) -> bytes:
    if not url.startswith('https://arxiv.org/pdf/'):
        raise ValueError('Only the manifest arXiv HTTPS PDF targets are allowed.')
    request = Request(url, headers={'User-Agent': 'TCGS-Reference-Archiver/1.0 (research reference retrieval)',
                                    'Accept': 'application/pdf'})
    with urlopen(request, timeout=timeout) as response:
        declared = response.headers.get('Content-Length')
        if declared and int(declared) > MAX_BYTES:
            raise ValueError('Download exceeds the 100 MB per-file safety limit.')
        chunks, count = [], 0
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            count += len(block)
            if count > MAX_BYTES:
                raise ValueError('Download exceeds the 100 MB per-file safety limit.')
            chunks.append(block)
    return b''.join(chunks)


def run(args: argparse.Namespace) -> int:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    results = []
    for reference in manifest['references']:
        target = (ROOT / reference['local_path']).resolve()
        if ROOT.resolve() not in target.parents:
            raise ValueError('Unsafe local path in reference manifest.')
        result = {'number': reference['number'], 'key': reference['key'],
                  'title': reference['title'], 'path': reference['local_path'],
                  'pdf_url': reference.get('pdf_url')}
        try:
            if target.is_file():
                result.update(validate_pdf(target.read_bytes(), reference))
                result['status'] = 'validated_existing'
            elif args.verify_only:
                result['status'] = 'missing'
            elif not reference.get('pdf_url'):
                result['status'] = 'missing_no_public_pdf_target'
            else:
                last_error = None
                for attempt in range(args.retries + 1):
                    try:
                        data = retrieve(reference['pdf_url'], args.timeout)
                        validation = validate_pdf(data, reference)
                        target.parent.mkdir(parents=True, exist_ok=True)
                        temporary = target.with_suffix('.pdf.part')
                        temporary.write_bytes(data)
                        temporary.replace(target)
                        result.update(validation)
                        result['status'] = 'downloaded_and_validated'
                        last_error = None
                        break
                    except (HTTPError, URLError, OSError, ValueError) as exc:
                        last_error = f'{type(exc).__name__}: {exc}'
                        if attempt < args.retries:
                            time.sleep(min(30, 3 * 2**attempt))
                if last_error:
                    result.update(status='failed', error=last_error)
                time.sleep(args.pause)
        except Exception as exc:
            # A corrupt existing reference is preserved for inspection, not overwritten.
            result.update(status='failed', error=f'{type(exc).__name__}: {exc}')
        print(f"[{reference['number']:02d}] {result['status']}: {reference['title']}")
        results.append(result)
    accepted = {'validated_existing', 'downloaded_and_validated'}
    successful = sum(r['status'] in accepted for r in results)
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'reference_count': len(results), 'validated_count': successful,
              'complete': successful == len(results),
              'note': 'The original delivery manifest records original coverage; this report records current local status.',
              'results': results}
    report_path = Path(__file__).with_name('download_report.json')
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.create_zip:
        if not report['complete']:
            print('No complete-reference ZIP created: one or more reference PDFs are missing or invalid.', file=sys.stderr)
        else:
            output = ROOT.parent / 'TCGS_Vacuum_3D_All_25_Reference_PDFs.zip'
            with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
                for ref in manifest['references']:
                    archive.write(ROOT / ref['local_path'], ref['local_path'])
                archive.write(report_path, 'references/download_report.json')
                archive.write(MANIFEST, 'references/reference_manifest_original_delivery.json')
                archive.writestr('README.txt',
                    'All 25 reference PDF files passed structural and heuristic title validation.\n'
                    'See download_report.json for dates, page counts, hashes, and version warnings.\n'
                    'Files retain their original licenses. No license of the new manuscript overrides them.\n'
                    'The original-delivery manifest is a historical availability record, not current coverage.\n')
            print(f'Created: {output}')
    print(f'Validated {successful}/{len(results)} reference PDFs. Report: {report_path}')
    return 0 if report['complete'] else 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--verify-only', action='store_true', help='Do not access the network.')
    parser.add_argument('--create-zip', action='store_true', help='Create a reference ZIP only if all 25 PDFs validate.')
    parser.add_argument('--timeout', type=float, default=45., help='Per-request timeout in seconds (default: 45).')
    parser.add_argument('--retries', type=int, default=2, help='Retries after an initial failed download (default: 2).')
    parser.add_argument('--pause', type=float, default=3., help='Pause between requested PDFs (default: 3 seconds).')
    options = parser.parse_args()
    if options.timeout <= 0 or options.retries < 0 or options.pause < 0:
        parser.error('timeout must be positive; retries and pause must be nonnegative.')
    raise SystemExit(run(options))
