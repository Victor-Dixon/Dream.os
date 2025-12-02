# Manual Deployment Checklist - URGENT

**Date**: 2025-12-01  
**Status**: ✅ **APPROVED FOR EXECUTION**  
**Priority**: CRITICAL

---

## 🚀 **DEPLOYMENT TASKS**

### **Task 1: FreeRideInvestor Deployment** (2-3 minutes)

- [ ] **Step 1**: Open `https://freerideinvestor.com/wp-admin`
- [ ] **Step 2**: Log in with WordPress admin credentials
- [ ] **Step 3**: Navigate to **Appearance > Theme Editor**
- [ ] **Step 4**: Select theme: **freerideinvestor**
- [ ] **Step 5**: Click **functions.php** in file list
- [ ] **Step 6**: Select all content (Ctrl+A), Delete
- [ ] **Step 7**: Open `D:\websites\FreeRideInvestor\functions.php`
- [ ] **Step 8**: Copy all content (Ctrl+A, Ctrl+C)
- [ ] **Step 9**: Paste into WordPress editor (Ctrl+V)
- [ ] **Step 10**: Click **Update File** button
- [ ] **Step 11**: Verify success message appears
- [ ] **Step 12**: Clear cache: **Settings > Permalinks > Save Changes**
- [ ] **Step 13**: Verify menu: **Appearance > Menus** (should show 0 Developer Tools links)

**File**: `D:\websites\FreeRideInvestor\functions.php` (53,088 bytes)  
**Goal**: Remove 18 Developer Tools links from navigation

---

### **Task 2: prismblossom.online Deployment** (2-3 minutes)

- [ ] **Step 1**: Open `https://prismblossom.online/wp-admin`
- [ ] **Step 2**: Log in with WordPress admin credentials
- [ ] **Step 3**: Navigate to **Appearance > Theme Editor**
- [ ] **Step 4**: Select theme: **prismblossom**
- [ ] **Step 5**: Click **functions.php** in file list
- [ ] **Step 6**: Select all content (Ctrl+A), Delete
- [ ] **Step 7**: Open `D:\websites\prismblossom.online\wordpress-theme\prismblossom\functions.php`
- [ ] **Step 8**: Copy all content (Ctrl+A, Ctrl+C)
- [ ] **Step 9**: Paste into WordPress editor (Ctrl+V)
- [ ] **Step 10**: Click **Update File** button
- [ ] **Step 11**: Verify success message appears
- [ ] **Step 12**: Clear cache: **Settings > Permalinks > Save Changes**

**File**: `D:\websites\prismblossom.online\wordpress-theme\prismblossom\functions.php`  
**Goal**: Fix text rendering issues

---

## ✅ **VERIFICATION TASKS**

### **FreeRideInvestor Verification**:

- [ ] **Check Navigation Menu**:
  - Visit: `https://freerideinvestor.com`
  - Count Developer Tools links in navigation
  - **Expected**: 0 links (currently 18)
  - **Status**: [ ] PASS / [ ] FAIL

- [ ] **Check Text Rendering**:
  - Verify no broken words (e.g., "Tbow Tactic" should be "TBOW Tactics")
  - **Status**: [ ] PASS / [ ] FAIL

- [ ] **Check Site Functionality**:
  - Test navigation links
  - Test page loading
  - **Status**: [ ] PASS / [ ] FAIL

---

### **prismblossom.online Verification**:

- [ ] **Check Text Rendering**:
  - Visit: `https://prismblossom.online`
  - Verify no broken words (e.g., "pri mblo om" should be "prismblossom")
  - **Status**: [ ] PASS / [ ] FAIL

- [ ] **Check Contact Form**:
  - Visit: `https://prismblossom.online/contact`
  - Verify form displays correctly
  - Test form submission (if possible)
  - **Status**: [ ] PASS / [ ] FAIL

- [ ] **Check Site Functionality**:
  - Test navigation
  - Test page loading
  - **Status**: [ ] PASS / [ ] FAIL

---

## 🔧 **AUTOMATED VERIFICATION**

After manual deployment, run:

```bash
python tools/verify_website_fixes.py
```

**Expected Results**:
- FreeRideInvestor: 0 Developer Tools links
- prismblossom.online: No text rendering issues

---

## 📋 **POST-DEPLOYMENT ACTIONS**

- [ ] Run automated verification tool
- [ ] Document deployment results
- [ ] Report to Captain
- [ ] Update deployment status

---

## ⚠️ **TROUBLESHOOTING**

**If file update fails**:
- Check for PHP syntax errors
- Verify file content copied correctly
- Try again

**If cache doesn't clear**:
- Use caching plugin to clear cache
- Or wait 5-10 minutes for cache to expire

**If menu still shows Developer Tools**:
- Go to **Appearance > Menus**
- Manually remove any Developer Tools items
- Save menu

---

**Status**: ⏳ **READY FOR EXECUTION**  
**Total Time**: ~5 minutes  
**Priority**: CRITICAL

🐝 **WE. ARE. SWARM. ⚡🔥**

