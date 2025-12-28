# MCP Servers Debugging Guide

**Date**: 2025-12-27  
**Agent**: Agent-3 (Infrastructure & DevOps Specialist)  
**Status**: Debugging Guide

---

## 🔍 Current Status

### **Server Files Status:**
- ✅ All 6 MCP server files exist
- ✅ All server files have valid Python syntax
- ✅ All server files can be imported successfully
- ✅ Configuration file exists: `mcp_servers/all_mcp_servers.json`

### **Connectivity Status:**
- ⚠️ MCP client configuration found: `C:\Users\USER\.cursor\mcp.json`
- ❌ MCP resources not accessible via `list_mcp_resources`
- ⚠️ Servers timeout when tested directly (expected - they use stdio transport)

---

## 🐛 Common Issues & Solutions

### **Issue 1: MCP Servers Not Showing Up in Cursor**

**Symptoms:**
- `list_mcp_resources()` returns empty
- MCP tools not available in Cursor

**Possible Causes:**
1. MCP servers not configured in Cursor settings
2. MCP servers not running/connected
3. Configuration file path incorrect
4. Python path issues

**Solutions:**

1. **Check Cursor MCP Configuration:**
   - Open Cursor Settings
   - Navigate to MCP Servers section
   - Verify servers are configured from `mcp_servers/all_mcp_servers.json`

2. **Verify Configuration Format:**
   ```json
   {
     "mcpServers": {
       "task-manager": {
         "command": "python",
         "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/task_manager_server.py"]
       }
     }
   }
   ```

3. **Check Python Path:**
   - Ensure `python` command is available in PATH
   - Or use full path: `"command": "C:/Python/python.exe"`

4. **Restart Cursor:**
   - MCP servers need Cursor restart to connect
   - Close and reopen Cursor after configuration changes

---

### **Issue 2: MCP Servers Timeout**

**Symptoms:**
- Servers timeout when tested directly
- `--help` flag doesn't work

**Explanation:**
- This is **NORMAL** - MCP servers use stdio transport
- They communicate via stdin/stdout, not command-line flags
- They're designed to run as background processes by the MCP client

**Solution:**
- Don't test servers directly with `--help`
- Test via MCP client (Cursor) instead
- Use `list_mcp_resources()` to verify connectivity

---

### **Issue 3: Import Errors**

**Symptoms:**
- Server files fail to import
- ModuleNotFoundError or ImportError

**Solutions:**

1. **Check Dependencies:**
   ```bash
   pip install mcp
   ```

2. **Verify Project Structure:**
   - Ensure `mcp_servers/` directory exists
   - Ensure `__init__.py` exists in `mcp_servers/`

3. **Check Python Path:**
   - Servers add project root to path automatically
   - Verify project structure is correct

---

### **Issue 4: Configuration File Not Found**

**Symptoms:**
- `mcp_servers/all_mcp_servers.json` not found
- Configuration errors

**Solutions:**

1. **Verify File Exists:**
   ```bash
   ls mcp_servers/all_mcp_servers.json
   ```

2. **Check JSON Validity:**
   ```bash
   python -m json.tool mcp_servers/all_mcp_servers.json
   ```

3. **Recreate Configuration:**
   - Use `mcp_servers/all_mcp_servers.json` as template
   - Update paths for your system

---

## 🛠️ Debugging Tools

### **Tool 1: Basic Server Check**
```bash
python tools/debug_mcp_servers.py
```

**Checks:**
- Server file existence
- Python syntax validity
- Module importability

---

### **Tool 2: Connectivity Test**
```bash
python tools/test_mcp_server_connectivity.py
```

**Checks:**
- MCP client configuration
- Server startup capability
- Configuration file locations

---

### **Tool 3: Manual Server Test**

Test a server function directly:

```python
import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import server module
from mcp_servers import task_manager_server as tm

# Test a function
result = tm.get_tasks("INBOX")
print(json.dumps(result, indent=2))
```

---

## 📋 Debugging Checklist

- [ ] **Server Files Exist**
  - [ ] All 6 server files present in `mcp_servers/`
  - [ ] `__init__.py` exists
  - [ ] Configuration file exists

- [ ] **Server Files Valid**
  - [ ] Python syntax valid (run `python -m py_compile`)
  - [ ] Modules can be imported
  - [ ] No import errors

- [ ] **MCP Client Configuration**
  - [ ] Cursor MCP settings configured
  - [ ] Configuration file path correct
  - [ ] Python command path correct
  - [ ] Server paths use forward slashes or escaped backslashes

- [ ] **MCP Client Connection**
  - [ ] Cursor restarted after configuration
  - [ ] MCP servers show as connected in Cursor
  - [ ] `list_mcp_resources()` returns resources

- [ ] **Dependencies**
  - [ ] `mcp` package installed
  - [ ] All server dependencies installed
  - [ ] Python version compatible

---

## 🔧 Quick Fixes

### **Fix 1: Reconfigure MCP Servers**

1. Copy configuration from `mcp_servers/all_mcp_servers.json`
2. Paste into Cursor MCP settings
3. Update paths if needed
4. Restart Cursor

### **Fix 2: Verify Python Path**

```bash
# Check Python version
python --version

# Check if python is in PATH
where python  # Windows
which python  # Linux/Mac
```

### **Fix 3: Test Server Import**

```python
# Test individual server
python -c "from mcp_servers import task_manager_server; print('OK')"
```

### **Fix 4: Check MCP Package**

```bash
pip install mcp
python -c "import mcp; print(mcp.__version__)"
```

---

## 📊 Current Diagnostic Results

**From `tools/debug_mcp_servers.py`:**
- ✅ All 6 servers: Files exist
- ✅ All 6 servers: Syntax valid
- ✅ All 6 servers: Import successful

**From `tools/test_mcp_server_connectivity.py`:**
- ✅ MCP config found: `C:\Users\USER\.cursor\mcp.json`
- ⚠️ Servers timeout (expected - stdio transport)

**Conclusion:**
- Server files are **healthy**
- Issue is likely **MCP client connectivity** or **configuration**
- Need to verify Cursor MCP settings are correct

---

## 🎯 Next Steps

1. **Verify Cursor MCP Configuration**
   - Check if servers are listed in Cursor settings
   - Verify paths are correct
   - Check for connection errors in Cursor logs

2. **Restart Cursor**
   - Close Cursor completely
   - Reopen Cursor
   - Check if MCP servers connect

3. **Check Cursor Logs**
   - Look for MCP connection errors
   - Check for Python path issues
   - Verify server startup messages

4. **Test MCP Resources**
   - Use `list_mcp_resources()` after restart
   - Should return resources if connected

---

## 📝 Configuration Reference

**Standard Configuration Format:**

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "description": "Server description"
    }
  }
}
```

**Windows Path Format:**
- Use forward slashes: `D:/path/to/file.py`
- Or escaped backslashes: `D:\\path\\to\\file.py`

**Python Command:**
- Use `python` if in PATH
- Or full path: `C:/Python/python.exe`

---

**Status:** 🔍 Debugging in progress  
**Tools Created:** `debug_mcp_servers.py`, `test_mcp_server_connectivity.py`  
**Next:** Verify Cursor MCP client configuration and connection

