import json
from pathlib import Path

brain_file = Path('swarm_brain/knowledge_base.json')
if brain_file.exists():
    with open(brain_file, 'r') as f:
        data = json.load(f)

    new_id = f'kb-{len(data["entries"]) + 1}'
    new_learning = {
        'id': new_id,
        'title': 'Workspace Integrity Enforcement with Audit Evidence Validation',
        'content': 'Implemented Stage-4 workspace integrity enforcement requiring audit evidence validation before closure acceptance. Sensor-judge-dispatcher pattern ensures workspace safety.',
        'author': 'Agent-3',
        'category': 'learning',
        'tags': ['governance', 'safety', 'workspace-integrity', 'audit-evidence', 'closure-validation'],
        'timestamp': '2025-12-28T05:15:00.000000',
        'metadata': {
            'session': 'workspace_integrity_enforcement_2025-12-28'
        }
    }

    data['entries'][new_id] = new_learning
    data['last_updated'] = '2025-12-28T05:15:00.000000'

    with open(brain_file, 'w') as f:
        json.dump(data, f, indent=2)

    print('Swarm Brain updated')
else:
    print('File not found')
