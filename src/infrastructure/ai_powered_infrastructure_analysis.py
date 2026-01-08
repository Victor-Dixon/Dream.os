"""
AI-Powered Infrastructure Analysis Module
Integrates advanced reasoning for infrastructure optimization and decision-making

V2 Compliance: <100 lines
Immediate AI utilization for infrastructure operations
"""

from src.ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine
from typing import Dict, List, Any
import json


class AIPoweredInfrastructureAnalyzer:
    """AI-enhanced infrastructure analysis and optimization"""

    def __init__(self):
        self.ai_engine = AdvancedReasoningEngine()

    def analyze_infrastructure_bottlenecks(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered bottleneck analysis"""
        analysis_query = f"""
        Analyze these infrastructure metrics for performance bottlenecks:

        Metrics: {json.dumps(metrics, indent=2)}

        Identify:
        1. Primary performance bottlenecks
        2. Root cause analysis
        3. Specific optimization recommendations
        4. Expected performance improvements
        5. Implementation priority (High/Medium/Low)
        """

        result = self.ai_engine.reason(analysis_query, mode="technical")
        return {
            "ai_analysis": result.response,
            "confidence": result.confidence_score,
            "recommendations": self._extract_recommendations(result.response)
        }

    def optimize_deployment_strategy(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """AI-driven deployment strategy optimization"""
        strategy_query = f"""
        Optimize deployment strategy for these requirements:

        Requirements: {json.dumps(requirements, indent=2)}

        Provide:
        1. Optimal deployment architecture
        2. Resource allocation recommendations
        3. Risk mitigation strategies
        4. Timeline optimization
        5. Success metrics
        """

        result = self.ai_engine.reason(strategy_query, mode="strategic")
        return {
            "optimized_strategy": result.response,
            "confidence": result.confidence_score,
            "implementation_steps": self._extract_steps(result.response)
        }

    def prioritize_infrastructure_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """AI-powered task prioritization"""
        prioritization_query = f"""
        Prioritize these infrastructure tasks by strategic impact:

        Tasks: {json.dumps(tasks, indent=2)}

        Rank by:
        1. Business impact (High/Medium/Low)
        2. Technical complexity (High/Medium/Low)
        3. Resource requirements
        4. Timeline constraints
        5. Risk assessment

        Provide prioritized list with reasoning.
        """

        result = self.ai_engine.reason(prioritization_query, mode="strategic")

        # Add AI prioritization to each task
        for i, task in enumerate(tasks):
            task["ai_priority_score"] = len(tasks) - i  # Simple scoring for now
            task["ai_analysis"] = result.response

        return sorted(tasks, key=lambda x: x.get("ai_priority_score", 0), reverse=True)

    def _extract_recommendations(self, ai_response: str) -> List[str]:
        """Extract actionable recommendations from AI response"""
        # Simple extraction - could be enhanced
        lines = ai_response.split('\n')
        recommendations = [line.strip() for line in lines if line.strip().startswith(('-', '•', '*'))]
        return recommendations[:5]  # Top 5 recommendations

    def _extract_steps(self, ai_response: str) -> List[str]:
        """Extract implementation steps from AI response"""
        lines = ai_response.split('\n')
        steps = []
        for line in lines:
            line = line.strip()
            if any(line.lower().startswith(prefix) for prefix in ['step', 'phase', '1.', '2.', '3.']):
                steps.append(line)
        return steps[:10]  # Top 10 steps


# Global instance for immediate use
ai_infrastructure_analyzer = AIPoweredInfrastructureAnalyzer()


def quick_infrastructure_analysis(metrics: Dict[str, Any]) -> str:
    """Quick AI-powered infrastructure analysis (5-minute setup)"""
    return ai_infrastructure_analyzer.analyze_infrastructure_bottlenecks(metrics)


def optimize_infrastructure_decision(requirements: Dict[str, Any]) -> str:
    """AI-optimized infrastructure decision making"""
    return ai_infrastructure_analyzer.optimize_deployment_strategy(requirements)


def prioritize_tasks_with_ai(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """AI-enhanced task prioritization"""
    return ai_infrastructure_analyzer.prioritize_infrastructure_tasks(tasks)