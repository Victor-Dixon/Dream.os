
# Build-In-Public Phase 0 Deployment Instructions
## Generated: 2025-12-26 06:27:55

**Task:** A4-WEB-PUBLIC-001  
**Phase:** Phase 0 - Visible Placeholders  
**Status:** Ready for deployment

---

## dadudekc.com Deployment

### Files to Deploy:
- `front-page.php`
- `style.css`

### Deployment Method 1: SFTP/File Manager (RECOMMENDED)

1. **Connect to server via SFTP or hosting File Manager**
2. **Navigate to:** `wp-content/themes/dadudekc/`
3. **Upload/Update files:**
   - `front-page.php` (7,933 bytes)
   - `style.css` (8,884 bytes)

4. **Verify theme activation:**
   - Login: https://dadudekc.com/wp-admin
   - Navigate: Appearance → Themes
   - Verify "dadudekc" theme is active

5. **Clear cache:**
   - Clear browser cache
   - Clear WordPress cache (if plugin installed)
   - Clear CDN cache (if applicable)

### Deployment Method 2: WordPress Admin Theme Editor

1. **Login:** https://dadudekc.com/wp-admin
2. **Navigate:** Appearance → Theme Editor
3. **Select theme:** dadudekc
4. **Edit files directly** (copy content from local files)

---

## weareswarm.online Deployment

### Files to Deploy:
- `style.css`
- `functions.php`
- `header.php`
- `footer.php`
- `front-page.php`
- `index.php`
- `page-swarm-manifesto.php`
- `page-how-the-swarm-works.php`

### Deployment Method 1: SFTP/File Manager (RECOMMENDED)

1. **Connect to server via SFTP or hosting File Manager**
2. **Navigate to:** `wp-content/themes/swarm/`
3. **Create theme directory if it doesn't exist**
4. **Upload all theme files:**
   - `style.css` (4,866 bytes)
   - `functions.php` (763 bytes)
   - `header.php` (703 bytes)
   - `footer.php` (248 bytes)
   - `front-page.php` (2,278 bytes)
   - `index.php` (383 bytes)
   - `page-swarm-manifesto.php` (1,398 bytes)
   - `page-how-the-swarm-works.php` (1,741 bytes)

5. **Activate theme:**
   - Login: https://weareswarm.online/wp-admin
   - Navigate: Appearance → Themes
   - Activate "swarm" theme

6. **Clear cache:**
   - Clear browser cache
   - Clear WordPress cache (if plugin installed)
   - Clear CDN cache (if applicable)

### Deployment Method 2: WordPress Admin Theme Editor

1. **Login:** https://weareswarm.online/wp-admin
2. **Navigate:** Appearance → Theme Editor
3. **Select theme:** swarm (or create new theme)
4. **Edit files directly** (copy content from local files)

---

## Verification Checklist

### dadudekc.com:
- [ ] front-page.php uploaded
- [ ] style.css uploaded (if updated)
- [ ] Theme active
- [ ] "What I Do" section visible (3 offer cards)
- [ ] "Receipts / Proof" section visible
- [ ] "Live Experiments" feed visible
- [ ] Primary CTA ("Start a Build Sprint") visible
- [ ] All sections display correctly
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Cache cleared

### weareswarm.online:
- [ ] All theme files uploaded
- [ ] Theme activated
- [ ] Homepage "Build in Public" section visible
- [ ] "Swarm Manifesto" page accessible (/swarm-manifesto)
- [ ] "How the Swarm Works" page accessible (/how-the-swarm-works)
- [ ] Cross-links to dadudekc.com visible
- [ ] Dark theme styling applied
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Cache cleared

---

## Post-Deployment Verification

1. **Visit dadudekc.com:**
   - Check homepage for "What I Do" section
   - Check "Receipts / Proof" section
   - Check "Live Experiments" feed
   - Verify primary CTA visible

2. **Visit weareswarm.online:**
   - Check homepage for "Build in Public" section
   - Visit /swarm-manifesto page
   - Visit /how-the-swarm-works page
   - Verify cross-links to dadudekc.com

3. **Test functionality:**
   - Click CTAs (should work or show placeholder behavior)
   - Test cross-links
   - Check mobile responsiveness
   - Verify no console errors

---

## Deployment Plan Summary

**dadudekc.com:**
- Files: 2 files
- Location: `wp-content/themes/dadudekc/`
- Method: SFTP/File Manager or WordPress Admin

**weareswarm.online:**
- Files: 8 files
- Location: `wp-content/themes/swarm/`
- Method: SFTP/File Manager or WordPress Admin

**Total Files:** 10 files

---

**Deployment Instructions Generated:** 2025-12-26 06:27:55  
**Agent-3 (Infrastructure & DevOps)**  
**Status:** ✅ Ready for deployment execution
