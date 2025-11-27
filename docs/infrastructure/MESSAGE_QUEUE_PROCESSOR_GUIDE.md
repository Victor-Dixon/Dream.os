# Message Queue Processor Guide

**Author**: Agent-3 (Infrastructure & DevOps)  
**Date**: 2025-01-27  
**Status**: ✅ Critical for Message Delivery

---

## 🚨 **CRITICAL ISSUE**

**Problem**: Discord messages show as "sent" but don't actually get delivered.

**Root Cause**: Messages are queued successfully, but the queue processor isn't running to deliver them.

**Solution**: Start the message queue processor as a background service.

---

## 🔧 **HOW IT WORKS**

### **Message Flow**:
1. **Discord Bot** → Queues message → Returns "sent" ✅
2. **Queue Processor** → Processes queue → Delivers via PyAutoGUI → Message arrives ✅

**Without Queue Processor**: Messages sit in queue, never delivered ❌

---

## 🚀 **STARTING THE QUEUE PROCESSOR**

### **Option 1: Unified Startup (RECOMMENDED - Starts Both Bot & Processor)**
```bash
python tools/start_discord_system.py
```
**This starts both Discord bot and queue processor together!**

### **Option 2: Queue Processor Only (If Bot Already Running)**
```bash
python tools/start_message_queue_processor.py
```

### **Option 2: Direct Module Execution**
```bash
python -m src.core.message_queue_processor
```

### **Option 3: Process Limited Messages**
```bash
python -m src.core.message_queue_processor 10  # Process 10 messages then exit
```

---

## 📋 **REQUIREMENTS**

The queue processor must be running for messages to be delivered. It:
- Processes messages from the queue sequentially
- Uses global keyboard lock to prevent race conditions
- Delivers messages via PyAutoGUI
- Tracks message delivery status

---

## 🔍 **VERIFICATION**

### **Check if Processor is Running**:
```powershell
Get-Process python | Where-Object {$_.CommandLine -like "*queue_processor*"}
```

### **Check Queue Status**:
```bash
# View queue contents
cat message_queue/queue.json
```

### **Expected Output**:
```
🔄 Message queue processor started
✅ Message delivered: queue_123 (DISCORD → Agent-1)
```

---

## ⚠️ **IMPORTANT NOTES**

1. **Must Run Continuously**: The processor must run as a background service
2. **One Instance Only**: Only one processor should run at a time
3. **Keyboard Control**: Processor uses global lock to prevent conflicts
4. **Sequential Delivery**: Messages are delivered one at a time

---

## 🛑 **STOPPING THE PROCESSOR**

Press `Ctrl+C` in the terminal where it's running, or:
```powershell
Get-Process python | Where-Object {$_.CommandLine -like "*queue_processor*"} | Stop-Process
```

---

## 📊 **TROUBLESHOOTING**

### **Issue: Messages Still Not Delivering**
1. Verify processor is running
2. Check queue for pending messages
3. Verify PyAutoGUI is working
4. Check agent coordinates are correct

### **Issue: Processor Crashes**
1. Check logs for errors
2. Verify all dependencies installed
3. Check message queue file permissions

---

## ✅ **STATUS**

**Queue Processor**: ✅ Available  
**Startup Tool**: ✅ Created  
**Documentation**: ✅ Complete

---

**WE. ARE. SWARM. PROCESSING. DELIVERING. 🐝⚡🔥**




