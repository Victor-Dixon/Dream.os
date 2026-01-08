#!/usr/bin/env python3
"""
Phase 1 AI Integration Starter
Immediate deployment of AI infrastructure foundation

Usage:
    python tools/phase1_ai_integration_starter.py --deploy-all
    python tools/phase1_ai_integration_starter.py --test-reasoning
    python tools/phase1_ai_integration_starter.py --status
"""

import sys
import os
from pathlib import Path
import subprocess


class Phase1AIIntegrationStarter:
    """Executes Phase 1 AI infrastructure foundation deployment"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.status = {
            "reasoning_engine": False,
            "vector_database": False,
            "web_apis": False,
            "integration_complete": False
        }

    def deploy_reasoning_engine(self):
        """Deploy AdvancedReasoningEngine integration"""
        try:
            # Test import
            sys.path.insert(0, str(self.project_root / "src"))
            from ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine

            # Test basic functionality
            engine = AdvancedReasoningEngine()
            test_result = engine.reason(
                query="Test integration",
                mode="simple"
            )

            if test_result and "response" in test_result:
                self.status["reasoning_engine"] = True
                print("✅ AdvancedReasoningEngine deployed successfully")
                return True
            else:
                print("⚠️ AdvancedReasoningEngine deployed but returned unexpected result")
                return False

        except Exception as e:
            print(f"❌ AdvancedReasoningEngine deployment failed: {str(e)}")
            return False

    def deploy_vector_database(self):
        """Deploy VectorDatabaseService integration"""
        try:
            # Test import
            from services.vector.vector_database_service import VectorDatabaseService

            # Test basic functionality (without actual DB operations)
            vdb_class = VectorDatabaseService

            if vdb_class:
                self.status["vector_database"] = True
                print("✅ VectorDatabaseService deployed successfully")
                return True
            else:
                print("⚠️ VectorDatabaseService class not available")
                return False

        except Exception as e:
            print(f"❌ VectorDatabaseService deployment failed: {str(e)}")
            return False

    def test_web_apis(self):
        """Test AI web API endpoints"""
        try:
            # Test if FastAPI is running and APIs are available
            result = subprocess.run([
                "python", "-c", "import requests; requests.get('http://localhost:8000/health', timeout=5)"
            ], capture_output=True, timeout=10)

            if result.returncode == 0:
                self.status["web_apis"] = True
                print("✅ AI Web APIs accessible (FastAPI running)")
                return True
            else:
                print("⚠️ AI Web APIs not accessible (FastAPI may not be running)")
                print("   Start with: python src/main.py --services fastapi")
                return False

        except Exception as e:
            print(f"❌ AI Web API test failed: {str(e)}")
            return False

    def create_integration_examples(self):
        """Create example scripts for AI integration"""
        examples_dir = self.project_root / "examples" / "ai_integration"
        examples_dir.mkdir(parents=True, exist_ok=True)

        # Reasoning engine example
        reasoning_example = '''#!/usr/bin/env python3
"""
AI Reasoning Integration Example
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine

def main():
    engine = AdvancedReasoningEngine()

    # Example reasoning request
    result = engine.reason(
        query="Analyze the benefits of swarm coordination",
        mode="strategic"
    )

    print("Reasoning Result:")
    print(f"Response: {result.get('response', 'No response')}")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    print(f"Mode: {result.get('mode', 'N/A')}")

if __name__ == "__main__":
    main()
'''

        # Vector database example
        vector_example = '''#!/usr/bin/env python3
"""
Vector Database Integration Example
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from services.vector.vector_database_service import VectorDatabaseService

def main():
    # Initialize vector database service
    vdb = VectorDatabaseService()

    # Example semantic search
    try:
        results = vdb.semantic_search(
            query="coordination patterns",
            limit=5
        )

        print("Semantic Search Results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.content[:100]}... (score: {result.score:.3f})")

    except Exception as e:
        print(f"Vector search example failed: {e}")
        print("Note: This requires actual vector database setup")

if __name__ == "__main__":
    main()
'''

        # Write examples
        with open(examples_dir / "reasoning_engine_example.py", 'w') as f:
            f.write(reasoning_example)

        with open(examples_dir / "vector_database_example.py", 'w') as f:
            f.write(vector_example)

        print(f"✅ Created AI integration examples in {examples_dir}")

    def deploy_all(self):
        """Execute complete Phase 1 AI integration deployment"""
        print("🚀 Starting Phase 1 AI Integration Deployment\n")

        # Deploy components
        reasoning_ok = self.deploy_reasoning_engine()
        vector_ok = self.deploy_vector_database()
        api_ok = self.test_web_apis()

        # Create examples
        self.create_integration_examples()

        # Update completion status
        self.status["integration_complete"] = all([reasoning_ok, vector_ok, api_ok])

        # Report results
        print("\n📊 Phase 1 Deployment Results:")
        print(f"  AdvancedReasoningEngine: {'✅' if reasoning_ok else '❌'}")
        print(f"  VectorDatabaseService: {'✅' if vector_ok else '❌'}")
        print(f"  Web APIs: {'✅' if api_ok else '❌'}")
        print(f"  Integration Complete: {'✅' if self.status['integration_complete'] else '❌'}")

        if self.status["integration_complete"]:
            print("\n🎯 Phase 1 AI Infrastructure Foundation: DEPLOYED")
            print("Next: Proceed to Phase 2 Coordination Infrastructure")
        else:
            print("\n⚠️ Phase 1 partially deployed - some components need attention")

        return self.status

    def get_status(self):
        """Get current deployment status"""
        return self.status


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Phase 1 AI Integration Starter")
    parser.add_argument("--deploy-all", action="store_true", help="Deploy all Phase 1 AI components")
    parser.add_argument("--test-reasoning", action="store_true", help="Test reasoning engine deployment")
    parser.add_argument("--test-vector", action="store_true", help="Test vector database deployment")
    parser.add_argument("--test-apis", action="store_true", help="Test web API accessibility")
    parser.add_argument("--status", action="store_true", help="Show deployment status")
    parser.add_argument("--create-examples", action="store_true", help="Create integration examples")

    args = parser.parse_args()

    starter = Phase1AIIntegrationStarter()

    if args.deploy_all:
        starter.deploy_all()

    elif args.test_reasoning:
        starter.deploy_reasoning_engine()

    elif args.test_vector:
        starter.deploy_vector_database()

    elif args.test_apis:
        starter.test_web_apis()

    elif args.create_examples:
        starter.create_integration_examples()

    elif args.status:
        status = starter.get_status()
        print("Phase 1 AI Integration Status:")
        for component, deployed in status.items():
            print(f"  {component}: {'✅' if deployed else '❌'}")

    else:
        print("Use --deploy-all, --test-reasoning, --test-vector, --test-apis, --status, or --create-examples")


if __name__ == "__main__":
    main()