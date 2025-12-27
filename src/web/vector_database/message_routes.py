"""
Message History API Routes - V2 Compliant
==========================================

API endpoints for message history dashboard.
Provides message history, statistics, and filtering.

<!-- SSOT Domain: web -->

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

from flask import Blueprint, jsonify, request
from typing import Optional

message_bp = Blueprint('messages', __name__, url_prefix='/api/messages')


@message_bp.route('/history', methods=['GET'])
def get_message_history():
    """Get message history with optional filtering."""
    try:
        from src.repositories.message_repository import MessageRepository
        
        repo = MessageRepository()
        
        # Get query parameters
        agent_id = request.args.get('agent_id', None)
        limit = request.args.get('limit', 100, type=int)
        sender = request.args.get('sender', None)
        recipient = request.args.get('recipient', None)
        
        # Get messages
        if agent_id:
            messages = repo.get_message_history(agent_id=agent_id, limit=limit)
        elif sender:
            messages = repo.get_messages_by_sender(sender)
            if limit:
                messages = messages[:limit]
        elif recipient:
            messages = repo.get_messages_by_recipient(recipient)
            if limit:
                messages = messages[:limit]
        else:
            messages = repo.get_recent_messages(limit=limit)
        
        return jsonify({
            "success": True,
            "messages": messages,
            "count": len(messages)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "messages": []
        }), 500


@message_bp.route('/stats', methods=['GET'])
def get_message_stats():
    """Get message statistics."""
    try:
        from src.repositories.message_repository import MessageRepository
        
        repo = MessageRepository()
        
        # Get all messages for stats
        all_messages = repo.get_message_history(limit=None)
        
        # Calculate statistics
        total = len(all_messages)
        
        # Count by type
        by_type = {}
        by_priority = {}
        by_agent = {}
        today_count = 0
        
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        for msg in all_messages:
            # By type
            msg_type = msg.get('message_type', 'unknown')
            by_type[msg_type] = by_type.get(msg_type, 0) + 1
            
            # By priority
            priority = msg.get('priority', 'regular')
            by_priority[priority] = by_priority.get(priority, 0) + 1
            
            # By agent (sender)
            sender = msg.get('from', 'UNKNOWN')
            by_agent[sender] = by_agent.get(sender, 0) + 1
            
            # Today count
            try:
                timestamp = msg.get('timestamp', '')
                if timestamp:
                    msg_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).date()
                    if msg_date == today:
                        today_count += 1
            except (ValueError, AttributeError):
                pass
        
        return jsonify({
            "success": True,
            "stats": {
                "total": total,
                "today": today_count,
                "by_type": by_type,
                "by_priority": by_priority,
                "by_agent": by_agent,
                "active_agents": len(by_agent)
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "stats": {}
        }), 500


@message_bp.route('/activity', methods=['GET'])
def get_agent_activity():
    """Get agent activity tracking data."""
    try:
        from src.core.agent_activity_tracker import get_activity_tracker
        
        tracker = get_activity_tracker()
        
        # FIX: Use get_all_agent_activity which exists, not get_recent_activity which doesn't
        all_activity = tracker.get_all_agent_activity()
        
        # Transform to expected format
        activity = []
        for agent_id, agent_data in all_activity.items():
            activity.append({
                "agent_id": agent_id,
                "status": agent_data.get("status", "inactive"),
                "timestamp": agent_data.get("last_active"),
                "last_activity": agent_data.get("last_active"),
                "action_count": agent_data.get("activity_count", 0),
                "operation": agent_data.get("operation", "unknown")
            })
        
        return jsonify({
            "success": True,
            "activity": activity
        })
    except ImportError:
        return jsonify({
            "success": False,
            "error": "Agent activity tracker not available",
            "activity": []
        }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "activity": []
        }), 500


@message_bp.route('/queue', methods=['GET'])
def get_queue_status():
    """Get message queue status."""
    try:
        from src.core.message_queue import MessageQueue
        
        queue = MessageQueue()
        stats = queue.get_statistics()
        
        return jsonify({
            "success": True,
            "queue": {
                "pending": stats.get('pending_count', 0),
                "delivered": stats.get('delivered_count', 0),
                "failed": stats.get('failed_count', 0),
                "total": stats.get('total_count', 0)
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "queue": {}
        }), 500




