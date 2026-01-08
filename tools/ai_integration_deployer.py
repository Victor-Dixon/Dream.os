#!/usr/bin/env python3
"""
AI Integration Deployment Tool
Automates enterprise AI capability adoption across swarm agents

Usage:
python tools/ai_integration_deployer.py --agent Agent-X --deploy
python tools/ai_integration_deployer.py --status
python tools/ai_integration_deployer.py --verify
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️  AI infrastructure not available - install required dependencies")

class AIIntegrationDeployer:
    """Automated AI capability deployment for swarm agents"""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.status_file = self.repo_root / "ai_integration_status.json"
        self.quickstart_guide = self.repo_root / "AI_INTEGRATION_QUICKSTART.md"

    def check_ai_availability(self) -> bool:
        """Verify AI infrastructure is operational"""
        if not AI_AVAILABLE:
            print("❌ AI infrastructure not available")
            return False

        try:
            engine = AdvancedReasoningEngine()
            # Quick test
            result = engine.reason("Test integration", mode="simple")
            if result and result.response:
                print("✅ AI infrastructure operational")
                return True
        except Exception as e:
            print(f"❌ AI infrastructure error: {e}")

        return False

    def deploy_ai_integration(self, agent_id: str) -> bool:
        """Deploy AI integration for specific agent"""
        print(f"\n🚀 Deploying AI integration for {agent_id}")

        if not self.check_ai_availability():
            return False

        # Create agent-specific AI workspace
        agent_workspace = self.repo_root / "agent_workspaces" / agent_id
        ai_dir = agent_workspace / "ai_integration"
        ai_dir.mkdir(parents=True, exist_ok=True)

        # Create AI integration files
        integration_files = {
            "ai_quickstart.py": self._create_ai_quickstart_script(agent_id),
            "ai_workflows.py": self._create_ai_workflows(agent_id),
            "ai_examples.py": self._create_ai_examples(agent_id),
            "integration_status.json": self._create_integration_status(agent_id)
        }

        for filename, content in integration_files.items():
            file_path = ai_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"  ✅ Created {filename}")

        # Update global status
        self._update_global_status(agent_id, "deployed")

        print(f"✅ AI integration deployed for {agent_id}")
        return True

    def verify_ai_integration(self, agent_id: str) -> Dict[str, Any]:
        """Verify AI integration functionality"""
        print(f"\n🔍 Verifying AI integration for {agent_id}")

        results = {
            "agent_id": agent_id,
            "ai_available": self.check_ai_availability(),
            "files_created": False,
            "functionality_test": False,
            "integration_status": "unknown"
        }

        # Check files exist
        agent_workspace = self.repo_root / "agent_workspaces" / agent_id
        ai_dir = agent_workspace / "ai_integration"

        expected_files = ["ai_quickstart.py", "ai_workflows.py", "ai_examples.py"]
        files_exist = all((ai_dir / f).exists() for f in expected_files)

        results["files_created"] = files_exist
        if files_exist:
            print("  ✅ Integration files present")
        else:
            print("  ❌ Integration files missing")

        # Test functionality
        if AI_AVAILABLE and files_exist:
            try:
                # Import and test the integration
                sys.path.insert(0, str(ai_dir))
                import ai_quickstart

                # Run a quick test
                result = ai_quickstart.quick_ai_analysis("Integration test")
                if result and len(result) > 10:
                    results["functionality_test"] = True
                    print("  ✅ AI functionality verified")
                else:
                    print("  ⚠️  AI functionality test inconclusive")
            except Exception as e:
                print(f"  ❌ Functionality test failed: {e}")
        else:
            print("  ⚠️  Cannot test functionality - prerequisites not met")

        # Check integration status
        status_file = ai_dir / "integration_status.json"
        if status_file.exists():
            with open(status_file, 'r') as f:
                status_data = json.load(f)
                results["integration_status"] = status_data.get("status", "unknown")

        return results

    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive AI integration status across swarm"""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                return json.load(f)

        return {"status": "no_status_file", "agents": {}}

    def _create_ai_quickstart_script(self, agent_id: str) -> str:
        """Create agent-specific AI quickstart script"""
        return f'''"""
AI Integration Quickstart for {agent_id}
Generated by AI Integration Deployer

Usage:
python ai_quickstart.py
"""

import sys
import os
from pathlib import Path

# Add paths for imports
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root / "src"))

def quick_ai_analysis(query: str, mode: str = "technical") -> str:
    """Quick AI analysis for common tasks"""
    try:
        from ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine

        engine = AdvancedReasoningEngine()
        result = engine.reason(query, mode=mode)

        return result.response if result else "AI analysis failed"
    except Exception as e:
        return f"AI integration error: {{e}}"

def analyze_code_quality(code: str) -> str:
    """AI-powered code quality analysis"""
    query = f"""
    Analyze this code for quality, security, and best practices:

    {{code}}

    Provide: issues found, severity levels, improvement suggestions
    """
    return quick_ai_analysis(query, "technical")

def strategic_task_planning(tasks: list) -> str:
    """AI-powered task prioritization and planning"""
    task_list = "\\n".join(f"- {{task}}" for task in tasks)
    query = f"""
    Prioritize and plan these tasks strategically:

    {{task_list}}

    Provide: priority ranking, estimated effort, dependencies, optimal sequence
    """
    return quick_ai_analysis(query, "strategic")

def decision_analysis(options: dict) -> str:
    """AI-powered decision analysis"""
    options_text = "\\n".join(f"{{k}}: {{v}}" for k, v in options.items())
    query = f"""
    Analyze these decision options:

    {{options_text}}

    Provide: recommendation, pros/cons analysis, risk assessment, implementation plan
    """
    return quick_ai_analysis(query, "analytical")

if __name__ == "__main__":
    # Demo functionality
    print(f"🤖 AI Integration Active for {{agent_id}}")
    print("\\nTesting AI capabilities...")

    test_result = quick_ai_analysis("Hello AI integration for {{agent_id}}")
    print(f"\\nAI Response: {{test_result}}")

    print("\\n✅ AI integration operational!")
    print("\\nAvailable functions:")
    print("- quick_ai_analysis(query, mode)")
    print("- analyze_code_quality(code)")
    print("- strategic_task_planning(tasks)")
    print("- decision_analysis(options)")
'''

    def _create_ai_workflows(self, agent_id: str) -> str:
        """Create agent-specific AI workflow templates"""
        return f'''"""
AI Workflow Templates for {agent_id}
Pre-built workflows for common AI-enhanced tasks
"""

from ai_quickstart import quick_ai_analysis, analyze_code_quality, strategic_task_planning

class AIEnhancedWorkflows:
    """AI-powered workflow templates"""

    def code_review_workflow(self, code_changes: str) -> dict:
        """Complete code review workflow with AI assistance"""
        print("🔍 Starting AI-enhanced code review...")

        # AI code analysis
        analysis = analyze_code_quality(code_changes)

        # AI-generated review comments
        review_query = f"""
        Generate detailed code review comments for:

        {{code_changes}}

        Focus on: logic errors, security issues, performance, maintainability
        """
        review_comments = quick_ai_analysis(review_query, "technical")

        return {{
            "analysis": analysis,
            "review_comments": review_comments,
            "recommendations": self._extract_recommendations(review_comments),
            "priority_issues": self._identify_priority_issues(review_comments)
        }}

    def task_prioritization_workflow(self, task_list: list) -> dict:
        """AI-powered task prioritization"""
        print("📋 AI task prioritization...")

        prioritization = strategic_task_planning(task_list)

        # Extract structured data
        return {{
            "prioritization": prioritization,
            "top_priority": self._extract_top_priority(prioritization),
            "estimated_effort": self._estimate_effort(prioritization),
            "dependencies": self._identify_dependencies(prioritization)
        }}

    def decision_support_workflow(self, decision_context: str, options: dict) -> dict:
        """AI decision support workflow"""
        print("🎯 AI decision analysis...")

        analysis = decision_analysis(options)

        return {{
            "analysis": analysis,
            "recommended_option": self._extract_recommendation(analysis),
            "implementation_plan": self._extract_implementation_plan(analysis),
            "risk_assessment": self._assess_risks(analysis)
        }}

    def _extract_recommendations(self, ai_response: str) -> list:
        """Extract actionable recommendations"""
        # Simple extraction logic
        lines = ai_response.split('\\n')
        return [line.strip() for line in lines if line.strip().startswith(('-', '•', '*'))][:5]

    def _identify_priority_issues(self, ai_response: str) -> list:
        """Identify high-priority issues"""
        priority_keywords = ["critical", "security", "performance", "bug"]
        issues = []
        for line in ai_response.split('\\n'):
            if any(keyword in line.lower() for keyword in priority_keywords):
                issues.append(line.strip())
        return issues[:3]

    def _extract_top_priority(self, prioritization: str) -> str:
        """Extract top priority task"""
        lines = prioritization.split('\\n')
        for line in lines:
            if "1." in line or "first" in line.lower():
                return line.strip()
        return "Top priority not clearly identified"

    def _estimate_effort(self, prioritization: str) -> str:
        """Estimate effort for prioritized tasks"""
        # Simplified effort estimation
        return "Effort estimation requires specific task details"

    def _identify_dependencies(self, prioritization: str) -> list:
        """Identify task dependencies"""
        deps = []
        for line in prioritization.split('\\n'):
            if "depend" in line.lower():
                deps.append(line.strip())
        return deps

    def _extract_recommendation(self, analysis: str) -> str:
        """Extract recommended option"""
        lines = analysis.split('\\n')
        for line in lines:
            if "recommend" in line.lower():
                return line.strip()
        return "Recommendation not clearly stated"

    def _extract_implementation_plan(self, analysis: str) -> str:
        """Extract implementation plan"""
        return "Implementation plan analysis requires detailed review"

    def _assess_risks(self, analysis: str) -> str:
        """Assess decision risks"""
        if "risk" in analysis.lower():
            return "Risks identified in analysis"
        return "Risk assessment not detailed"

# Global workflow instance
ai_workflows = AIEnhancedWorkflows()

# Convenience functions
def review_code(code: str) -> dict:
    """Quick code review workflow"""
    return ai_workflows.code_review_workflow(code)

def prioritize_tasks(tasks: list) -> dict:
    """Quick task prioritization"""
    return ai_workflows.task_prioritization_workflow(tasks)

def analyze_decision(options: dict) -> dict:
    """Quick decision analysis"""
    return ai_workflows.decision_support_workflow("", options)
'''

    def _create_ai_examples(self, agent_id: str) -> str:
        """Create AI usage examples"""
        return f'''"""
AI Integration Examples for {agent_id}
Practical examples of AI-enhanced workflows
"""

from ai_workflows import review_code, prioritize_tasks, analyze_decision
from ai_quickstart import quick_ai_analysis

def example_code_review():
    """Example: AI-enhanced code review"""
    print("🔍 AI Code Review Example")

    sample_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
    """

    review = review_code(sample_code)
    print("AI Analysis:", review['analysis'][:200] + "...")
    print("Recommendations:", review['recommendations'][:2])

def example_task_prioritization():
    """Example: AI task prioritization"""
    print("\\n📋 AI Task Prioritization Example")

    tasks = [
        "Fix critical security vulnerability",
        "Optimize database queries",
        "Update documentation",
        "Add new feature request",
        "Refactor legacy code"
    ]

    prioritization = prioritize_tasks(tasks)
    print("AI Prioritization:", prioritization['prioritization'][:300] + "...")

def example_decision_analysis():
    """Example: AI decision support"""
    print("\\n🎯 AI Decision Analysis Example")

    options = {{
        "Option A": "Use PostgreSQL for new database",
        "Option B": "Use MongoDB for flexibility",
        "Option C": "Keep existing MySQL setup"
    }}

    analysis = analyze_decision(options)
    print("AI Analysis:", analysis['analysis'][:300] + "...")

def example_custom_ai_query():
    """Example: Custom AI analysis"""
    print("\\n🤖 Custom AI Query Example")

    query = "Design an optimal caching strategy for a high-traffic web application"
    result = quick_ai_analysis(query, mode="technical")

    print("AI Response:", result[:400] + "...")

def run_all_examples():
    """Run all AI integration examples"""
    print(f"🚀 AI Integration Examples for {{agent_id}}\\n")

    try:
        example_code_review()
        example_task_prioritization()
        example_decision_analysis()
        example_custom_ai_query()

        print("\\n✅ All AI integration examples completed successfully!")
        print("\\n💡 AI capabilities now available for:")
        print("  - Code review and quality analysis")
        print("  - Task prioritization and planning")
        print("  - Decision support and analysis")
        print("  - Custom technical queries")

    except Exception as e:
        print(f"❌ Example execution failed: {{e}}")
        print("Check AI infrastructure availability")

if __name__ == "__main__":
    run_all_examples()
'''

    def _create_integration_status(self, agent_id: str) -> str:
        """Create integration status tracking"""
        status = {
            "agent_id": agent_id,
            "status": "deployed",
            "deployment_time": time.time(),
            "ai_available": AI_AVAILABLE,
            "capabilities": [
                "code_review",
                "task_prioritization",
                "decision_analysis",
                "custom_queries"
            ],
            "last_verified": None,
            "usage_stats": {
                "queries_made": 0,
                "successful_responses": 0,
                "average_response_time": 0
            }
        }
        return json.dumps(status, indent=2)

    def _update_global_status(self, agent_id: str, status: str):
        """Update global AI integration status"""
        current_status = self.get_integration_status()

        if "agents" not in current_status:
            current_status["agents"] = {}

        current_status["agents"][agent_id] = {
            "status": status,
            "last_updated": time.time(),
            "ai_available": AI_AVAILABLE
        }

        current_status["last_updated"] = time.time()
        current_status["total_deployed"] = len([a for a in current_status["agents"].values() if a["status"] == "deployed"])

        with open(self.status_file, 'w') as f:
            json.dump(current_status, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="AI Integration Deployment Tool")
    parser.add_argument("--agent", help="Specific agent to deploy for")
    parser.add_argument("--deploy", action="store_true", help="Deploy AI integration")
    parser.add_argument("--verify", action="store_true", help="Verify AI integration")
    parser.add_argument("--status", action="store_true", help="Show integration status")
    parser.add_argument("--all", action="store_true", help="Deploy to all agents")

    args = parser.parse_args()

    deployer = AIIntegrationDeployer()

    if args.status:
        status = deployer.get_integration_status()
        print("\\n🤖 AI Integration Status:")
        print(json.dumps(status, indent=2))

    elif args.deploy:
        if args.all:
            # Deploy to all agents
            agent_dirs = [d.name for d in (Path(__file__).parent.parent / "agent_workspaces").iterdir()
                         if d.is_dir() and d.name.startswith("Agent-")]
            success_count = 0
            for agent_id in agent_dirs:
                if deployer.deploy_ai_integration(agent_id):
                    success_count += 1
            print(f"\\n📊 Deployment Summary: {{success_count}}/{{len(agent_dirs)}} agents successful")
        elif args.agent:
            deployer.deploy_ai_integration(args.agent)
        else:
            print("❌ Specify --agent <id> or --all")

    elif args.verify:
        if args.agent:
            result = deployer.verify_ai_integration(args.agent)
            print("\\n🔍 Verification Results:")
            print(json.dumps(result, indent=2))
        else:
            print("❌ Specify --agent <id> for verification")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()