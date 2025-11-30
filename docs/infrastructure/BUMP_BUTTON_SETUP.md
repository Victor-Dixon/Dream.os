# Bump Button Setup & Verification

**Date**: 2025-11-30  
**Author**: Agent-6

---

## ✅ **CODE VERIFICATION**

The bump button code is **correctly implemented**:

- ✅ Button defined: `self.bump_btn` in `MainControlPanelView`
- ✅ Label: "Bump Agents"
- ✅ Custom ID: "control_bump"
- ✅ Row: 2 (with Restart Bot, Shutdown Bot, Unstall Agent)
- ✅ Callback: `show_bump_selector` method
- ✅ View: `BumpAgentView` created and integrated

---

## 🔍 **WHY YOU DON'T SEE THE BUTTON**

Discord buttons are **tied to the message** they were sent with. You cannot edit a message to add new buttons. The button will only appear when:

1. **Discord bot is restarted** (to load new code)
2. **Control panel message is RE-SENT** (new message with new buttons)

---

## 🚀 **HOW TO SEE THE BUTTON**

### **Option 1: Use !control Command**
```
!control
```
or
```
!panel
```
or
```
!menu
```

This will send a **NEW** control panel message with all buttons, including the new "Bump Agents" button.

### **Option 2: Restart Bot**
1. Restart the Discord bot (to load new code)
2. Bot will automatically send startup message with new control panel
3. The new control panel will have the "Bump Agents" button

### **Option 3: Use !help Command**
```
!help
```
Then click the control panel button in the help message.

---

## 📍 **BUTTON LOCATION**

The "Bump Agents" button is in:
- **Control Panel** → **Row 2**
- **Position**: 4th button in Row 2
- **Buttons in Row 2**:
  1. Restart Bot (🔄)
  2. Shutdown Bot (🛑)
  3. Unstall Agent (🚨)
  4. **Bump Agents (👆)** ← NEW!

---

## ✅ **VERIFICATION STEPS**

1. **Restart Discord bot** (if not already restarted)
2. **Type `!control` in Discord** to get new control panel
3. **Look for "Bump Agents" button** in Row 2
4. **Click button** to open agent selector

---

## 🧪 **TESTING**

Run verification script:
```bash
python tools/verify_bump_button.py
```

This will verify:
- Button code is present
- Button is properly configured
- Row 2 button count (Discord limit: 5 per row)

---

## 📝 **NOTE**

If you still don't see the button after restarting and using `!control`:
1. Check bot logs for errors
2. Verify bot is running latest code
3. Check Discord permissions (bot needs to send messages with components)

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Agent-6 - Coordination & Communication Specialist*

