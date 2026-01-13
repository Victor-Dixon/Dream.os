# GA4/Pixel ID Configuration Template

**Date**: 2025-12-27  
**Agent**: Agent-3 (Infrastructure & DevOps)  
**Coordination**: Agent-5 (Business Intelligence)  
**Status**: Placeholder structure ready - IDs needed

## wp-config.php Configuration Format

### Required Constants

Add the following constants to each site's `wp-config.php` file (before the "That's all, stop editing!" line):

```php
// GA4/Pixel Analytics Configuration
// Replace placeholder values with actual IDs when available

// freerideinvestor.com
define('GA4_MEASUREMENT_ID_FREERIDE', 'G-XXXXXXXXXX'); // GA4 Measurement ID format: G-XXXXXXXXXX
define('FACEBOOK_PIXEL_ID_FREERIDE', '123456789012345'); // Facebook Pixel ID format: 15-digit number

// tradingrobotplug.com
define('GA4_MEASUREMENT_ID_TRADING', 'G-XXXXXXXXXX'); // GA4 Measurement ID format: G-XXXXXXXXXX
define('FACEBOOK_PIXEL_ID_TRADING', '123456789012345'); // Facebook Pixel ID format: 15-digit number

// dadudekc.com
define('GA4_MEASUREMENT_ID_DADUDEKC', 'G-XXXXXXXXXX'); // GA4 Measurement ID format: G-XXXXXXXXXX
define('FACEBOOK_PIXEL_ID_DADUDEKC', '123456789012345'); // Facebook Pixel ID format: 15-digit number

// crosbyultimateevents.com
define('GA4_MEASUREMENT_ID_CROSBY', 'G-XXXXXXXXXX'); // GA4 Measurement ID format: G-XXXXXXXXXX
define('FACEBOOK_PIXEL_ID_CROSBY', '123456789012345'); // Facebook Pixel ID format: 15-digit number
```

### Site-Specific Configuration (Alternative)

If using site-specific constants, update the theme's `functions.php` or `analytics.php` to use the appropriate constant:

```php
// In theme functions.php or analytics.php
$ga4_id = defined('GA4_MEASUREMENT_ID_FREERIDE') ? GA4_MEASUREMENT_ID_FREERIDE : '';
$pixel_id = defined('FACEBOOK_PIXEL_ID_FREERIDE') ? FACEBOOK_PIXEL_ID_FREERIDE : '';
```

### Unified Configuration (Recommended)

For sites using unified constants (current deployment):

```php
// In wp-config.php
define('GA4_MEASUREMENT_ID', 'G-XXXXXXXXXX');
define('FACEBOOK_PIXEL_ID', '123456789012345');
```

## ID Format Specifications

### GA4 Measurement ID
- **Format**: `G-XXXXXXXXXX`
- **Example**: `G-ABC123XYZ9`
- **Length**: 11 characters (G- + 10 alphanumeric)
- **Where to find**: Google Analytics 4 Admin → Data Streams → Measurement ID

### Facebook Pixel ID
- **Format**: 15-digit number
- **Example**: `123456789012345`
- **Length**: Exactly 15 digits
- **Where to find**: Facebook Events Manager → Data Sources → Pixel ID

## Current Deployment Status

### ✅ Code Deployed (Ready for ID Configuration)
1. **freerideinvestor.com**
   - Code location: `wp/wp-content/themes/freerideinvestor-modern/functions.php`
   - Uses: `GA4_MEASUREMENT_ID` and `FACEBOOK_PIXEL_ID` constants
   - Status: ✅ Code deployed, ⏳ IDs needed

2. **tradingrobotplug.com**
   - Code location: `wp/wp-content/themes/tradingrobotplug-theme/functions.php`
   - Uses: `GA4_MEASUREMENT_ID` and `FACEBOOK_PIXEL_ID` constants
   - Status: ✅ Code deployed, ⏳ IDs needed

### ⏳ Remote Deployment Pending (Code + IDs needed)
3. **dadudekc.com**
   - Deployment: Remote (no local WordPress)
   - Manual instructions: `docs/website_audits/2026/dadudekc.com_MANUAL_DEPLOYMENT_INSTRUCTIONS.md`
   - Status: ⏳ Remote deployment + IDs needed

4. **crosbyultimateevents.com**
   - Deployment: Remote (no local WordPress)
   - Manual instructions: `docs/website_audits/2026/crosbyultimateevents.com_MANUAL_DEPLOYMENT_INSTRUCTIONS.md`
   - Status: ⏳ Remote deployment + IDs needed

## Configuration Steps

### For Local Sites (freerideinvestor.com, tradingrobotplug.com)

1. **Access wp-config.php**
   - Location: `wp/wp-config.php` (root of WordPress installation)
   - Backup: Create backup before editing

2. **Add Constants**
   - Add GA4/Pixel constants before "That's all, stop editing!" line
   - Use format shown above

3. **Replace Placeholders**
   - Replace `G-XXXXXXXXXX` with actual GA4 Measurement ID
   - Replace `123456789012345` with actual Facebook Pixel ID

4. **Verify Configuration**
   - Check constants are defined: `defined('GA4_MEASUREMENT_ID')`
   - Verify no syntax errors in wp-config.php

### For Remote Sites (dadudekc.com, crosbyultimateevents.com)

1. **Deploy Code First**
   - Use manual deployment instructions
   - Or coordinate remote deployment access

2. **Configure IDs**
   - Access wp-config.php via SFTP/hosting file manager
   - Add constants using same format

3. **Verify**
   - Check site loads without errors
   - Verify analytics code appears in page source

## ID Request Template

See: `docs/website_audits/2026/GA4_PIXEL_ID_REQUEST_TEMPLATE.md`

## Validation Readiness

**Agent-5 Validation Framework**: ✅ Ready  
**Blocked On**: Actual GA4/Pixel IDs for all 4 sites

Once IDs are configured:
- Agent-5 can run validation immediately
- Automated validation tools ready
- Analytics tracking verification ready

## Next Steps

1. ⏳ **Acquire GA4/Pixel IDs** for all 4 sites
2. ⏳ **Configure wp-config.php** with actual IDs
3. ✅ **Run Agent-5 validation** once IDs configured
4. ⏳ **Coordinate remote deployment** for dadudekc.com and crosbyultimateevents.com

## Status

✅ Configuration Template Ready  
⏳ Awaiting Actual IDs

