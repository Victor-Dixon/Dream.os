#!/usr/bin/env python3
"""
GitHub Queue Processor - Automatic Retry System
================================================

Processes queued GitHub operations when rate limits reset.
Automatically retries PR creation, merging, and other operations.

Features:
- Monitors rate limits and processes queue when available
- Automatic retry with exponential backoff
- Processes PR operations from deferred queue
- Continues processing until queue empty or rate-limited

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-10
Priority: HIGH
"""

import sys
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from tools.enhanced_unified_github import EnhancedUnifiedGitHub, OperationType
    from src.core.deferred_push_queue import get_deferred_push_queue, PushStatus
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)


class GitHubQueueProcessor:
    """Processes queued GitHub operations."""
    
    def __init__(self):
        """Initialize queue processor."""
        self.github = EnhancedUnifiedGitHub()
        self.queue = get_deferred_push_queue()
        logger.info("✅ GitHub Queue Processor initialized")
    
    def process_queue(self, max_items: int = 10, wait_for_reset: bool = False) -> Dict[str, int]:
        """
        Process queued operations.
        
        Args:
            max_items: Maximum items to process per cycle
            wait_for_reset: Wait for rate limit reset if exhausted
        
        Returns:
            Statistics dictionary
        """
        stats = {
            "processed": 0,
            "succeeded": 0,
            "failed": 0,
            "deferred": 0,
            "queued": 0
        }
        
        pending_count = self.queue.get_pending_count()
        if pending_count == 0:
            logger.info("📭 Queue is empty")
            return stats
        
        logger.info(f"📥 Processing queue: {pending_count} pending items")
        
        # Check rate limits
        limits = self.github.check_rate_limits()
        rest_limit = limits.get("rest")
        graphql_limit = limits.get("graphql")
        
        # Check if we can proceed
        can_proceed = (
            (rest_limit and rest_limit.available and rest_limit.remaining > 10) or
            (graphql_limit and graphql_limit.available and graphql_limit.remaining > 10)
        )
        
        if not can_proceed:
            if wait_for_reset:
                # Wait for rate limit reset
                reset_time = min(
                    rest_limit.reset_time if rest_limit else float('inf'),
                    graphql_limit.reset_time if graphql_limit else float('inf')
                )
                wait_seconds = max(0, int(reset_time - time.time()))
                if wait_seconds > 0:
                    logger.info(f"⏳ Rate limits exhausted. Waiting {wait_seconds}s for reset...")
                    time.sleep(min(wait_seconds, 3600))  # Max 1 hour wait
            else:
                logger.warning("⚠️ Rate limits exhausted. Queue processing deferred.")
                return stats
        
        # Process up to max_items
        for _ in range(min(max_items, pending_count)):
            entry = self.queue.dequeue_push()
            if not entry:
                break
            
            entry_id = entry.get("id")
            metadata = entry.get("metadata", {})
            action = metadata.get("action", "push")
            
            logger.info(f"🔄 Processing: {entry.get('repo')}/{entry.get('branch')} (ID: {entry_id}, action: {action})")
            
            # Mark as retrying
            self.queue.mark_retrying(entry_id)
            stats["processed"] += 1
            
            # Process based on action type
            try:
                if action == "create_pr":
                    success = self._process_create_pr(entry)
                elif action == "merge_pr":
                    success = self._process_merge_pr(entry)
                else:
                    logger.warning(f"⚠️ Unknown action: {action}, skipping")
                    success = False
                
                if success:
                    stats["succeeded"] += 1
                    self.queue.mark_completed(entry_id)
                    logger.info(f"✅ Completed: {entry.get('repo')}/{entry.get('branch')}")
                else:
                    # Check if rate-limited again
                    limits_after = self.github.check_rate_limits()
                    rest_after = limits_after.get("rest")
                    graphql_after = limits_after.get("graphql")
                    
                    still_rate_limited = (
                        (not rest_after or not rest_after.available) and
                        (not graphql_after or not graphql_after.available)
                    )
                    
                    if still_rate_limited:
                        stats["deferred"] += 1
                        logger.info(f"⏳ Rate-limited again, deferring: {entry.get('repo')}/{entry.get('branch')}")
                    else:
                        # Other error - mark failed if retries exceeded
                        retry_count = entry.get("retry_count", 0)
                        if retry_count >= 5:
                            stats["failed"] += 1
                            self.queue.mark_failed(entry_id, "Max retries exceeded", max_retries=5)
                            logger.warning(f"❌ Failed permanently: {entry.get('repo')}/{entry.get('branch')}")
                        else:
                            stats["deferred"] += 1
                            logger.info(f"⏳ Deferred for retry: {entry.get('repo')}/{entry.get('branch')}")
            
            except Exception as e:
                logger.error(f"❌ Error processing {entry_id}: {e}")
                stats["failed"] += 1
                retry_count = entry.get("retry_count", 0)
                if retry_count >= 5:
                    self.queue.mark_failed(entry_id, str(e), max_retries=5)
                else:
                    stats["deferred"] += 1
        
        return stats
    
    def _process_create_pr(self, entry: Dict[str, Any]) -> bool:
        """Process create PR operation."""
        metadata = entry.get("metadata", {})
        params = metadata.get("params", {})
        
        repo = params.get("repo")
        title = params.get("title")
        body = params.get("body")
        head = params.get("head")
        base = params.get("base", "main")
        
        if not all([repo, title, body, head]):
            logger.error(f"❌ Missing required parameters for PR creation")
            return False
        
        result = self.github.create_pr(repo, title, body, head, base, queue_on_failure=False)
        
        if result.get("success"):
            logger.info(f"✅ PR created: {result.get('pr_url')}")
            return True
        else:
            logger.warning(f"⚠️ PR creation failed: {result.get('error')}")
            return False
    
    def _process_merge_pr(self, entry: Dict[str, Any]) -> bool:
        """Process merge PR operation."""
        metadata = entry.get("metadata", {})
        params = metadata.get("params", {})
        
        repo = params.get("repo")
        pr_number = params.get("pr_number")
        merge_method = params.get("merge_method", "merge")
        
        if not repo or not pr_number:
            logger.error(f"❌ Missing required parameters for PR merge")
            return False
        
        result = self.github.merge_pr(repo, pr_number, merge_method, queue_on_failure=False)
        
        if result.get("success"):
            logger.info(f"✅ PR merged: {result.get('sha')}")
            return True
        else:
            logger.warning(f"⚠️ PR merge failed: {result.get('error')}")
            return False
    
    def run_continuous(self, check_interval: int = 300, max_cycles: Optional[int] = None):
        """
        Run continuous queue processing.
        
        Args:
            check_interval: Seconds between queue checks
            max_cycles: Maximum cycles to run (None = infinite)
        """
        logger.info(f"🔄 Starting continuous queue processing (check every {check_interval}s)")
        cycle = 0
        
        try:
            while max_cycles is None or cycle < max_cycles:
                cycle += 1
                logger.info(f"\n📊 Cycle {cycle}: Processing queue...")
                
                stats = self.process_queue(max_items=10, wait_for_reset=True)
                
                logger.info(f"📊 Cycle {cycle} results:")
                logger.info(f"   Processed: {stats['processed']}")
                logger.info(f"   Succeeded: {stats['succeeded']}")
                logger.info(f"   Failed: {stats['failed']}")
                logger.info(f"   Deferred: {stats['deferred']}")
                
                # Check if queue is empty
                pending_count = self.queue.get_pending_count()
                if pending_count == 0:
                    logger.info("✅ Queue empty - processing complete!")
                    break
                
                # Wait before next check
                if cycle < (max_cycles or float('inf')):
                    logger.info(f"⏳ Waiting {check_interval}s before next check...")
                    time.sleep(check_interval)
        
        except KeyboardInterrupt:
            logger.info("\n⚠️ Processing interrupted by user")
        except Exception as e:
            logger.error(f"❌ Error in continuous processing: {e}")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process GitHub operations queue")
    parser.add_argument(
        "--max-items",
        type=int,
        default=10,
        help="Maximum items to process per cycle (default: 10)"
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run continuous processing (checks queue periodically)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Check interval in seconds for continuous mode (default: 300)"
    )
    parser.add_argument(
        "--max-cycles",
        type=int,
        default=None,
        help="Maximum cycles for continuous mode (default: unlimited)"
    )
    parser.add_argument(
        "--wait-for-reset",
        action="store_true",
        help="Wait for rate limit reset if exhausted"
    )
    
    args = parser.parse_args()
    
    processor = GitHubQueueProcessor()
    
    if args.continuous:
        processor.run_continuous(
            check_interval=args.interval,
            max_cycles=args.max_cycles
        )
    else:
        stats = processor.process_queue(
            max_items=args.max_items,
            wait_for_reset=args.wait_for_reset
        )
        
        print("\n" + "="*60)
        print("📊 QUEUE PROCESSING RESULTS")
        print("="*60)
        print(f"Processed: {stats['processed']}")
        print(f"Succeeded: {stats['succeeded']}")
        print(f"Failed: {stats['failed']}")
        print(f"Deferred: {stats['deferred']}")
        
        # Show queue stats
        queue_stats = processor.queue.get_stats()
        print(f"\nQueue Status:")
        print(f"  Pending: {queue_stats['pending']}")
        print(f"  Retrying: {queue_stats['retrying']}")
        print(f"  Failed: {queue_stats['failed']}")
        print(f"  Completed: {queue_stats['completed']}")


if __name__ == "__main__":
    main()


