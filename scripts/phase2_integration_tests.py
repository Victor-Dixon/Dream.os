#!/usr/bin/env python3
"""
Phase 2: Integration Tests
==========================

Tests basic functionality of extracted components to ensure they work correctly
in their new locations after import updates.

Run this script from the repository root.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any

# Add systems directory to Python path for testing extracted components
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "systems"))
print(f"DEBUG: Added {project_root / 'systems'} to sys.path")
print(f"DEBUG: sys.path[0] = {sys.path[0]}")
print(f"DEBUG: systems directory exists: {(project_root / 'systems').exists()}")

def test_system_imports():
    """Test that all extracted systems can be imported successfully."""
    print("🔍 Testing System Imports...")

    test_results = {
        "gamification": False,
        "memory": False,
        "templates": False,
        "gui": False,
        "scrapers": False,
        "analytics": False,
        "lead_scoring": False,
        "lead_harvesting": False,
        "code_analysis": False
    }

    # Test gamification system
    try:
        from gamification.mmorpg.mmorpg_system import MMORPGSystem
        test_results["gamification"] = True
        print("  ✅ Gamification system imported successfully")
    except Exception as e:
        print(f"  ❌ Gamification system import failed: {e}")

    # Test memory system
    try:
        from memory.memory.manager import MemoryManager
        test_results["memory"] = True
        print("  ✅ Memory system imported successfully")
    except Exception as e:
        print(f"  ❌ Memory system import failed: {e}")

    # Test template system
    try:
        from templates.templates.engine.template_engine import PromptTemplateEngine
        test_results["templates"] = True
        print("  ✅ Template system imported successfully")
    except Exception as e:
        print(f"  ❌ Template system import failed: {e}")

    # Test GUI system (basic import only, no Qt initialization)
    try:
        from gui.gui.components.shared_components import SharedComponents
        test_results["gui"] = True
        print("  ✅ GUI system imported successfully")
    except Exception as e:
        print(f"  ❌ GUI system import failed: {e}")

    # Test scrapers system
    try:
        from scrapers.chatgpt_scraper import ChatGPTScraper
        test_results["scrapers"] = True
        print("  ✅ Scrapers system imported successfully")
    except Exception as e:
        print(f"  ❌ Scrapers system import failed: {e}")

    # Test analytics system
    try:
        from analytics.analytics.analytics_system import AnalyticsSystem
        test_results["analytics"] = True
        print("  ✅ Analytics system imported successfully")
    except Exception as e:
        print(f"  ❌ Analytics system import failed: {e}")

    # Test lead scoring system
    try:
        from tools.lead_scoring.scoring import LeadScorer
        test_results["lead_scoring"] = True
        print("  ✅ Lead scoring system imported successfully")
    except Exception as e:
        print(f"  ❌ Lead scoring system import failed: {e}")

    # Test lead harvesting system
    try:
        from tools.lead_harvesting.scrapers.base import BaseScraper
        test_results["lead_harvesting"] = True
        print("  ✅ Lead harvesting system imported successfully")
    except Exception as e:
        print(f"  ❌ Lead harvesting system import failed: {e}")

    # Test code analysis system
    try:
        from tools.code_analysis.Agents.AgentBase import AgentBase
        test_results["code_analysis"] = True
        print("  ✅ Code analysis system imported successfully")
    except Exception as e:
        print(f"  ❌ Code analysis system import failed: {e}")

    return test_results

def test_basic_functionality():
    """Test basic functionality of extracted systems."""
    print("\n🔧 Testing Basic Functionality...")

    functionality_results = {
        "gamification_init": False,
        "memory_init": False,
        "template_render": False,
        "lead_scoring": False
    }

    # Test gamification system initialization
    try:
        from gamification.mmorpg.mmorpg_system import MMORPGConfig
        config = MMORPGConfig()
        assert config.xp_multiplier == 1.0
        functionality_results["gamification_init"] = True
        print("  ✅ Gamification config initialized successfully")
    except Exception as e:
        print(f"  ❌ Gamification config failed: {e}")

    # Test memory system initialization (without database)
    try:
        from memory.memory.manager import MemoryManager
        # Just test that the class can be instantiated (don't actually connect to DB)
        assert hasattr(MemoryManager, '__init__')
        functionality_results["memory_init"] = True
        print("  ✅ Memory manager class available")
    except Exception as e:
        print(f"  ❌ Memory manager failed: {e}")

    # Test template rendering
    try:
        from templates.templates.engine.template_engine import PromptTemplateEngine
        # Just test that the class exists and has expected methods
        assert hasattr(PromptTemplateEngine, 'render_template')
        functionality_results["template_render"] = True
        print("  ✅ Template engine class available")
    except Exception as e:
        print(f"  ❌ Template engine failed: {e}")

    # Test lead scoring
    try:
        from tools.lead_scoring.scoring import LeadScorer
        from tools.lead_harvesting.scrapers.base import Lead

        # Create a test lead
        test_lead = Lead(
            title="Python Developer Needed",
            description="Looking for experienced Python developer for web scraping project",
            url="https://example.com/job/123",
            posted_date="2024-01-01T00:00:00Z"
        )

        # Test scorer initialization
        config = {"keywords": ["python", "scraping"], "scoring": {"keyword_weight": 1.0}}
        scorer = LeadScorer(config)

        # Test scoring
        scored_lead = scorer.score(test_lead)
        assert scored_lead.score > 0  # Should get some score for keyword match
        functionality_results["lead_scoring"] = True
        print("  ✅ Lead scoring working correctly")
    except Exception as e:
        print(f"  ❌ Lead scoring failed: {e}")

    return functionality_results

def test_dependencies():
    """Test that required dependencies are available."""
    print("\n📦 Testing Dependencies...")

    dependency_results = {
        "pyqt6": False,
        "jinja2": False,
        "pandas": False,
        "torch": False,
        "faiss": False
    }

    # Test PyQt6 availability
    try:
        import PyQt6
        dependency_results["pyqt6"] = True
        print("  ✅ PyQt6 available")
    except ImportError:
        print("  ⚠️  PyQt6 not available (GUI features will be limited)")

    # Test Jinja2 availability
    try:
        import jinja2
        dependency_results["jinja2"] = True
        print("  ✅ Jinja2 available")
    except ImportError:
        print("  ❌ Jinja2 not available (template system will fail)")

    # Test pandas availability
    try:
        import pandas
        dependency_results["pandas"] = True
        print("  ✅ Pandas available")
    except ImportError:
        print("  ⚠️  Pandas not available (data processing features limited)")

    # Test torch availability
    try:
        import torch
        dependency_results["torch"] = True
        print("  ✅ PyTorch available")
    except ImportError:
        print("  ⚠️  PyTorch not available (ML features will be limited)")

    # Test FAISS availability
    try:
        import faiss
        dependency_results["faiss"] = True
        print("  ✅ FAISS available")
    except ImportError:
        print("  ⚠️  FAISS not available (vector search features will be limited)")

    return dependency_results

def generate_test_report(import_results: Dict, functionality_results: Dict, dependency_results: Dict):
    """Generate a test report."""
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST REPORT")
    print("=" * 60)

    # Summary statistics
    import_success = sum(import_results.values())
    import_total = len(import_results)
    functionality_success = sum(functionality_results.values())
    functionality_total = len(functionality_results)
    dependency_available = sum(dependency_results.values())
    dependency_total = len(dependency_results)

    print("\n📈 SUMMARY:")
    print("  Imports: {}/{} successful ({:.1f}%)".format(import_success, import_total, import_success/import_total*100))
    print("  Functionality: {}/{} working ({:.1f}%)".format(functionality_success, functionality_total, functionality_success/functionality_total*100))
    print("  Dependencies: {}/{} available ({:.1f}%)".format(dependency_available, dependency_total, dependency_available/dependency_total*100))

    # Overall health score
    overall_score = (import_success + functionality_success + dependency_available) / (import_total + functionality_total + dependency_total) * 100

    if overall_score >= 90:
        print("\n🎉 OVERALL HEALTH: EXCELLENT ({:.1f}%)".format(overall_score))
        print("   ✅ All systems ready for production use")
    elif overall_score >= 75:
        print("\n👍 OVERALL HEALTH: GOOD ({:.1f}%)".format(overall_score))
        print("   ⚠️  Minor issues to resolve before production")
    elif overall_score >= 60:
        print("\n⚠️  OVERALL HEALTH: FAIR ({:.1f}%)".format(overall_score))
        print("   🔧 Significant issues need attention")
    else:
        print("\n❌ OVERALL HEALTH: POOR ({:.1f}%)".format(overall_score))
        print("   🚨 Critical issues prevent system operation")

    # Detailed results
    print("\n🔍 DETAILED RESULTS:")
    print("System Imports:")
    for system, success in import_results.items():
        status = "✅" if success else "❌"
        print("  {} {}".format(status, system))

    print("\nBasic Functionality:")
    for test, success in functionality_results.items():
        status = "✅" if success else "❌"
        print("  {} {}".format(status, test))

    print("\nDependencies:")
    for dep, available in dependency_results.items():
        status = "✅" if available else "⚠️ "
        print("  {} {}".format(status, dep))

def main():
    """Main integration test function."""
    print("🧪 Phase 2: Integration Testing")
    print("=" * 40)

    # Run all tests
    import_results = test_system_imports()
    functionality_results = test_basic_functionality()
    dependency_results = test_dependencies()

    # Generate report
    generate_test_report(import_results, functionality_results, dependency_results)

    print("\n" + "=" * 40)
    print("✅ Phase 2: Integration testing complete!")
    print("\nNext: Database migration script creation")

if __name__ == "__main__":
    main()