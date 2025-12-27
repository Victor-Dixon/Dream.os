# Quick Start: Devlog Feed for WeAreSwarm.Online

## 🚀 Quick Setup (3 Steps)

### Step 1: Generate Feed

```bash
python tools/generate_devlog_feed.py --output runtime/feeds/public_build_feed.json
```

This scans all devlogs in `agent_workspaces/*/devlogs/` and generates a JSON Feed.

### Step 2: Upload to WordPress

Upload the generated feed file to weareswarm.online:

**Option A: FTP/SFTP**
- Upload `runtime/feeds/public_build_feed.json` to: `/wp-content/themes/runtime/feeds/public_build_feed.json`

**Option B: WordPress Admin (if plugin installed)**
- Upload via WordPress file manager or plugin interface

### Step 3: Display on Website

**Option A: Shortcode** (Recommended)
```
[swarm_build_feed limit="10"]
```

Add this to any WordPress page/post to display the feed.

**Option B: REST API**
```
GET https://weareswarm.online/wp-json/swarm/v1/feed
```

Use this endpoint to consume the feed in custom themes or external applications.

## 📋 Complete Example

```bash
# 1. Generate feed
python tools/generate_devlog_feed.py --output runtime/feeds/public_build_feed.json

# 2. Upload feed.json to weareswarm.online via FTP
#    Location: /wp-content/themes/runtime/feeds/public_build_feed.json

# 3. Activate plugin (one-time setup)
#    - Upload swarm-build-feed.php to /wp-content/plugins/
#    - Activate in WordPress admin

# 4. Add shortcode to page
#    [swarm_build_feed limit="10"]
```

## 🔄 Regular Updates

To update the feed regularly:

```bash
# Generate new feed (overwrites existing)
python tools/generate_devlog_feed.py --output runtime/feeds/public_build_feed.json

# Upload updated feed to WordPress
# (Same as Step 2 above)
```

**Pro Tip:** Set up a cron job or scheduled task to generate the feed daily/hourly.

## 🎨 Customization

### Change Number of Items

```php
[swarm_build_feed limit="20"]  // Show 20 items instead of 10
```

### Include All Devlogs (Not Just Public Signals)

```bash
python tools/generate_devlog_feed.py --all --output runtime/feeds/public_build_feed.json
```

### Custom Feed URL

Edit `tools/generate_devlog_feed.py`:
```python
generator = DevlogFeedGenerator(feed_url="https://your-custom-url.com/feed.json")
```

## 📖 Full Documentation

See `docs/DEVELOP_FEED_INTEGRATION.md` for complete documentation.

