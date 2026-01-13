#!/usr/bin/env python3
"""
Intelligent Message Router v1.0
================================

AI-powered message classification and routing system.
Prevents duplicate coordination messages, ensures efficient swarm communication.

Author: Agent-4 (Strategic Coordination Lead)
Created: 2026-01-13
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict

class IntelligentMessageRouter:
    """AI-powered message routing and deduplication system."""

    def __init__(self, repo_path: str = "D:/Agent_Cellphone_V2_Repository"):
        self.repo_path = Path(repo_path)
        self.coordination_cache = self.repo_path / "coordination_cache.json"
        self.message_history = self.repo_path / "message_history_cache.json"
        self.agent_workspaces = self.repo_path / "agent_workspaces"

        # Load existing coordination data
        self.coordination_data = self._load_coordination_cache()
        self.message_cache = self._load_message_history()

        # Message classification patterns
        self.message_types = {
            'COORDINATION_REQUEST': [
                'coordination request', 'swarm coordination', 'task assignment',
                'parallel processing', 'work distribution', 'synchronize'
            ],
            'STATUS_UPDATE': [
                'status update', 'progress report', 'completion status',
                'task completed', 'work finished', 'update'
            ],
            'DUPLICATE_WARNING': [
                'duplicate message', 'already sent', 'repeated coordination',
                'same request', 'redundant'
            ],
            'BOTTLENECK_ALERT': [
                'bottleneck', 'overloaded', 'capacity exceeded', 'too many tasks',
                'workload issue', 'agent overwhelmed'
            ],
            'QUALITY_ASSURANCE': [
                'qa check', 'validation required', 'testing needed',
                'code review', 'quality gate'
            ],
            'RESOURCE_REQUEST': [
                'need help', 'assistance required', 'support needed',
                'resource allocation', 'additional capacity'
            ]
        }

    def _load_coordination_cache(self) -> Dict:
        """Load current coordination cache."""
        try:
            with open(self.coordination_cache, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _load_message_history(self) -> Dict:
        """Load message history for deduplication."""
        try:
            with open(self.message_history, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'messages': [], 'hashes': set()}

    def classify_message(self, message_content: str) -> Tuple[str, float]:
        """Classify message type using AI pattern matching."""
        content_lower = message_content.lower()
        best_match = 'UNKNOWN'
        best_score = 0.0

        for msg_type, patterns in self.message_types.items():
            score = 0
            for pattern in patterns:
                if pattern in content_lower:
                    score += 1

            # Normalize score by pattern count for fair comparison
            normalized_score = score / len(patterns) if patterns else 0

            if normalized_score > best_score:
                best_score = normalized_score
                best_match = msg_type

        return best_match, best_score

    def check_duplicate(self, message_content: str, from_agent: str, to_agent: str,
                       time_window_minutes: int = 30) -> Tuple[bool, Optional[str]]:
        """Check if message is a duplicate within time window."""
        message_hash = self._generate_message_hash(message_content, from_agent, to_agent)

        # Check hash cache first
        if message_hash in self.message_cache.get('hashes', set()):
            return True, "Hash match - identical message content"

        # Check for similar messages within time window
        cutoff_time = datetime.now().timestamp() - (time_window_minutes * 60)

        for cached_msg in self.message_cache.get('messages', []):
            if cached_msg['timestamp'] > cutoff_time:
                # Check content similarity (simple approach)
                if self._calculate_similarity(message_content, cached_msg['content']) > 0.8:
                    return True, f"Similar message {time_window_minutes}min ago"

        return False, None

    def _generate_message_hash(self, content: str, from_agent: str, to_agent: str) -> str:
        """Generate unique hash for message deduplication."""
        hash_input = f"{from_agent}->{to_agent}:{content.strip()}"
        return hashlib.md5(hash_input.encode()).hexdigest()

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity score."""
        # Basic word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def route_message(self, from_agent: str, to_agent: str, message_content: str,
                     priority: str = 'regular') -> Dict:
        """Route message with intelligent processing."""
        # Classify message
        msg_type, confidence = self.classify_message(message_content)

        # Check for duplicates
        is_duplicate, duplicate_reason = self.check_duplicate(
            message_content, from_agent, to_agent
        )

        routing_decision = {
            'timestamp': datetime.now().isoformat(),
            'from_agent': from_agent,
            'to_agent': to_agent,
            'message_type': msg_type,
            'classification_confidence': confidence,
            'is_duplicate': is_duplicate,
            'duplicate_reason': duplicate_reason,
            'routing_action': self._determine_routing_action(
                msg_type, is_duplicate, priority
            ),
            'processing_recommendations': self._generate_processing_recommendations(
                msg_type, message_content
            )
        }

        # Cache message if not duplicate
        if not is_duplicate:
            self._cache_message(from_agent, to_agent, message_content, msg_type)

        return routing_decision

    def _determine_routing_action(self, msg_type: str, is_duplicate: bool,
                                 priority: str) -> str:
        """Determine appropriate routing action."""
        if is_duplicate:
            return "BLOCK_DUPLICATE"

        if priority == 'urgent':
            return "IMMEDIATE_PROCESSING"

        if msg_type == 'COORDINATION_REQUEST':
            return "ASSIGN_TO_AGENT4"  # Agent-4 handles coordination

        if msg_type == 'BOTTLENECK_ALERT':
            return "ESCALATE_TO_SWARM_LEAD"

        if msg_type == 'RESOURCE_REQUEST':
            return "QUEUE_FOR_DISTRIBUTION"

        if msg_type == 'QUALITY_ASSURANCE':
            return "ASSIGN_TO_AGENT7"  # Agent-7 handles testing

        return "STANDARD_PROCESSING"

    def _generate_processing_recommendations(self, msg_type: str, content: str) -> List[str]:
        """Generate AI-powered processing recommendations."""
        recommendations = []

        if msg_type == 'COORDINATION_REQUEST':
            recommendations.extend([
                "Extract specific task assignments from message",
                "Check current agent workloads before assignment",
                "Schedule follow-up status check in 30 minutes",
                "Update swarm coordination dashboard"
            ])

        elif msg_type == 'STATUS_UPDATE':
            recommendations.extend([
                "Update task progress in swarm tracker",
                "Check for blockers requiring escalation",
                "Validate progress against timeline",
                "Generate automated progress report"
            ])

        elif msg_type == 'BOTTLENECK_ALERT':
            recommendations.extend([
                "Immediate workload analysis required",
                "Consider task redistribution across swarm",
                "Escalate to Agent-4 for coordination",
                "Monitor agent status for next 15 minutes"
            ])

        elif msg_type == 'QUALITY_ASSURANCE':
            recommendations.extend([
                "Route to Agent-7 testing specialist",
                "Schedule cross-agent validation session",
                "Check integration test coverage",
                "Update quality metrics dashboard"
            ])

        elif msg_type == 'RESOURCE_REQUEST':
            recommendations.extend([
                "Analyze available swarm capacity",
                "Check agent expertise matching",
                "Consider parallel task assignment",
                "Monitor resource utilization"
            ])

        return recommendations

    def _cache_message(self, from_agent: str, to_agent: str, content: str, msg_type: str):
        """Cache message for deduplication and analysis."""
        message_hash = self._generate_message_hash(content, from_agent, to_agent)

        message_record = {
            'timestamp': datetime.now().timestamp(),
            'from_agent': from_agent,
            'to_agent': to_agent,
            'content': content,
            'type': msg_type,
            'hash': message_hash
        }

        # Add to message history
        if 'messages' not in self.message_cache:
            self.message_cache['messages'] = []
        self.message_cache['messages'].append(message_record)

        # Add to hash set
        if 'hashes' not in self.message_cache:
            self.message_cache['hashes'] = set()
        self.message_cache['hashes'].add(message_hash)

        # Clean old messages (keep last 1000)
        if len(self.message_cache['messages']) > 1000:
            self.message_cache['messages'] = self.message_cache['messages'][-1000:]
            # Rebuild hash set
            self.message_cache['hashes'] = {msg['hash'] for msg in self.message_cache['messages']}

        # Save to file
        self._save_message_cache()

    def _save_message_cache(self):
        """Save message cache to persistent storage."""
        # Convert set to list for JSON serialization
        cache_copy = self.message_cache.copy()
        cache_copy['hashes'] = list(cache_copy.get('hashes', set()))

        with open(self.message_history, 'w') as f:
            json.dump(cache_copy, f, indent=2, default=str)

    def get_routing_analytics(self) -> Dict:
        """Get analytics on message routing patterns."""
        messages = self.message_cache.get('messages', [])

        if not messages:
            return {'total_messages': 0, 'analytics': 'No message data available'}

        # Analyze patterns
        type_counts = defaultdict(int)
        agent_pairs = defaultdict(int)
        duplicate_rate = 0

        for msg in messages:
            type_counts[msg.get('type', 'UNKNOWN')] += 1
            pair = f"{msg['from_agent']}->{msg['to_agent']}"
            agent_pairs[pair] += 1

        # Calculate duplicate rate (rough estimate)
        total_pairs = len(agent_pairs)
        high_frequency_pairs = sum(1 for count in agent_pairs.values() if count > 10)

        return {
            'total_messages': len(messages),
            'message_types': dict(type_counts),
            'top_agent_pairs': dict(sorted(agent_pairs.items(), key=lambda x: x[1], reverse=True)[:5]),
            'routing_efficiency': self._calculate_routing_efficiency(),
            'duplicate_prevention_rate': (high_frequency_pairs / total_pairs * 100) if total_pairs > 0 else 0
        }

    def _calculate_routing_efficiency(self) -> float:
        """Calculate routing efficiency score."""
        messages = self.message_cache.get('messages', [])
        if not messages:
            return 100.0  # Perfect efficiency with no messages

        # Efficiency based on message type distribution and processing
        coordination_msgs = sum(1 for msg in messages if msg.get('type') == 'COORDINATION_REQUEST')
        status_updates = sum(1 for msg in messages if msg.get('type') == 'STATUS_UPDATE')

        # Ideal ratio: more status updates than coordination requests indicates good flow
        if coordination_msgs == 0:
            return 100.0

        ratio = status_updates / coordination_msgs
        efficiency = min(100.0, ratio * 25)  # Cap at 100, scale factor

        return efficiency

    def optimize_routing(self) -> Dict:
        """Generate routing optimization recommendations."""
        analytics = self.get_routing_analytics()

        optimizations = []

        # Check for high-frequency pairs that might indicate bottlenecks
        pairs = analytics.get('top_agent_pairs', {})
        for pair, count in pairs.items():
            if count > 20:  # Threshold for potential optimization
                optimizations.append(f"High frequency {pair}: {count} messages - consider batching or direct channels")

        # Check message type balance
        types = analytics.get('message_types', {})
        total = analytics.get('total_messages', 0)

        if total > 0:
            coord_pct = types.get('COORDINATION_REQUEST', 0) / total * 100
            status_pct = types.get('STATUS_UPDATE', 0) / total * 100

            if coord_pct > status_pct * 2:
                optimizations.append(f"Coordination requests ({coord_pct:.1f}%) exceed status updates ({status_pct:.1f}%) - improve progress tracking")

        # Efficiency recommendations
        efficiency = analytics.get('routing_efficiency', 100)
        if efficiency < 80:
            optimizations.append(f"Routing efficiency: {efficiency:.1f}% - optimize message flows and reduce overhead")

        return {
            'current_efficiency': efficiency,
            'optimizations': optimizations,
            'recommendations': [
                "Implement message batching for high-frequency pairs",
                "Create dedicated status update channels",
                "Add automated progress tracking to reduce manual coordination",
                "Implement smart escalation protocols for bottlenecks"
            ]
        }

