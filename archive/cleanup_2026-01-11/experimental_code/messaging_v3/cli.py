#!/usr/bin/env python3
"""
Simple CLI for Messaging V3
"""

import argparse
import logging
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(parent_dir))

from message import Message
from queue import MessageQueue
from delivery import send_message
from features import MessagingFeatures

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(description="Messaging V3 CLI")

    parser.add_argument(
        "--agent", "-a",
        required=True,
        help="Target agent (Agent-1 through Agent-8)"
    )

    parser.add_argument(
        "--message", "-m",
        required=True,
        help="Message content"
    )

    parser.add_argument(
        "--sender", "-s",
        default="system",
        help="Sender identifier"
    )

    parser.add_argument(
        "--priority", "-p",
        choices=["low", "normal", "high", "urgent"],
        default="normal",
        help="Message priority"
    )

    parser.add_argument(
        "--category", "-c",
        choices=["direct", "a2a", "broadcast"],
        default="direct",
        help="Message category"
    )

    parser.add_argument(
        "--queue-only", "-q",
        action="store_true",
        help="Only queue message, don't deliver immediately"
    )

    parser.add_argument(
        "--process-queue",
        action="store_true",
        help="Process queued messages"
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show queue status"
    )

    # Advanced features from old system
    parser.add_argument(
        "--a2a-coordination",
        action="store_true",
        help="Send A2A coordination message"
    )

    parser.add_argument(
        "--broadcast",
        action="store_true",
        help="Broadcast message to all agents"
    )

    parser.add_argument(
        "--soft-onboarding",
        help="Send soft onboarding to specified agent"
    )

    parser.add_argument(
        "--hard-onboarding",
        help="Send hard onboarding to specified agent"
    )

    parser.add_argument(
        "--survey-coordination",
        action="store_true",
        help="Initiate survey coordination"
    )

    parser.add_argument(
        "--consolidation-coordination",
        action="store_true",
        help="Initiate consolidation coordination"
    )

    parser.add_argument(
        "--consolidation-batch",
        default="DEFAULT",
        help="Consolidation batch ID"
    )

    parser.add_argument(
        "--consolidation-status",
        default="INITIATED",
        help="Consolidation status"
    )

    # Task management (from old system)
    parser.add_argument(
        "--get-next-task",
        action="store_true",
        help="Get next task for specified agent"
    )

    parser.add_argument(
        "--complete-task",
        help="Mark task as completed (requires task ID)"
    )

    parser.add_argument(
        "--list-tasks",
        action="store_true",
        help="List all available tasks"
    )

    parser.add_argument(
        "--task-status",
        help="Check status of specific task"
    )

    # Status and monitoring (from old system)
    parser.add_argument(
        "--leaderboard",
        action="store_true",
        help="Show agent performance leaderboard"
    )

    parser.add_argument(
        "--robinhood-stats",
        action="store_true",
        help="Show Robinhood trading statistics"
    )

    # Work management (from old system)
    parser.add_argument(
        "--generate-work-resume",
        action="store_true",
        help="Generate work resume for agent"
    )

    parser.add_argument(
        "--save-resume",
        action="store_true",
        help="Save generated resume to file"
    )

    # Infrastructure health (from old system)
    parser.add_argument(
        "--infra-health",
        action="store_true",
        help="Perform infrastructure health check"
    )

    # Resend failed messages (from old system)
    parser.add_argument(
        "--resend-failed",
        action="store_true",
        help="Reset failed messages to PENDING for retry"
    )

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    features = MessagingFeatures()

    try:
        if args.status:
            # Show queue status
            queue = MessageQueue()
            count = queue.count()
            print(f"📋 Queue Status: {count} messages")

            if count > 0:
                messages = queue.peek(5)
                print("Recent messages:")
                for i, msg in enumerate(messages):
                    print(f"  {i+1}. {msg.sender} → {msg.recipient}: {msg.content[:50]}...")
            return 0

        if args.process_queue:
            # Process queued messages
            queue = MessageQueue()
            messages = queue.dequeue(10)  # Process up to 10 messages

            if not messages:
                print("📋 No messages to process")
                return 0

            success_count = 0
            for msg in messages:
                try:
                    if send_message(msg.recipient, msg.content, msg.sender):
                        success_count += 1
                        print(f"✅ Delivered to {msg.recipient}")
                    else:
                        print(f"❌ Failed to deliver to {msg.recipient}")
                except Exception as e:
                    print(f"❌ Error delivering to {msg.recipient}: {e}")

            print(f"📊 Processed {len(messages)} messages, {success_count} successful")
            return 0

        # Advanced features
        if args.a2a_coordination:
            if not args.message:
                print("❌ ERROR: --message required for A2A coordination")
                return 1
            if features.send_a2a_coordination(args.sender, args.agent, args.message):
                print(f"✅ A2A coordination sent to {args.agent}")
            else:
                print(f"⚠️ A2A coordination queued for {args.agent}")
            return 0

        if args.broadcast:
            if not args.message:
                print("❌ ERROR: --message required for broadcast")
                return 1
            success_count = features.broadcast_message(args.sender, args.message, args.priority)
            print(f"📊 Broadcast sent to agents, {success_count} immediate deliveries")
            return 0

        if args.soft_onboarding:
            if features.send_soft_onboarding(args.soft_onboarding, args.sender):
                print(f"✅ Soft onboarding sent to {args.soft_onboarding}")
            else:
                print(f"⚠️ Soft onboarding queued for {args.soft_onboarding}")
            return 0

        if args.hard_onboarding:
            if features.send_hard_onboarding(args.hard_onboarding, args.sender):
                print(f"✅ Hard onboarding sent to {args.hard_onboarding}")
            else:
                print(f"⚠️ Hard onboarding queued for {args.hard_onboarding}")
            return 0

        if args.survey_coordination:
            if features.coordinate_survey():
                print("✅ Survey coordination initiated")
            else:
                print("❌ Survey coordination failed")
            return 0

        if args.consolidation_coordination:
            if features.coordinate_consolidation(args.consolidation_batch, args.consolidation_status):
                print(f"✅ Consolidation coordination initiated (batch: {args.consolidation_batch})")
            else:
                print("❌ Consolidation coordination failed")
            return 0

        # Task management commands
        if args.get_next_task:
            if not args.agent:
                print("❌ ERROR: --agent required for --get-next-task")
                return 1
            task = features.get_next_task(args.agent)
            if task:
                print(f"📋 Next task for {args.agent}: {task}")
            else:
                print(f"📋 No tasks available for {args.agent}")
            return 0

        if args.complete_task:
            if not args.agent:
                print("❌ ERROR: --agent required for --complete-task")
                return 1
            if features.complete_task(args.complete_task, args.agent):
                print(f"✅ Task {args.complete_task} marked as completed by {args.agent}")
            else:
                print(f"❌ Failed to complete task {args.complete_task}")
            return 0

        if args.list_tasks:
            print("📋 Task management integration not yet fully implemented")
            print("   This would show all available tasks across agents")
            return 0

        if args.task_status:
            print(f"📋 Task status for {args.task_status}: Integration not yet implemented")
            return 0

        # Status and monitoring commands
        if args.leaderboard:
            leaderboard = features.get_leaderboard()
            print("🏆 Agent Performance Leaderboard")
            print(f"   Total Agents: {leaderboard.get('total_agents', 0)}")
            print(f"   Active Agents: {leaderboard.get('active_agents', 0)}")
            if leaderboard.get('error'):
                print(f"   Error: {leaderboard['error']}")
            return 0

        if args.robinhood_stats:
            stats = features.get_robinhood_stats()
            print("📈 Robinhood Trading Statistics")
            print(f"   Total Trades: {stats.get('total_trades', 0)}")
            print(f"   Win Rate: {stats.get('win_rate', 0.0):.1%}")
            print(f"   Total P&L: ${stats.get('total_pnl', 0.0):.2f}")
            print(f"   Active Positions: {stats.get('active_positions', 0)}")
            if stats.get('error'):
                print(f"   Note: {stats['error']}")
            return 0

        # Work management commands
        if args.generate_work_resume:
            if not args.agent:
                print("❌ ERROR: --agent required for --generate-work-resume")
                return 1

            resume = features.generate_work_resume(
                args.agent,
                include_recent_commits=True,
                include_coordination=True,
                include_devlogs=True
            )

            print(resume)

            if args.save_resume:
                try:
                    filename = f"work_resume_{args.agent}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                    with open(filename, 'w') as f:
                        f.write(resume)
                    print(f"\\n✅ Work resume saved to: {filename}")
                except Exception as e:
                    print(f"\\n❌ Failed to save resume: {e}")

            return 0

        # Infrastructure health command
        if args.infra_health:
            print("🔍 Performing Infrastructure Health Check...")
            health_report = features.perform_infrastructure_health_check()

            print(f"📊 Overall Status: {health_report.get('overall_status', 'unknown').upper()}")

            # Messaging health
            messaging = health_report.get('messaging', {})
            print(f"   📨 Messaging: {messaging.get('status', 'unknown')} (Queue: {messaging.get('queue_size', 0)})")

            # Agent health
            agents = health_report.get('agents', {})
            healthy_count = sum(1 for status in agents.values() if status == 'healthy')
            print(f"   🤖 Agents: {healthy_count}/{len(agents)} healthy")

            # Recommendations
            recommendations = health_report.get('recommendations', [])
            if recommendations:
                print("   💡 Recommendations:")
                for rec in recommendations:
                    print(f"      • {rec}")

            if health_report.get('error'):
                print(f"   ❌ Error: {health_report['error']}")

            return 0

        # Resend failed messages command
        if args.resend_failed:
            # This would need to be implemented in the queue system
            print("🔄 Resend failed messages feature not yet implemented")
            print("   This would reset FAILED messages back to PENDING status")
            return 0

        # Send message
        if args.queue_only:
            # Queue only
            message = Message(
                id=None,
                sender=args.sender,
                recipient=args.agent,
                content=args.message,
                priority=args.priority,
                category=args.category
            )

            queue = MessageQueue()
            msg_id = queue.enqueue(message)
            print(f"📋 Message queued for {args.agent} (ID: {msg_id})")
        else:
            # Send immediately
            if send_message(args.agent, args.message, args.sender):
                print(f"✅ Message sent to {args.agent}")
            else:
                print(f"❌ Failed to send message to {args.agent}")
                return 1

        return 0

    except Exception as e:
        logger.error(f"CLI error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())