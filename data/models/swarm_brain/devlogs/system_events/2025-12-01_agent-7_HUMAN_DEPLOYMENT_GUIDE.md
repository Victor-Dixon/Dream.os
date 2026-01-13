# Human Deployment Guide - Step-by-Step Instructions

**Date**: 2025-12-01 20:27:00  
**Agent**: Agent-7 (Web Development Specialist)  
**Status**: 📋 **READY FOR HUMAN DEPLOYMENT**

---

## 🎯 **DEPLOYMENT OVERVIEW**

**Sites to Deploy**: 2  
**Priority**: HIGH  
**Estimated Time**: 5-10 minutes per site

---

## 📋 **DEPLOYMENT CHECKLIST**

### **Before Starting**:
- [ ] Both files verified and ready
- [ ] WordPress admin access available
- [ ] Browser ready (Chrome/Firefox recommended)

### **After Deployment**:
- [ ] Run verification script
- [ ] Check both sites manually
- [ ] Create completion report

---

## 🚀 **SITE 1: prismblossom.online - CSS Fix**

### **File to Deploy**:
- **Local Path**: `D:\websites\prismblossom.online\wordpress-theme\prismblossom\functions.php`
- **Theme**: prismblossom
- **File**: functions.php

### **What Changed**:
- Added ligature fixes: `font-feature-settings: 'liga' 0 !important;`
- Added: `font-variant-ligatures: none !important;`
- Applied to body and all text elements

### **Step-by-Step Instructions**:

1. **Open WordPress Admin**:
   - Go to: `https://prismblossom.online/wp-admin`
   - Log in with your WordPress credentials

2. **Navigate to Theme Editor**:
   - Click: **Appearance** (left sidebar)
   - Click: **Theme Editor**

3. **Select Theme and File**:
   - **Select theme**: Choose **prismblossom** from dropdown (top right)
   - **Select file**: Click **functions.php** from file list (left sidebar)

4. **Locate the CSS Block**:
   - Press **Ctrl+F** to open find dialog
   - Search for: `$text_rendering_css`
   - You should see it around line 42

5. **Replace the CSS Block**:
   - Find this section (around lines 42-65):
   ```php
   $text_rendering_css = "
       body, body * {
           font-family: 'Rubik Bubbles', 'Arial', 'Helvetica Neue', 'Helvetica', sans-serif !important;
           text-rendering: optimizeLegibility !important;
           ...
       }
   ";
   ```
   - **Replace entire CSS block** with this (includes ligature fixes):
   ```php
   $text_rendering_css = "
       body, body * {
           font-family: 'Rubik Bubbles', 'Arial', 'Helvetica Neue', 'Helvetica', sans-serif !important;
           text-rendering: optimizeLegibility !important;
           -webkit-font-smoothing: antialiased !important;
           -moz-osx-font-smoothing: grayscale !important;
           -webkit-text-size-adjust: 100% !important;
           -ms-text-size-adjust: 100% !important;
           text-size-adjust: 100% !important;
           letter-spacing: normal !important;
           word-spacing: normal !important;
           font-feature-settings: 'liga' 0 !important;
           font-variant-ligatures: none !important;
           font-variant: normal !important;
       }
       /* Fix for specific text rendering issues */
       h1, h2, h3, h4, h5, h6, p, span, div, a, label, button {
           letter-spacing: 0 !important;
           word-spacing: 0.1em !important;
           font-feature-settings: 'liga' 0 !important;
           font-variant-ligatures: none !important;
       }
       /* Ensure no font loading causes spacing issues */
       @font-face {
           font-display: swap;
       }
   ";
   ```

6. **Save Changes**:
   - Click: **Update File** button (bottom of editor)
   - Wait for confirmation message

7. **Clear Cache**:
   - Go to: **Settings > Permalinks**
   - Click: **Save Changes** (this clears WordPress cache)

8. **Verify**:
   - Visit: `https://prismblossom.online`
   - Check: Text should render correctly (no broken "prismblossom.online" pattern)
   - Visit: `https://prismblossom.online/carmyn`
   - Check: Text should render correctly

---

## 🚀 **SITE 2: FreeRideInvestor - Menu Filter Verification**

### **File to Check/Deploy**:
- **Local Path**: `D:\websites\FreeRideInvestor\functions.php`
- **Theme**: freerideinvestor
- **File**: functions.php

### **What to Verify**:
- Menu filter functions should be present
- Functions should remove Developer Tools links

### **Step-by-Step Instructions**:

#### **Step 1: Check if functions.php is Deployed**

