#!/usr/bin/env python3
import json
from pathlib import Path

contracts_dir = Path('agent_workspaces/contracts/agent_contracts')
if contracts_dir.exists():
    for contract_file in contracts_dir.glob('*_contracts.json'):
        with open(contract_file, 'r') as f:
            data = json.load(f)
            for contract_id, contract in data.items():
                if 'Default Contract' in contract.get('title', ''):
                    print(f'Found default contract in {contract_file.name}:')
                    print(f'  ID: {contract_id}')
                    print(f'  Title: {contract.get("title")}')
                    print(f'  Created: {contract.get("created_at")}')
                    print()
else:
    print("Contracts directory not found")