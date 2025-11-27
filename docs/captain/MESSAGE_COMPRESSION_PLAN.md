# 📦 Message Compression Plan

**For:** Victor  
**From:** Agent-4 (Captain)  
**Date:** 2025-01-27  
**Priority:** HIGH

---

## 🎯 GOAL

Compress message history data efficiently while preserving learning value and audit trail.

---

## 📊 COMPRESSION STRATEGY

### **1. Message Content Compression**

**Full Messages (Recent):**
- Keep full content for last 7 days
- Full sender, recipient, timestamp, queue_id

**Compressed Messages (7-30 days):**
- Keep: sender, recipient, timestamp, queue_id, message_type, priority
- Compress: content → first 200 chars + length
- Remove: full content, metadata details

**Archived Messages (30+ days):**
- Keep: sender, recipient, timestamp, message_type, priority
- Compress: content → hash + length only
- Aggregate: Group by sender/recipient pairs, count messages
- Remove: individual message content

### **2. Aggregation Strategy**

**Daily Aggregates:**
- Count messages per sender/recipient pair
- Track message types distribution
- Track priority distribution
- Store in `data/message_history_daily_YYYY-MM-DD.json`

**Weekly Aggregates:**
- Aggregate daily data
- Store in `data/message_history_weekly_YYYY-WW.json`

**Monthly Aggregates:**
- Aggregate weekly data
- Store in `data/message_history_monthly_YYYY-MM.json`

### **3. Compression Levels**

**Level 1: Recent (0-7 days)**
- Format: Full JSON with all fields
- Size: ~1-5 KB per message
- Retention: Full detail

**Level 2: Compressed (7-30 days)**
- Format: JSON with truncated content
- Size: ~500 bytes per message
- Retention: Metadata + preview

**Level 3: Aggregated (30+ days)**
- Format: Aggregated statistics
- Size: ~100 bytes per day
- Retention: Statistics only

---

## 🔧 IMPLEMENTATION

### **Compression Rules:**

```python
def compress_message(message: dict, age_days: int) -> dict:
    """Compress message based on age."""
    if age_days <= 7:
        # Level 1: Full detail
        return message
    
    elif age_days <= 30:
        # Level 2: Truncated content
        compressed = {
            "sender": message["sender"],
            "recipient": message["recipient"],
            "timestamp": message["timestamp"],
            "queue_id": message.get("queue_id"),
            "message_type": message.get("message_type"),
            "priority": message.get("priority"),
            "content_preview": message["content"][:200],
            "content_length": len(message["content"]),
        }
        return compressed
    
    else:
        # Level 3: Statistics only
        return None  # Will be aggregated
```

### **Aggregation Rules:**

```python
def aggregate_messages(messages: list) -> dict:
    """Aggregate messages into statistics."""
    stats = {
        "date": messages[0]["timestamp"][:10],
        "total_messages": len(messages),
        "by_sender": {},
        "by_recipient": {},
        "by_type": {},
        "by_priority": {},
    }
    
    for msg in messages:
        # Count by sender
        sender = msg["sender"]
        stats["by_sender"][sender] = stats["by_sender"].get(sender, 0) + 1
        
        # Count by recipient
        recipient = msg["recipient"]
        stats["by_recipient"][recipient] = stats["by_recipient"].get(recipient, 0) + 1
        
        # Count by type
        msg_type = msg.get("message_type", "unknown")
        stats["by_type"][msg_type] = stats["by_type"].get(msg_type, 0) + 1
        
        # Count by priority
        priority = msg.get("priority", "regular")
        stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
    
    return stats
```

---

## 📈 STORAGE ESTIMATES

**Assumptions:**
- 100 messages/day average
- 12 concurrent users
- Average message: 500 chars

**Storage per Day:**
- Level 1 (7 days): 100 × 5 KB × 7 = 3.5 MB
- Level 2 (23 days): 100 × 0.5 KB × 23 = 1.15 MB
- Level 3 (aggregated): 100 bytes/day

**Total per Month:**
- Full detail: ~3.5 MB
- Compressed: ~1.15 MB
- Aggregated: ~3 KB
- **Total: ~4.65 MB/month**

**Compression Ratio:**
- Without compression: 100 × 5 KB × 30 = 15 MB/month
- With compression: 4.65 MB/month
- **Savings: 69% reduction**

---

## 🔄 COMPRESSION SCHEDULE

**Daily:**
- Compress messages older than 7 days
- Create daily aggregates for messages older than 30 days

**Weekly:**
- Aggregate daily statistics
- Archive full messages older than 30 days

**Monthly:**
- Aggregate weekly statistics
- Final compression pass

---

## 📚 LEARNING VALUE PRESERVATION

**What We Keep:**
- ✅ Sender/recipient patterns
- ✅ Message type distribution
- ✅ Priority distribution
- ✅ Timing patterns
- ✅ Queue performance metrics

**What We Compress:**
- ⚠️ Full message content (after 7 days)
- ⚠️ Metadata details (after 30 days)

**What We Aggregate:**
- 📊 Daily/weekly/monthly statistics
- 📊 Communication patterns
- 📊 System usage metrics

---

## 🎯 COMPRESSION GOALS

1. **Reduce Storage:** 70%+ reduction in message history size
2. **Preserve Learning:** Keep patterns and statistics
3. **Maintain Audit Trail:** Keep sender/recipient/timestamp
4. **Enable Analysis:** Aggregated data for insights

---

**WE. ARE. SWARM. COMPRESSING. LEARNING. 🐝⚡🔥**