1. **Open WordPress Admin**:
   - Go to: `https://freerideinvestor.com/wp-admin`
   - Log in with your WordPress credentials

2. **Navigate to Theme Editor**:
   - Click: **Appearance** (left sidebar)
   - Click: **Theme Editor**

3. **Select Theme and File**:
   - **Select theme**: Choose **freerideinvestor** from dropdown
   - **Select file**: Click **functions.php** from file list

4. **Search for Menu Filter**:
   - Press **Ctrl+F** to open find dialog
   - Search for: `freeride_dedupe_developer_tools_menu`
   - **If found**: Function is deployed, proceed to Step 2
   - **If not found**: Function not deployed, proceed to Step 1b

#### **Step 1b: Deploy functions.php (If Not Found)**

1. **Open Local File**:
   - Open: `D:\websites\FreeRideInvestor\functions.php` in text editor
   - Select all (Ctrl+A) and copy (Ctrl+C)

2. **Replace in WordPress Editor**:
   - In WordPress Theme Editor, select all (Ctrl+A)
   - Paste (Ctrl+V) to replace entire file
   - Click: **Update File**
   - Wait for confirmation

3. **Clear Cache**:
   - Go to: **Settings > Permalinks**
   - Click: **Save Changes**

#### **Step 2: Test Menu Filter**

1. **Clear All Caches**:
   - Go to: **Settings > Permalinks**
   - Click: **Save Changes**
   - Clear any caching plugin cache if present

2. **Check Navigation Menu**:
   - Visit: `https://freerideinvestor.com`
   - Check navigation menu
   - Count Developer Tools links

3. **If 0 Links Found**: ✅ **SUCCESS - Filter Working**
4. **If Links Still Present**: Proceed to Step 3

#### **Step 3: Manual Menu Cleanup (If Filter Not Working)**

1. **Navigate to Menus**:
   - Go to: **Appearance > Menus**
   - Select: **Primary Menu** (or main menu)

2. **Remove Developer Tools Items**:
   - Find all menu items containing:
     - "Developer Tool"
     - "Developer Tools"
     - "dev tool"
     - "dev tools"
   - For each item:
     - Click the item to expand
     - Click: **Remove** link
   - Repeat until all Developer Tools items removed

3. **Save Menu**:
   - Click: **Save Menu** button
   - Wait for confirmation

4. **Clear Cache**:
   - Go to: **Settings > Permalinks**
   - Click: **Save Changes**

5. **Verify**:
   - Visit: `https://freerideinvestor.com`
   - Check navigation menu
   - Should see: **0 Developer Tools links**

---

## ✅ **POST-DEPLOYMENT VERIFICATION**

### **After Both Sites Deployed**:

1. **Run Verification Script**:
   ```bash
   python tools/post_deployment_verification.py
   ```

2. **Expected Results**:
   - **FreeRideInvestor**: 0 Developer Tools links ✅
   - **prismblossom.online**: Text rendering "success" ✅

3. **Manual Verification**:
   - **FreeRideInvestor**: Visit homepage, check navigation menu
   - **prismblossom.online**: Visit homepage, check text rendering
   - **prismblossom.online/carmyn**: Visit Carmyn page, check text rendering

4. **Report Results**:
   - Document in: `DEPLOYMENT_COMPLETION_REPORT.md`
   - Report to Captain

---

## 🚨 **TROUBLESHOOTING**

### **If CSS Fix Doesn't Work**:
- Hard refresh browser: **Ctrl+F5**
- Clear browser cache
- Check WordPress cache plugin
- Verify CSS is in `<head>` section (view page source)

### **If Menu Filter Doesn't Work**:
- Verify menu location is "primary"
- Clear all caches (WordPress, browser, CDN)
- Check if menu items added via different method
- Use manual removal as fallback

### **If File Update Fails**:
- Check file permissions
- Try uploading via SFTP/File Manager instead
- Contact hosting support if needed

---

## 📊 **QUICK REFERENCE**

### **prismblossom.online**:
- **URL**: `https://prismblossom.online/wp-admin`
- **Theme**: prismblossom
- **File**: functions.php
- **Change**: Add ligature fixes to CSS

### **FreeRideInvestor**:
- **URL**: `https://freerideinvestor.com/wp-admin`
- **Theme**: freerideinvestor
- **File**: functions.php
- **Change**: Verify menu filter, manual cleanup if needed

---

**Guide Generated**: 2025-12-01 20:27:00  
**Agent**: Agent-7 (Web Development Specialist)

🐝 **WE. ARE. SWARM. ⚡🔥**

