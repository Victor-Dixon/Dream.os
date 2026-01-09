#!/bin/bash
# Deploy FreeRideInvestor theme to live WordPress site

echo "🚀 FreeRideInvestor Theme Deployment"
echo "===================================="

# Configuration - MODIFY THESE PATHS
LIVE_WP_PATH="/var/www/freerideinvestor.com"  # Path to live WordPress installation
BACKUP_SUFFIX="_backup_$(date +%Y%m%d_%H%M%S)"

echo "Live WordPress path: $LIVE_WP_PATH"

# Backup existing theme
if [ -d "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2" ]; then
    echo "📦 Backing up existing theme..."
    mv "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2" "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2$BACKUP_SUFFIX"
    echo "✅ Backup created: freerideinvestor-v2$BACKUP_SUFFIX"
fi

# Copy new theme
echo "📋 Deploying new theme..."
cp -r freerideinvestor-v2 "$LIVE_WP_PATH/wp-content/themes/"
echo "✅ Theme deployed"

# Set permissions
echo "🔧 Setting permissions..."
find "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2" -type f -exec chmod 644 {} \;
find "$LIVE_WP_PATH/wp-content/themes/freerideinvestor-v2" -type d -exec chmod 755 {} \;

echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Activate theme in WordPress admin"
echo "2. Run menu setup script or follow manual setup"
echo "3. Test menu navigation"
echo "4. Remove backup if everything works"
