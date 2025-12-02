
# Manual WordPress Admin Deployment Instructions

## Site: https://freerideinvestor.com
## File: functions.php
## Theme: freerideinvestor

### Steps:

1. **Log into WordPress Admin**:
   - Go to: https://freerideinvestor.com/wp-admin
   - Enter your WordPress admin credentials
   - Click "Log In"

2. **Navigate to Theme Editor**:
   - In left sidebar, click: **Appearance**
   - Click: **Theme Editor**
   - Select theme: **freerideinvestor**
   - In file list, click: **functions.php**

3. **Replace File Contents**:
   - Select all existing content (Ctrl+A or Cmd+A)
   - Delete selected content (Delete key)
   - Open local file: `D:\websites\FreeRideInvestor\functions.php`
   - Select all content (Ctrl+A or Cmd+A)
   - Copy content (Ctrl+C or Cmd+C)
   - Paste into WordPress editor (Ctrl+V or Cmd+V)

4. **Update File**:
   - Scroll down to bottom of editor
   - Click: **Update File** button
   - Wait for success message

5. **Clear Cache**:
   - Go to: **Settings > Permalinks**
   - Click: **Save Changes** (this clears cache)
   - Or use caching plugin to clear cache

6. **Verify**:
   - Check live site navigation menu
   - Verify Developer Tools links are removed
   - Test site functionality

### File Details:
- **Local File**: D:\websites\FreeRideInvestor\functions.php
- **File Size**: 53,088 bytes
- **Theme**: freerideinvestor
- **Target File**: functions.php

### Troubleshooting:
- If file is too large, WordPress may timeout - try smaller chunks
- If editor doesn't load, check theme permissions
- If update fails, check file syntax for PHP errors
