# Hostinger API Credential Discovery - Agent-3

**Date**: 2025-12-01  
**Purpose**: Use Hostinger API to discover SFTP credentials automatically  
**Status**: ✅ **TOOL CREATED**

---

## 🎯 **OBJECTIVE**

Extend WordPressManager to use Hostinger API to discover SFTP credentials, then use those credentials for deployment via existing SFTP system.

---

## 🛠️ **TOOL CREATED**

### **Hostinger API Helper** ✅

**File**: `tools/hostinger_api_helper.py` (350 lines, V2 compliant)

**Features**:
- Uses Hostinger API to discover SFTP host/server information
- Retrieves domain and hosting information
- Attempts to extract FTP/SFTP credentials from API
- Auto-updates `.env` file with discovered credentials
- Falls back to common Hostinger patterns if API doesn't provide full info

---

## 🚀 **USAGE**

### **Discover Credentials for a Domain**:
```bash
python tools/hostinger_api_helper.py --domain freerideinvestor.com --update-env
```

**What it does**:
1. Uses `HOSTINGER_API_KEY` from `.env` file
2. Queries Hostinger API for domain/hosting info
3. Extracts SFTP host, port, username (if available)
4. Updates `.env` file with `HOSTINGER_HOST` and `HOSTINGER_PORT`
5. Uses existing password from `.env` (API doesn't return passwords for security)

### **List All Domains**:
```bash
python tools/hostinger_api_helper.py --list-domains
```

**Output**: Shows all domains in your Hostinger account

---

## 📋 **HOW IT WORKS**

### **Step 1: API Discovery**
- Queries Hostinger API for domain information
- Gets hosting server details
- Attempts to get FTP/SFTP information

### **Step 2: Credential Extraction**
- Extracts server IP/hostname from API response
- Gets port (defaults to 65002 for Hostinger)
- Gets username if available in API
- **Note**: Password not returned by API (security)

### **Step 3: .env Update**
- Updates or adds `HOSTINGER_HOST` to `.env`
- Updates or adds `HOSTINGER_PORT` to `.env`
- Updates or adds `HOSTINGER_USER` if found
- Preserves existing `HOSTINGER_PASS` (you already have this)

### **Step 4: Use Existing SFTP System**
- WordPressManager automatically uses updated `.env` credentials
- Existing SFTP deployment system works as before
- No breaking changes to existing functionality

---

## 🔧 **REQUIREMENTS**

### **1. Install requests library**:
```bash
pip install requests
```

### **2. Set HOSTINGER_API_KEY in .env**:
```env
HOSTINGER_API_KEY=your_api_key_here
```

**How to get API key**:
1. Log into Hostinger hPanel
2. Go to API section
3. Generate API token
4. Copy token to `.env` file

---

## ✅ **BENEFITS**

1. **Automated Discovery**: No manual lookup of server IP
2. **No Breaking Changes**: Still uses existing SFTP system
3. **Auto-Update**: Updates `.env` automatically
4. **Fallback Safe**: If API fails, can still manually set `HOSTINGER_HOST`

---

## 🚀 **WORKFLOW**

### **Before (Manual)**:
1. Log into Hostinger hPanel
2. Find FTP/SFTP server address
3. Manually add `HOSTINGER_HOST` to `.env`
4. Deploy using SFTP

### **After (Automated)**:
1. Run: `python tools/hostinger_api_helper.py --domain freerideinvestor.com --update-env`
2. Tool discovers `HOSTINGER_HOST` from API
3. Updates `.env` automatically
4. Deploy using SFTP (same as before)

---

## 📊 **EXAMPLE USAGE**

```bash
# Discover credentials for FreeRideInvestor
python tools/hostinger_api_helper.py --domain freerideinvestor.com --update-env

# Output:
# 🔍 Discovering SFTP credentials for freerideinvestor.com...
# ✅ Discovered host: 157.173.214.121
# ✅ Port: 65002
# ✅ Username: u123456789
# ✅ Updated .env file: .env

# Now deploy using existing tool
python tools/deploy_freeride_functions.py
```

---

## ⚠️ **LIMITATIONS**

1. **Password Not in API**: Hostinger API doesn't return passwords (security)
   - **Solution**: Use existing `HOSTINGER_PASS` in `.env` (you already have this)

2. **API Endpoints May Vary**: Hostinger API structure may differ
   - **Solution**: Tool tries multiple endpoints and falls back to common patterns

3. **Username May Not Be Available**: Some API responses don't include username
   - **Solution**: Use existing `HOSTINGER_USER` in `.env` if API doesn't provide

---

## ✅ **STATUS**

**Tool Created**: ✅ `tools/hostinger_api_helper.py`  
**Integration**: ✅ Works with existing WordPressManager  
**Breaking Changes**: ❌ None - extends existing functionality  
**Ready to Use**: ✅ After installing `requests` and setting `HOSTINGER_API_KEY`

---

**Created By**: Agent-3 (Infrastructure & DevOps Specialist)  
**Date**: 2025-12-01

🐝 **WE. ARE. SWARM. ⚡🔥**

