# Dark Theme Fix for DaduDeKC.com Home and About Pages

## Problem
The home page and about page don't match the dark theme style of other pages on the site.

## Solution

### Option 1: Add CSS via WordPress Customizer (Recommended)

1. Log into WordPress Admin: `https://dadudekc.com/wp-admin`
2. Go to **Appearance → Customize**
3. Click on **Additional CSS**
4. Copy and paste the CSS from: `tools/dadudekc_home_about_dark_theme_css.txt`
5. Click **Publish**

### Option 2: Add CSS to Individual Pages

1. Log into WordPress Admin
2. Go to **Pages → All Pages**
3. Edit the **Home** page (ID: 5)
4. Switch to **Text/HTML** editor (not Visual)
5. Add the `<style>` tag with CSS at the beginning of the content
6. Repeat for **About** page (ID: 76)

### Option 3: Automated Fix (Requires Credentials)

If you have WordPress REST API credentials configured:

```bash
python tools/fix_dadudekc_dark_theme_pages.py
```

**Credentials Setup:**
- Set environment variables:
  - `WORDPRESS_USERNAME`
  - `WORDPRESS_APPLICATION_PASSWORD`
  - `WORDPRESS_SITE_URL` (optional, defaults to https://dadudekc.com)

OR create config file: `D:/websites/configs/wordpress_credentials.json`

## CSS Files Generated

1. **`tools/dadudekc_home_about_dark_theme_css.txt`** - Page-specific CSS (targets only home and about pages)
2. **`tools/dadudekc_dark_theme_css.txt`** - General dark theme CSS (applies to all pages)

## What the CSS Does

- Sets dark background (`#1a1a1a`) for body and content areas
- Sets light text color (`#e8e8e8`) for readability
- Styles headings in white (`#ffffff`)
- Styles links in blue (`#4a9eff`) with hover effects
- Styles buttons and form elements to match dark theme
- Uses `!important` to override existing styles

## Verification

After applying the CSS:
1. Visit `https://dadudekc.com` (home page)
2. Visit `https://dadudekc.com/about` (about page)
3. Verify both pages now have dark theme matching other pages

## Notes

- Page IDs used: Home (5), About (76)
- CSS uses page-specific selectors to avoid affecting other pages
- All styles use `!important` to ensure they override existing styles

