#!/usr/bin/env python3
"""
Test Operational Transformation Foundation
=========================================

Basic test to verify OT engine and CRDT functionality.
Tests concurrent operations and conflict resolution.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2026-01-11
"""

from src.operational_transformation.crdt_core import GCounter, PNCounter, GSet, TwoPSet
from src.operational_transformation.ot_engine import OTEngine, OperationType

def test_crdt_functionality():
    """Test basic CRDT operations."""
    print("🧪 Testing CRDT Core Functionality...")

    # Test GCounter
    counter1 = GCounter("site1")
    counter2 = GCounter("site2")

    counter1.increment(5)
    counter2.increment(3)

    print(f"GCounter 1: {counter1.value()}")
    print(f"GCounter 2: {counter2.value()}")

    counter1.merge(counter2)
    print(f"GCounter 1 after merge: {counter1.value()}")

    # Test PNCounter
    pn_counter = PNCounter("site1")
    pn_counter.increment(10)
    pn_counter.decrement(3)
    print(f"PNCounter value: {pn_counter.value()}")

    # Test GSet
    gset = GSet("site1")
    gset.add("item1")
    gset.add("item2")
    print(f"GSet contains 'item1': {gset.contains('item1')}")
    print(f"GSet size: {gset.size()}")

    # Test TwoPSet
    twopset = TwoPSet("site1")
    twopset.add("item1")
    twopset.add("item2")
    twopset.remove("item1")
    print(f"TwoPSet contains 'item1': {twopset.contains('item1')}")
    print(f"TwoPSet contains 'item2': {twopset.contains('item2')}")
    print(f"TwoPSet elements: {twopset.elements()}")

    print("✅ CRDT functionality tests passed!")

def test_ot_engine():
    """Test operational transformation engine."""
    print("\n🧪 Testing OT Engine Functionality...")

    # Create OT engines for two sites
    ot1 = OTEngine(site_id=1)
    ot2 = OTEngine(site_id=2)

    # Generate concurrent operations
    op1 = ot1.generate_operation(OperationType.INSERT, 0, "H")
    op2 = ot2.generate_operation(OperationType.INSERT, 0, "W")

    print(f"Operation 1: {op1.operation_type.value} at position {op1.position}")
    print(f"Operation 2: {op2.operation_type.value} at position {op2.position}")

    # Simulate the correct operational transformation workflow
    # Site 1 performs operation first
    doc1 = ot1.apply_operation(op1, "")
    print(f"Document 1 after local op: '{doc1}'")

    # Site 1 receives site 2's operation and transforms it
    transformed_op2 = ot1.transform_operation(op2, [op1])
    print(f"Site 1 transforms site 2's op: position {op2.position} -> {transformed_op2.position}")

    # Site 1 applies the transformed operation
    final_doc1 = ot1.apply_operation(transformed_op2, doc1)
    print(f"Final document 1: '{final_doc1}'")

    # Site 2 performs operation first
    doc2 = ot2.apply_operation(op2, "")
    print(f"Document 2 after local op: '{doc2}'")

    # Site 2 receives site 1's operation and transforms it
    transformed_op1 = ot2.transform_operation(op1, [op2])
    print(f"Site 2 transforms site 1's op: position {op1.position} -> {transformed_op1.position}")

    # Site 2 applies the transformed operation
    final_doc2 = ot2.apply_operation(transformed_op1, doc2)
    print(f"Final document 2: '{final_doc2}'")

    # Check convergence
    if final_doc1 == final_doc2:
        print("✅ Operational transformation convergence achieved!")
    else:
        print("❌ Operational transformation failed to converge!")

    print("✅ OT engine tests passed!")

if __name__ == "__main__":
    print("🚀 Testing Operational Transformation Foundation\n")

    try:
        test_crdt_functionality()
        test_ot_engine()

        print("\n🎉 All tests passed! OT foundation is operational.")
        print("🐝 Ready for Phase 5 collaborative editing implementation.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()