# 🧪 DISCORD COMMANDS TEST GUIDE

**Agent**: Agent-5  
**Date**: 2025-01-27  
**Purpose**: Comprehensive testing guide for all Discord bot commands

---

## 📋 **ALL DISCORD COMMANDS**

### **1. Text Commands (Slash/Prefix Commands)**

#### **`!message <agent> <message>`**
- **Purpose**: Send message to specific agent
- **Usage**: `!message Agent-1 Hello from Discord`
- **Test Steps**:
  1. Type: `!message Agent-1 Test message`
  2. Should see: "✅ Message Sent - Delivered to Agent-1"
  3. Check Agent-1's chat input in Cursor IDE - message should appear
  4. Check queue: Message should be queued and processed

#### **`!broadcast <message>`**
- **Purpose**: Broadcast message to all 8 agents
- **Usage**: `!broadcast System update message`
- **Test Steps**:
  1. Type: `!broadcast Test broadcast message`
  2. Should see: "✅ Broadcast Sent - Delivered to all agents"
  3. Check all 8 agents' chat inputs - message should appear sequentially
  4. Check queue: 8 messages should be queued

#### **`!gui`**
- **Purpose**: Open interactive GUI control panel
- **Usage**: `!gui`
- **Test Steps**:
  1. Type: `!gui`
  2. Should see: Interactive control panel with buttons
  3. Test each button:
     - Agent selection dropdown
     - Broadcast button
     - Status button
     - Refresh button

#### **`!status`**
- **Purpose**: Show swarm status
- **Usage**: `!status`
- **Test Steps**:
  1. Type: `!status`
  2. Should see: Embed showing all 8 agents' status
  3. Verify status data is accurate

#### **`!help`**
- **Purpose**: Show help menu
- **Usage**: `!help`
- **Test Steps**:
  1. Type: `!help`
  2. Should see: Interactive help menu
  3. Test navigation buttons

#### **`!shutdown`** (Admin only)
- **Purpose**: Gracefully shutdown bot
- **Usage**: `!shutdown`
- **Test Steps**:
  1. Type: `!shutdown`
  2. Should see: Confirmation dialog
  3. Click "Confirm" → Bot should shutdown
  4. Click "Cancel" → Bot should stay online

#### **`!restart`** (Admin only)
- **Purpose**: Restart bot
- **Usage**: `!restart`
- **Test Steps**:
  1. Type: `!restart`
  2. Should see: Confirmation dialog
  3. Click "Confirm" → Bot should restart
  4. Click "Cancel" → Bot should stay online

---

### **2. GUI Modals (Interactive Forms)**

#### **Agent Message Modal**
- **Access**: Click agent in GUI dropdown → Modal opens
- **Fields**:
  - Message text (required, max 2000 chars)
  - Priority: regular/urgent (optional, default: regular)
- **Test Steps**:
  1. Open GUI (`!gui`)
  2. Select agent from dropdown
  3. Fill message and priority
  4. Submit
  5. Should see: "✅ Message queued for Agent-X!" with queue ID
  6. Check agent's chat input - message should appear

#### **Broadcast Modal**
- **Access**: Click "Broadcast to All" button in GUI
- **Fields**:
  - Message text (required, max 2000 chars)
  - Priority: regular/urgent (optional, default: regular)
- **Test Steps**:
  1. Open GUI (`!gui`)
  2. Click "Broadcast to All"
  3. Fill message and priority
  4. Submit
  5. Should see: "✅ Broadcast sent to all 8 agents!"
  6. Check all agents' chat inputs - message should appear

#### **Jet Fuel Message Modal**
- **Access**: Available in advanced GUI views
- **Fields**:
  - Agent ID (required)
  - Jet Fuel message (required, max 2000 chars)
- **Test Steps**:
  1. Open advanced GUI
  2. Click "Jet Fuel" button
  3. Enter agent ID and message
  4. Submit
  5. Should see: "✅ Jet Fuel message queued for Agent-X!"
  6. Check agent's chat input - message with "🚀 JET FUEL" header should appear

#### **Jet Fuel Broadcast Modal**
- **Access**: Available in advanced GUI views
- **Fields**:
  - Jet Fuel message (required, max 2000 chars)
- **Test Steps**:
  1. Open advanced GUI
  2. Click "Jet Fuel Broadcast" button
  3. Enter message
  4. Submit
  5. Should see: "✅ Jet Fuel broadcast sent to all 8 agents!"
  6. Check all agents' chat inputs - Jet Fuel messages should appear

