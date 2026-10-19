import json
from pathlib import Path
from contracts import validate_collection
root = Path(__file__).resolve().parent.parent
registry = json.loads((root / 'shared/jurisdictions.json').read_text())
assert registry['schema_version'] == 1
ids = [j['id'] for j in registry['jurisdictions']]
assert len(ids) == len(set(ids))
for jurisdiction in registry['jurisdictions']:
    validate_collection(json.loads((root / 'public/data/issues' / f"{jurisdiction['id']}.json").read_text()))
print('Jurisdiction registry and issue contracts are valid.')
