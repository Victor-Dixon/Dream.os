#!/usr/bin/env python3
"""
Manually Trigger Status Monitor Resume Prompts
==============================================

Forces the status monitor to check all agents for inactivity and send resume prompts.
This bypasses the normal 5-minute check interval and 5-minute inactivity threshold.

Author: Agent-4 (Captain)
Date: 2025-12-03
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.agent_activity_detector import AgentActivityDetector
from src.core.optimized_stall_resume_prompt import generate_optimized_resume_prompt
from src.services.messaging_infrastructure import MessageCoordinator, UnifiedMessagePriority
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AGENTS = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
WORKSPACE_ROOT = Path(__file__).parent.parent


async def check_and_send_resume(agent_id: str, force: bool = False) -> bool:
    """Check agent inactivity and send resume prompt if needed."""
    try:
        activity_detector = AgentActivityDetector()
        
        # Check activity with shorter lookback for manual trigger
        summary = activity_detector.detect_agent_activity(
            agent_id, lookback_minutes=60)
        
        # For manual trigger, use 5 minutes threshold (same as normal)
        inactivity_threshold = 5.0
        
        should_send = False
        if force:
            # Force mode: send if any inactivity detected
            should_send = not summary.is_active or summary.inactivity_duration_minutes >= 5.0
        else:
            # Normal mode: only if inactive 5+ minutes
            should_send = not summary.is_active or summary.inactivity_duration_minutes >= inactivity_threshold
        
        if should_send:
            logger.info(f"🚨 {agent_id} is inactive ({summary.inactivity_duration_minutes:.1f} min) - sending resume prompt")
            
            # Load status for context
            status_file = WORKSPACE_ROOT / "agent_workspaces" / agent_id / "status.json"
            fsm_state = "active"
            last_mission = "Unknown"
            
            if status_file.exists():
                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        status = json.load(f)
                    fsm_state = status.get("status", "active")
                    last_mission = status.get("current_mission", "Unknown")
                except Exception as e:
                    logger.warning(f"Could not read status for {agent_id}: {e}")
            
            # Generate resume prompt
            resumer_prompt = generate_optimized_resume_prompt(
                agent_id=agent_id,
                fsm_state=fsm_state,
                last_mission=last_mission,
                stall_duration_minutes=summary.inactivity_duration_minutes
            )
            
            # Format resume message
            resume_message = f"🚨 RESUMER PROMPT - Inactivity Detected\n\n"
            resume_message += f"{resumer_prompt}\n\n"
            resume_message += f"**Inactivity Duration**: {summary.inactivity_duration_minutes:.1f} minutes\n"
            if summary.last_activity:
                resume_message += f"**Last Activity**: {summary.last_activity.strftime('%Y-%m-%d %H:%M:%S')}\n"
            if summary.activity_sources:
                resume_message += f"**Activity Sources**: {', '.join(summary.activity_sources)}\n"
            resume_message += f"\n**Action Required**: Review your status, update status.json, and resume operations.\n"
            resume_message += f"\n🐝 WE. ARE. SWARM. ⚡🔥"
            
            # Send via messaging system
            result = MessageCoordinator.send_to_agent(
                agent=agent_id,
                message=resume_message,
                priority=UnifiedMessagePriority.URGENT,
                use_pyautogui=True,
                stalled=True,
                sender="Captain Agent-4"
            )
            
            if result.get("success"):
                logger.info(f"✅ Resume message sent to {agent_id}")
                return True
            else:
                logger.error(f"❌ Failed to send to {agent_id}: {result.get('error', 'Unknown')}")
                return False
        else:
            logger.info(f"✅ {agent_id} is active (inactivity: {summary.inactivity_duration_minutes:.1f} min)")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error checking {agent_id}: {e}", exc_info=True)
        return False


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manually trigger status monitor resume prompts")
    parser.add_argument("--force", action="store_true", 
                       help="Force send to all agents regardless of inactivity (5 min threshold)")
    parser.add_argument("--agent", help="Check specific agent only")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🚨 MANUAL STATUS MONITOR RESUME TRIGGER")
    print("=" * 70)
    print()
    
    agents_to_check = [args.agent] if args.agent else AGENTS
    
    if args.force:
        print("⚠️  FORCE MODE: Sending resume prompts to all agents (5 min threshold)")
    else:
        print("📊 NORMAL MODE: Checking inactivity (5 min threshold)")
    print()
    
    results = {"sent": [], "skipped": [], "failed": []}
    
    for agent_id in agents_to_check:
        if agent_id not in AGENTS:
            logger.warning(f"⚠️  Unknown agent: {agent_id}")
            continue
            
        sent = await check_and_send_resume(agent_id, force=args.force)
        if sent:
            results["sent"].append(agent_id)
        else:
            results["skipped"].append(agent_id)
    
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Resume prompts sent: {len(results['sent'])}")
    print(f"⏭️  Skipped (active): {len(results['skipped'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    
    if results["sent"]:
        print()
        print("🚨 Agents sent resume prompts:")
        for agent_id in results["sent"]:
            print(f"   - {agent_id}")
    
    print()
    print("🐝 WE. ARE. SWARM. ⚡🔥")


if __name__ == "__main__":
    asyncio.run(main())

