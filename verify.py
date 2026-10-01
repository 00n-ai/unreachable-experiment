"""Verify this release without credentials, API calls, or the original workspace."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from scipy.stats import beta

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT/'SHA256SUMS.json').read_text())
for name, expected in manifest.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
counts = Counter()
seen = set()
for path in sorted((ROOT/'data').glob('*-outcomes.jsonl.gz')):
    with gzip.open(path, 'rt') as stream:
        for line in stream:
            row = json.loads(line)
            key = (row['model'], row['instance_id'])
            assert key not in seen, key
            seen.add(key)
            assert row['negated'] is False
            counts[(row['model'], row['depth'], row['breadth'], row['reachable'], row['classification'])] += 1
assert len(seen) == 80000
data = json.loads((ROOT/'data/explainer.json').read_text())
assert len(data['cells']) == 20
tail = .05 / 40
for cell in data['cells']:
    prefix = (cell['model'], cell['depth'], cell['breadth'])
    for reachable, field in ((False, 'counts'), (True, 'reachable_counts')):
        actual = {key[-1]: value for key, value in counts.items() if key[:-1] == (*prefix, reachable)}
        assert actual == cell[field], (prefix, reachable)
        assert sum(actual.values()) == 2000
    k, u, n = cell['correct'], cell['unknown'], cell['n']
    bounds = [float(beta.ppf(tail, k, n-k+1)) if k else 0.,
              float(beta.ppf(1-tail, k+u+1, n-k-u)) if k+u<n else 1.]
    assert all(abs(a-b)<1e-12 for a,b in zip(bounds, cell['joint_interval']))
    decision = 'above_90' if bounds[0]>.9 else 'below_90' if bounds[1]<.9 else 'unresolved'
    assert decision == cell['decision']
print(f'PASS: {len(manifest)} file hashes; 80,000 unique observations; 20 joint intervals; reachable controls.')
