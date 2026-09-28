#!/usr/bin/env python3
"""Offline validation tests only; no assertion of successful live downloads."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('download_references', HERE/'download_references.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
manifest = json.loads((HERE/'reference_manifest.json').read_text(encoding='utf-8'))
checks = []
for r in manifest['references']:
    if r['included']:
        result = module.validate_pdf((module.ROOT/r['local_path']).read_bytes(), r)
        checks.append({'check': 'validate supplied PDF '+r['key'], 'passed': True,
                       'pages': result['pages']})
reference = manifest['references'][0]
for name, data in [('HTML response', b'<html>Access denied</html>'*100),
                   ('truncated PDF', (module.ROOT/reference['local_path']).read_bytes()[:10000])]:
    try:
        module.validate_pdf(data, reference)
    except Exception:
        checks.append({'check': 'reject '+name, 'passed': True})
    else:
        raise AssertionError('Invalid response accepted: '+name)
wrong_file = module.ROOT/manifest['references'][1]['local_path']
try:
    module.validate_pdf(wrong_file.read_bytes(), reference)
except ValueError:
    checks.append({'check': 'reject recognizable wrong article', 'passed': True})
else:
    raise AssertionError('Wrong article passed the identity check.')
report={'all_passed':True,'network_transfer_tested':False,'checks':checks}
(HERE/'downloader_offline_tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{len(checks)} offline PDF validation tests passed. Live downloading was not tested.')
