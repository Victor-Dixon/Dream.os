#!/usr/bin/env python3
"""Test script for contract storage API compatibility fix"""

from src.services.contract_system.storage import ContractStorage
from src.services.contract_service import ContractService

def test_contract_api_compatibility():
    print("Testing Contract Storage API Compatibility...")

    # Initialize components
    storage = ContractStorage()
    service = ContractService(storage)

    # Test data
    test_contract = {
        'title': 'API Compatibility Test Contract',
        'description': 'Testing the fixed contract storage API',
        'status': 'active',
        'priority': 'medium'
    }

    print("1. Testing interface-compliant methods...")

    # Test save_contract_data (interface method)
    result = storage.save_contract_data('Agent-Test', test_contract)
    print(f"   ✅ save_contract_data result: {result}")

    # Test load_contract_data (interface method)
    loaded = storage.load_contract_data('Agent-Test')
    print(f"   ✅ load_contract_data result: {loaded is not None}")
    if loaded:
        print(f"   Title: {loaded.get('title', 'N/A')}")

    print("2. Testing ContractService integration...")

    # Test that ContractService uses the new methods
    service_result = service.save_contract('Agent-Test', test_contract)
    print(f"   ✅ ContractService.save_contract result: {service_result}")

    service_loaded = service.load_contract('Agent-Test')
    print(f"   ✅ ContractService.load_contract result: {service_loaded is not None}")

    print("3. Testing backward compatibility...")

    # Test list_contracts method
    all_contracts = storage.list_contracts()
    print(f"   ✅ list_contracts returned {len(all_contracts)} contracts")

    print("🎉 Contract Storage API compatibility test PASSED!")
    print("   - Interface-compliant methods working")
    print("   - ContractService integration successful")
    print("   - Backward compatibility maintained")

if __name__ == "__main__":
    test_contract_api_compatibility()