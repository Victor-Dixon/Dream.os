# Deployment Credential Analysis - Why Swarm Can Deploy

**Date**: 2025-12-03  
**Issue**: User questioning why swarm can deploy if sites.json isn't the problem

---

## 🔍 **ROOT CAUSE IDENTIFIED**

### **The Real Issue: Protocol Mismatch**

**sites.json** contains:
- **FTP credentials** (port 21)
- All sites configured with FTP (port 21)

**wordpress_manager.py** (primary deployment tool) uses:
- **SFTP** (port 65002) by default
- Falls back to `.env` environment variables when sites.json doesn't match

---

## 📊 **CREDENTIAL LOADING FLOW**

### **wordpress_manager.py Load Order:**

1. **First**: Try `sites.json` (FTP, port 21)
   - ❌ **Mismatch**: Tool needs SFTP (port 65002), sites.json has FTP (port 21)
   - ⚠️ **Result**: Credentials rejected (wrong protocol)

2. **Fallback**: Try `.env` environment variables (SFTP, port 65002)
   - ✅ **Match**: Tool uses SFTP, .env has SFTP credentials
   - ✅ **Result**: Deployment works using .env credentials

---

## ✅ **WHY DEPLOYMENT WORKS**

**The swarm can deploy because:**
- `.env` file has working SFTP credentials (port 65002)
- `wordpress_manager.py` falls back to `.env` when sites.json doesn't match
- SFTP connection succeeds using `.env` credentials

**sites.json isn't the problem because:**
- It has valid FTP credentials (port 21)
- But tools are using SFTP (port 65002)
- Tools automatically fall back to `.env` for SFTP

---

## 🔧 **SOLUTION OPTIONS**

### **Option 1: Update sites.json for SFTP** (Recommended)
- Change port from `21` (FTP) to `65002` (SFTP)
- Keep same host, username, password
- Tools will use sites.json instead of .env fallback

### **Option 2: Keep Current Setup**
- Leave sites.json as FTP (port 21)
- Keep .env with SFTP (port 65002)
- Tools continue using .env fallback (works fine)

### **Option 3: Use FTP Tools**
- Use `ftp_deployer.py` instead of `wordpress_manager.py`
- `ftp_deployer.py` uses FTP (port 21) and works with sites.json
- No fallback needed

---

## 📋 **TOOLS AND PROTOCOLS**

| Tool | Protocol | Port | Uses sites.json? |
|------|----------|------|------------------|
| `wordpress_manager.py` | SFTP | 65002 | ❌ Falls back to .env |
| `ftp_deployer.py` | FTP | 21 | ✅ Uses sites.json |
| `deploy_via_sftp.py` | SFTP | 65002 | ❌ Falls back to .env |

---

## 🎯 **RECOMMENDATION**

**Update sites.json to use SFTP (port 65002)** for consistency:
- All sites already have correct host, username, password
- Only need to change port from `21` to `65002`
- Tools will use sites.json directly (no fallback needed)
- Single source of truth for credentials

---

**Status**: ✅ **Root cause identified** - Protocol mismatch, not credential problem  
**Action**: Update sites.json ports to 65002 for SFTP compatibility



