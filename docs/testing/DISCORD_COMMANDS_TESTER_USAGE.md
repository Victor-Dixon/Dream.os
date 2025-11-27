# 🧪 Discord Commands Tester - Usage Guide

**From**: Agent-6 (Coordination & Communication Specialist)  
**Date**: 2025-01-27  
**Status**: ✅ **ENHANCED WITH DIRECT TESTING**

---

## 📊 EXISTING TOOL ENHANCED

**Location**: `tools/coordination/discord_commands_tester.py`  
**Status**: ✅ **ENHANCED** - Now supports direct Discord testing!

---

## 🎯 USAGE MODES

### **Mode 1: Static Analysis** (Default)

**Analyzes command files for error handling:**

```bash
python tools/coordination/discord_commands_tester.py
```

**What it does**:
- ✅ Finds all Discord command files
- ✅ Analyzes commands for error handling
- ✅ Generates coverage report
- ✅ Saves report to `data/discord_commands_test_report.json`

**Output**: Command analysis report showing:
- Total commands found
- Commands with error handling
- Coverage percentage
- Commands needing error handling

---

### **Mode 2: Direct Discord Testing** (NEW!)

**Tests commands directly in Discord using PyAutoGUI:**

```bash
python tools/coordination/discord_commands_tester.py --test-in-discord
```

**What it does**:
- ✅ Extracts all commands from files
- ✅ Types commands in Discord automatically
- ✅ Sends commands (presses Enter)
- ✅ Waits for bot responses
- ✅ Reports success/failure for each command

**Requirements**:
- ✅ Discord bot must be running
- ✅ Discord (web or desktop) must be open
- ✅ Test channel must be selected
- ✅ Message input box must be focused
- ✅ `pyautogui` installed (`pip install pyautogui`)

---

### **Mode 3: Test Specific Commands** (NEW!)

**Test only specific commands:**

```bash
python tools/coordination/discord_commands_tester.py --test-in-discord --commands "!help,!status,!control"
```

**What it does**:
- ✅ Tests only the specified commands
- ✅ Types and sends each command
- ✅ Reports results

**Example**:
```bash
# Test 3 specific commands
python tools/coordination/discord_commands_tester.py --test-in-discord --commands "!help,!status,!gui"

# Test all messaging commands
python tools/coordination/discord_commands_tester.py --test-in-discord --commands "!control,!gui,!status,!message,!broadcast,!help"
```

---

## 🚀 QUICK START

### **Step 1: Install PyAutoGUI** (if testing in Discord)
```bash
pip install pyautogui
```

### **Step 2: Start Discord Bot**
```bash
python src/discord_commander/unified_discord_bot.py
```

### **Step 3: Open Discord**
- Open Discord (web or desktop)
- Navigate to your test channel
- Focus the message input box

### **Step 4: Run Tests**

**Static Analysis** (no Discord needed):
```bash
python tools/coordination/discord_commands_tester.py
```

**Direct Discord Testing**:
```bash
python tools/coordination/discord_commands_tester.py --test-in-discord
```

**Test Specific Commands**:
```bash
python tools/coordination/discord_commands_tester.py --test-in-discord --commands "!help,!status"
```

---

## 📋 COMMAND LINE OPTIONS

```bash
python tools/coordination/discord_commands_tester.py [OPTIONS]

Options:
  -h, --help              Show help message
  --test-in-discord       Test commands directly in Discord (PyAutoGUI)
  --commands COMMANDS     Comma-separated list of commands to test
```

---

## ✅ TEST RESULTS

### **Static Analysis Output**:
- Command files analyzed
- Total commands found
- Error handling coverage
- Commands needing error handling
- Report saved to JSON

### **Direct Testing Output**:
- Commands tested
- Success/failure for each command
- Success rate percentage
- Results saved to JSON

---

## 🎯 EXAMPLE USAGE

### **Example 1: Analyze Commands**
```bash
$ python tools/coordination/discord_commands_tester.py

🔍 Analyzing Discord Command Files...
📁 Found 5 command file(s)
🔧 Total Commands: 24
✅ Commands with Error Handling: 15
📈 Coverage: 62.5%
```

### **Example 2: Test All Commands in Discord**
```bash
$ python tools/coordination/discord_commands_tester.py --test-in-discord

🤖 TESTING DISCORD COMMANDS DIRECTLY
⏳ Starting in 5 seconds...
🧪 Testing 17 commands in Discord...
[1/17] Testing: !help
   ✅ Sent: !help
[2/17] Testing: !status
   ✅ Sent: !status
...
✅ Passed: 17/17
📈 Success Rate: 100.0%
```

### **Example 3: Test Specific Commands**
```bash
$ python tools/coordination/discord_commands_tester.py --test-in-discord --commands "!help,!status,!control"

🧪 Testing 3 commands in Discord...
[1/3] Testing: !help
   ✅ Sent: !help
[2/3] Testing: !status
   ✅ Sent: !status
[3/3] Testing: !control
   ✅ Sent: !control
✅ Passed: 3/3
```

---

## 💡 TIPS

1. **For static analysis**: No Discord needed, runs fast
2. **For direct testing**: Make sure Discord is focused before running
3. **For specific commands**: Use `--commands` flag for quick testing
4. **Wait time**: Script waits 5 seconds before starting (time to focus Discord)
5. **Between commands**: 2 second wait for bot response, 1 second between commands

---

## 🐛 TROUBLESHOOTING

**Issue**: PyAutoGUI not found
- **Solution**: `pip install pyautogui`

**Issue**: Commands not sending
- **Solution**: Make sure Discord window is focused and message input is active

**Issue**: Bot not responding
- **Solution**: Check bot is running and online

**Issue**: Wrong channel
- **Solution**: Navigate to test channel before running script

---

**WE. ARE. SWARM. TESTING. AUTOMATED.** 🐝⚡🔥

**Agent-6**: Enhanced existing tester! Now supports direct Discord testing!

**Status**: ✅ **TOOL ENHANCED** | **DIRECT TESTING ADDED** | **READY TO USE**




