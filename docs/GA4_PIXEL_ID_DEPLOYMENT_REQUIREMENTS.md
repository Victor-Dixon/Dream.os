# GA4/Pixel ID Deployment Requirements

**Generated:** 2025-12-30
**Agent:** Agent-3 (Infrastructure & DevOps)
**Purpose:** Document ID requirements for analytics validation blocker resolution

## Current Status (per Agent-5 validation)

### Sites Requiring ID Deployment

1. **freerideinvestor.com**
   - GA4 Measurement ID: ❌ NOT SET (needed)
   - Facebook Pixel ID: ✅ Configured (000000000000000 placeholder - needs real ID)
   - Status: CONFIGURED (but has placeholder)

2. **tradingrobotplug.com**
   - GA4 Measurement ID: ❌ NOT SET (needed)
   - Facebook Pixel ID: ✅ Configured (000000000000000 placeholder - needs real ID)
   - Status: MISSING

3. **dadudekc.com**
   - GA4 Measurement ID: ❌ NOT SET (needed)
   - Facebook Pixel ID: ❌ NOT SET (needed)
   - Status: MISSING

4. **crosbyultimateevents.com**
   - GA4 Measurement ID: ❌ NOT SET (needed)
   - Facebook Pixel ID: ❌ NOT SET (needed)
   - Status: MISSING

## ID Requirements Summary

**Total IDs Needed:**
- GA4 Measurement IDs: 4 (one per site)
- Facebook Pixel IDs: 4 (one per site)
- **Total: 8 IDs**

## Deployment Target

**File:** `wp-config.php` on remote WordPress servers
**Constants:**
- `GA4_MEASUREMENT_ID`
- `FACEBOOK_PIXEL_ID`

**Format:**
```php
define('GA4_MEASUREMENT_ID', 'G-XXXXXXXXXX');
define('FACEBOOK_PIXEL_ID', '123456789012345');
```

## Deployment Method

1. **Access:** SSH to remote servers or WP-CLI
2. **File Location:** `/path/to/wordpress/wp-config.php`
3. **Update:** Replace placeholder values or add constants if missing
4. **Verification:** Use `tools/automated_p0_analytics_validation.py` to verify

## Blocker

**Status:** ⚠️ BLOCKED
**Reason:** Real GA4/Pixel IDs not available in local configuration
**Action Required:** 
- Coordinate with Agent-4/user to obtain real ID values
- Once IDs provided, deployment can proceed immediately
- Estimated deployment time: 30-45 minutes for all 4 sites

## Next Steps

1. ✅ Analysis complete - requirements documented
2. ⏳ Waiting for real ID values from Agent-4/user
3. ⏳ Deploy IDs to wp-config.php once values provided
4. ⏳ Verify deployment using validation tool
5. ⏳ Notify Agent-5 for re-validation

