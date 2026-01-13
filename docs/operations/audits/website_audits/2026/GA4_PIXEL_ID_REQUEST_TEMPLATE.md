# GA4/Pixel ID Request Template

**Date**: 2025-12-27  
**Agent**: Agent-3 (Infrastructure & DevOps)  
**Coordination**: Agent-5 (Business Intelligence)  
**Purpose**: Template for requesting GA4/Pixel IDs

## ID Request Checklist

### Required IDs for Analytics Validation

| Site | GA4 Measurement ID | Facebook Pixel ID | Status |
|------|-------------------|-------------------|--------|
| freerideinvestor.com | ⏳ Needed | ⏳ Needed | Code deployed ✅ |
| tradingrobotplug.com | ⏳ Needed | ⏳ Needed | Code deployed ✅ |
| dadudekc.com | ⏳ Needed | ⏳ Needed | Remote deployment pending |
| crosbyultimateevents.com | ⏳ Needed | ⏳ Needed | Remote deployment pending |

## ID Format Requirements

### GA4 Measurement ID
- **Format**: `G-XXXXXXXXXX` (G- + 10 alphanumeric characters)
- **Example**: `G-ABC123XYZ9`
- **Where to find**: 
  - Google Analytics 4 Admin
  - Data Streams → Select property → Measurement ID
  - Format: G-XXXXXXXXXX

### Facebook Pixel ID
- **Format**: 15-digit number
- **Example**: `123456789012345`
- **Where to find**:
  - Facebook Events Manager
  - Data Sources → Select Pixel → Pixel ID
  - Format: 15-digit number

## Request Template

### For Site Owner/Stakeholder

```
Subject: GA4/Pixel ID Request - [Site Name]

Hi [Name],

We're setting up analytics tracking for [Site Name] and need the following IDs:

1. GA4 Measurement ID (Google Analytics 4)
   - Format: G-XXXXXXXXXX
   - Location: Google Analytics Admin → Data Streams → Measurement ID
   - If you don't have GA4 set up, we can create one or use Universal Analytics ID

2. Facebook Pixel ID
   - Format: 15-digit number
   - Location: Facebook Events Manager → Data Sources → Pixel ID
   - If you don't have a Pixel, we can create one

Once we have these IDs, we'll configure them in wp-config.php and run validation.

Please provide:
- GA4 Measurement ID: [G-XXXXXXXXXX]
- Facebook Pixel ID: [123456789012345]

Thanks!
```

### For Internal Coordination

```
Subject: GA4/Pixel ID Acquisition - [Site Name]

Agent-5 / [Coordinator],

Requesting GA4/Pixel IDs for analytics validation:

Site: [Site Name]
URL: [https://site.com]

Current Status:
- Code deployed: ✅ / ⏳
- wp-config.php ready: ✅
- Validation framework: ✅ Ready

Blocked on:
- GA4 Measurement ID: ⏳ Needed
- Facebook Pixel ID: ⏳ Needed

Next Steps:
1. Acquire IDs from [source]
2. Configure in wp-config.php
3. Run validation

Can you help acquire these IDs or provide guidance on ID creation?
```

## ID Creation Options

### If IDs Don't Exist

#### GA4 Measurement ID
1. **Create New GA4 Property**
   - Go to Google Analytics
   - Admin → Create Property
   - Select "GA4" property type
   - Add website URL
   - Get Measurement ID from Data Streams

2. **Use Universal Analytics**
   - If only Universal Analytics exists
   - Can migrate or create GA4 property
   - Or use Universal Analytics ID temporarily

#### Facebook Pixel ID
1. **Create New Pixel**
   - Go to Facebook Events Manager
   - Data Sources → Connect Data → Web
   - Create new Pixel
   - Get Pixel ID (15-digit number)

2. **Use Existing Pixel**
   - If Pixel already exists
   - Get ID from Events Manager
   - Verify it's active

## Placeholder Configuration

Until actual IDs are available, sites can use placeholder configuration:

```php
// Placeholder configuration (for testing structure)
define('GA4_MEASUREMENT_ID', 'G-PLACEHOLDER');
define('FACEBOOK_PIXEL_ID', '000000000000000');
```

**Note**: Placeholders will not track analytics but allow code structure validation.

## Priority Sites

### High Priority (Code Already Deployed)
1. **freerideinvestor.com** - Code deployed ✅, IDs needed ⏳
2. **tradingrobotplug.com** - Code deployed ✅, IDs needed ⏳

### Medium Priority (Remote Deployment Pending)
3. **dadudekc.com** - Remote deployment + IDs needed ⏳
4. **crosbyultimateevents.com** - Remote deployment + IDs needed ⏳

## Coordination

**Agent-3 Role**: Infrastructure/Deployment (wp-config.php configuration)  
**Agent-5 Role**: Analytics Validation (ID acquisition, validation framework)

**Synergy**: Agent-3 handles configuration once IDs available; Agent-5 handles ID acquisition and validation.

## Status

✅ Request Template Ready  
⏳ Awaiting ID Acquisition