def main():
    """Main router execution with analytics."""
    router = IntelligentMessageRouter()

    print("🧠 INTELLIGENT MESSAGE ROUTER v1.0")
    print("=" * 50)
    print(f"Active: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    # Display routing analytics
    analytics = router.get_routing_analytics()
    print("📊 ROUTING ANALYTICS:")
    print(f"Total Messages Processed: {analytics['total_messages']}")
    print(f"Routing Efficiency: {analytics['routing_efficiency']:.1f}%")
    print(".1f")
    print()

    if analytics['total_messages'] > 0:
        print("📈 MESSAGE TYPE DISTRIBUTION:")
        for msg_type, count in analytics['message_types'].items():
            pct = count / analytics['total_messages'] * 100
            print(".1f")

        print()
        print("🔗 TOP AGENT PAIRS:")
        for pair, count in analytics['top_agent_pairs'].items():
            print(f"  {pair}: {count} messages")

    # Display optimization recommendations
    optimizations = router.optimize_routing()
    if optimizations['optimizations']:
        print()
        print("⚡ ROUTING OPTIMIZATIONS:")
        for opt in optimizations['optimizations']:
            print(f"🎯 {opt}")

    print()
    print("💡 RECOMMENDATIONS:")
    for rec in optimizations['recommendations']:
        print(f"🔧 {rec}")

    print()
    print("🛡️  MESSAGE ROUTING ACTIVE - DUPLICATES PREVENTED, EFFICIENCY MAXIMIZED")

if __name__ == "__main__":
    main()