#### **Selective Broadcast Modal**
- **Access**: Available in advanced GUI views
- **Fields**:
  - Agent IDs (comma-separated, required)
  - Message text (required, max 2000 chars)
  - Priority: regular/urgent (optional)
- **Test Steps**:
  1. Open advanced GUI
  2. Click "Selective Broadcast" button
  3. Enter: "Agent-1, Agent-2, Agent-3"
  4. Enter message and priority
  5. Submit
  6. Should see: "✅ Broadcast sent to 3 agent(s)!"
  7. Check those 3 agents' chat inputs - message should appear

---

### **3. Direct Message Format**

#### **`[C2A] Agent-X\n\nMessage content`**
- **Purpose**: Direct message format (Captain-to-Agent)
- **Usage**: 
```
[C2A] Agent-1

This is a direct message
```
- **Test Steps**:
  1. Type message in Discord channel
  2. Should automatically queue message
  3. Check agent's chat input - message should appear

#### **`[D2A] Agent-X\n\nMessage content`**
- **Purpose**: Direct message format (Discord-to-Agent, urgent)
- **Usage**:
```
[D2A] Agent-1

This is an urgent direct message
```
- **Test Steps**:
  1. Type message in Discord channel
  2. Should automatically queue as urgent
  3. Check agent's chat input - urgent message should appear

---

## ✅ **TESTING CHECKLIST**

### **Prerequisites**:
- [ ] Discord bot is online and running
- [ ] Queue processor is running
- [ ] All 8 agent windows are open in Cursor IDE
- [ ] Coordinates are valid for all agents

### **Text Commands**:
- [ ] `!message` works
- [ ] `!broadcast` works
- [ ] `!gui` opens GUI panel
- [ ] `!status` shows agent status
- [ ] `!help` shows help menu
- [ ] `!shutdown` (admin) works with confirmation
- [ ] `!restart` (admin) works with confirmation

### **GUI Modals**:
- [ ] Agent Message Modal works
- [ ] Broadcast Modal works
- [ ] Jet Fuel Message Modal works
- [ ] Jet Fuel Broadcast Modal works
- [ ] Selective Broadcast Modal works

### **Direct Message Format**:
- [ ] `[C2A]` format works
- [ ] `[D2A]` format works (urgent)

### **Delivery Verification**:
- [ ] Messages appear in agent chat inputs
- [ ] Messages are queued correctly
- [ ] Queue processor processes messages
- [ ] Messages show correct tags ([C2A], [D2A], etc.)
- [ ] Urgent messages have urgent prefix
- [ ] Jet Fuel messages have Jet Fuel header

---

## 🔧 **FIXES APPLIED**

### **1. All Modals Now Use Non-Blocking Queue**
- ✅ Changed `wait_for_delivery=True` → `wait_for_delivery=False`
- ✅ Prevents Discord 3-second timeout issues
- ✅ Queue processor handles delivery asynchronously

### **2. Improved Error Messages**
- ✅ Shows queue ID for tracking
- ✅ Explains async delivery process
- ✅ Provides troubleshooting guidance

### **3. Better Logging**
- ✅ Added logging for all queue operations
- ✅ Error logging with full context

---

## 📊 **EXPECTED BEHAVIOR**

### **Message Flow**:
```
User Command → Discord Bot → ConsolidatedMessagingService 
→ MessageQueue.enqueue() ✅ (instant)
→ Returns queue_id to Discord ✅ (instant)
→ MessageQueueProcessor.process_queue() 
→ PyAutoGUIMessagingDelivery.send_message() 
→ Agent chat input ✅ (within seconds)
```

### **Response Times**:
- Discord response: < 3 seconds ✅
- Message queuing: < 1 second ✅
- Message delivery: 5-30 seconds (depends on queue)
- Queue processor: Continuous background processing

---

## 🐛 **KNOWN ISSUES**

### **1. Delivery Failures**
- **Issue**: Some messages show "FAILED" status
- **Cause**: PyAutoGUI delivery errors (coordinates, window focus)
- **Workaround**: Check queue processor logs, verify coordinates

### **2. Queue Processing**
- **Issue**: Messages stuck in PROCESSING
- **Fix Applied**: Fixed indentation bug in queue processor
- **Status**: Should be resolved

---

## ✅ **TEST RESULTS**

Run through all commands and check boxes above as you test.

**Last Updated**: 2025-01-27  
**Tested By**: Agent-5


