# Menu & Content Fixes Execution Plan

**Date:** 2025-12-20  
**Agent:** Agent-7 (Web Development Specialist)  
**Status:** ✅ **TOOL CREATED** - Ready for execution

---

## Task Summary

**freerideinvestor.com:** 6 broken links (4 menu links: About, Blog, Contact)  
**crosbyultimateevents.com:** 1 broken link (Blog in nav menu)

---

## Issues Identified

### **freerideinvestor.com (6 issues)**

**Broken Menu Links:**
1. "About" link in nav menu → `https://freerideinvestor.com/about` (404)
2. "Blog" link in footer menu → `https://freerideinvestor.com/blog` (404)
3. "About" link in footer menu → `https://freerideinvestor.com/about` (404)
4. "Contact" link in footer menu → `https://freerideinvestor.com/contact` (404)

**Action Required:**
- Create missing pages: About, Blog, Contact
- Update menu links to point to correct pages
- Add content to created pages

### **crosbyultimateevents.com (1 issue)**

**Broken Menu Link:**
1. "Blog" link in nav menu → `https://crosbyultimateevents.com/blog` (404)

**Action Required:**
- Blog page exists (ID: 13) but menu link is broken
- Update nav menu to point to correct blog page URL
- Verify blog page is accessible

---

## Execution Plan

### **Step 1: Check Page Existence** ✅

**Tool:** `tools/fix_freeride_crosby_menu_links.py`

**Results:**
- ✅ crosbyultimateevents.com: Blog page exists (ID: 13)
- ⚠️ freerideinvestor.com: REST API credentials not configured

### **Step 2: Create Missing Pages**

**For freerideinvestor.com:**
1. Create "About" page (`/about`)
2. Create "Blog" page (`/blog`)
3. Create "Contact" page (`/contact`)

**Method:**
- Via WordPress REST API (if credentials configured)
- Or manual creation via WordPress admin

### **Step 3: Update Menu Links**

**For freerideinvestor.com:**
- Update nav menu: Fix "About" link
- Update footer menu: Fix "Blog", "About", "Contact" links

**For crosbyultimateevents.com:**
- Update nav menu: Fix "Blog" link to point to page ID 13

**Method:**
- WordPress admin → Appearance → Menus
- Or via REST API if menu endpoints available

### **Step 4: Add Content**

**For created pages:**
- Add appropriate content (About page, Blog archive, Contact form)
- Ensure pages are SEO-friendly

### **Step 5: Verification**

**Command:**
```bash
python tools/comprehensive_website_audit.py --site freerideinvestor.com --check-links
python tools/comprehensive_website_audit.py --site crosbyultimateevents.com --check-links
```

---

## Site Configuration Status

### **freerideinvestor.com** ⚠️
- **REST API:** ⚠️ Not configured in `site_configs.json`
- **Action:** Manual fix required OR configure REST API credentials

### **crosbyultimateevents.com** ✅
- **REST API:** ✅ Configured (dadudeKC@Gmail.com)
- **Status:** Ready for automated fix

---

## Next Actions

### **Immediate:**
1. ✅ Tool created - `fix_freeride_crosby_menu_links.py`
2. ⏳ Configure freerideinvestor.com REST API credentials (or manual fix)
3. ⏳ Fix crosbyultimateevents.com blog menu link
4. ⏳ Create missing pages for freerideinvestor.com

### **Follow-up:**
1. Add content to created pages
2. Test all menu links
3. Verify fixes with audit tool

---

## Files

**Tool:** `tools/fix_freeride_crosby_menu_links.py`  
**Documentation:** `docs/website_grade_cards/menu_content_fixes_execution_plan.md`

---

**Status**: ✅ **TOOL CREATED** - Ready for execution

**Next Action:** Configure freerideinvestor.com credentials or proceed with manual fixes

🐝 **WE. ARE. SWARM. ⚡**

