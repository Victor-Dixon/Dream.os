#!/usr/bin/env python3
"""
Remove Default/Placeholder Contracts from Contract System

This script removes all contracts with "Default Contract" in the title
from the contract storage system.
"""
import json
from pathlib import Path

def remove_default_contracts():
    """Remove all default/placeholder contracts from agent contract files."""
    contracts_dir = Path('agent_workspaces/contracts/agent_contracts')

    if not contracts_dir.exists():
        print("❌ Contracts directory not found")
        return

    total_removed = 0

    for contract_file in contracts_dir.glob('*_contracts.json'):
        print(f"🔍 Processing {contract_file.name}...")

        with open(contract_file, 'r') as f:
            data = json.load(f)

        original_count = len(data)
        contracts_to_remove = []

        # Identify default contracts to remove
        for contract_id, contract in data.items():
            if 'Default Contract' in contract.get('title', ''):
                contracts_to_remove.append(contract_id)
                print(f"   🗑️ Marked for removal: {contract.get('title')} ({contract_id})")

        # Remove the default contracts
        for contract_id in contracts_to_remove:
            del data[contract_id]
            total_removed += 1

        removed_count = original_count - len(data)
        if removed_count > 0:
            print(f"   ✅ Removed {removed_count} default contracts from {contract_file.name}")

            # Save the cleaned file
            with open(contract_file, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            print(f"   ℹ️ No default contracts found in {contract_file.name}")

    print(f"\n🎉 Cleanup complete! Removed {total_removed} default contracts total.")

    # Also clean the main contracts.json file if it exists
    main_contracts_file = Path('agent_workspaces/contracts/contracts.json')
    if main_contracts_file.exists():
        print("🔍 Cleaning main contracts.json...")
        with open(main_contracts_file, 'r') as f:
            main_data = json.load(f)

        main_original_count = len(main_data)
        main_to_remove = []

        for contract_id, contract in main_data.items():
            if 'Default Contract' in contract.get('title', ''):
                main_to_remove.append(contract_id)

        for contract_id in main_to_remove:
            del main_data[contract_id]

        main_removed = main_original_count - len(main_data)
        if main_removed > 0:
            print(f"   ✅ Removed {main_removed} default contracts from contracts.json")
            with open(main_contracts_file, 'w') as f:
                json.dump(main_data, f, indent=2)
            total_removed += main_removed
        else:
            print("   ℹ️ No default contracts found in contracts.json")

    print(f"\n🏁 Final total: Removed {total_removed} placeholder contracts from the system.")

if __name__ == '__main__':
    remove_default_contracts()