# Manual Repository Replacement Instructions

**Date**: 2025-11-22  
**Status**: READY TO EXECUTE  
**Priority**: P0-CRITICAL

---

## 🎯 Situation

- ✅ BFG cleanup complete (4,565 commits cleaned)
- ✅ Mirror verified: `.env` completely removed from history
- ✅ Mirror location: `D:\temp\Agent_Cellphone_V2_Repository.git`
- ⚠️ Current directory locked/in use - manual replacement required

---

## 🔧 Manual Execution Steps

### **Option A: Complete Replacement (Recommended)**

1. **Close Cursor/IDE** (to unlock directory)

2. **Open PowerShell as Administrator**

3. **Navigate and backup**:
   ```powershell
   cd D:\
   Move-Item -Path "Agent_Cellphone_V2_Repository" -Destination "Agent_Cellphone_V2_Repository.backup" -Force
   ```

4. **Clone cleaned mirror**:
   ```powershell
   git clone D:\temp\Agent_Cellphone_V2_Repository.git Agent_Cellphone_V2_Repository
   cd Agent_Cellphone_V2_Repository
   ```

5. **Verify .env removed**:
   ```powershell
   git log --all --full-history --source -- .env
   # Should return nothing
   ```

6. **Force push**:
   ```powershell
   git push origin agent --force
   ```

7. **Reopen Cursor/IDE** in the new repository

---

### **Option B: Update Current Repository (If directory can't be replaced)**

1. **In current repository** (if git still works):
   ```powershell
   cd D:\Agent_Cellphone_V2_Repository
   git remote add cleaned-mirror D:\temp\Agent_Cellphone_V2_Repository.git
   git fetch cleaned-mirror
   git reset --hard cleaned-mirror/agent
   git push origin agent --force
   ```

---

## ✅ Verification

After replacement, verify:
```powershell
# Check .env removed
git log --all --full-history --source -- .env
# Should return nothing

# Check push successful
git log origin/agent --oneline | Select-Object -First 3
```

---

## 📋 Status

- ✅ **Mirror verified clean**: `.env` completely removed
- ✅ **Pre-commit hook**: Active (prevents future .env commits)
- ✅ **Emergency protocol**: Complete and documented
- ⏳ **Replacement**: Ready to execute manually

---

**Next**: Execute manual replacement when directory is unlocked

