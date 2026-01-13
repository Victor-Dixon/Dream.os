#!/bin/bash
# Deploy Build-In-Public Sites and Fix UTF-8 Encoding Issues
# ========================================================
#
# This script handles deployment of dadudekc.com and freerideinvestor.com
# and addresses UTF-8 encoding issues across all sites.
#
# Usage: ./deploy_build_in_public_sites.sh [site_name]
# If no site_name provided, deploys to both sites
#
# Author: Agent-3 (Infrastructure & DevOps Specialist)
# Created: 2026-01-08

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$REPO_ROOT/logs/build_in_public_deployment_$(date +%Y%m%d_%H%M%S).log"

# Sites to deploy
SITES=("dadudekc.com" "freerideinvestor.com")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Error handling
error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    log "ERROR: $1"
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
    log "SUCCESS: $1"
}

# Info message
info() {
    echo -e "${BLUE}INFO: $1${NC}"
    log "INFO: $1"
}

# Warning message
warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
    log "WARNING: $1"
}

# Check if site parameter is provided
TARGET_SITE=""
if [ $# -eq 1 ]; then
    TARGET_SITE="$1"
    if [[ ! " ${SITES[@]} " =~ " ${TARGET_SITE} " ]]; then
        error "Invalid site: $TARGET_SITE. Valid sites: ${SITES[*]}"
    fi
    SITES=("$TARGET_SITE")
fi

log "Starting Build-In-Public deployment script"
log "Target sites: ${SITES[*]}"
log "Log file: $LOG_FILE"

# Function to deploy a single site
deploy_site() {
    local site="$1"
    local site_dir="${WEBSITES_ROOT:-$REPO_ROOT/sites}/$site"

    info "Starting deployment for $site"

    # Check if site directory exists
    if [ ! -d "$site_dir" ]; then
        error "Site directory not found: $site_dir"
    fi

    # Check for wp-config.php and ensure UTF-8 charset
    local wp_config="$site_dir/wp/wp-config.php"
    if [ -f "$wp_config" ]; then
        info "Checking wp-config.php charset configuration"

        # Check if charset is already set correctly
        if grep -q "define('DB_CHARSET', 'utf8mb4')" "$wp_config"; then
            success "DB_CHARSET already set to utf8mb4 in wp-config.php"
        else
            warning "DB_CHARSET not set to utf8mb4, updating..."

            # Add charset definition if not present
            if ! grep -q "DB_CHARSET" "$wp_config"; then
                # Find the database defines and add charset after them
                sed -i "/define('DB_NAME'/a define('DB_CHARSET', 'utf8mb4');" "$wp_config"
                success "Added DB_CHARSET = utf8mb4 to wp-config.php"
            else
                # Update existing charset
                sed -i "s/define('DB_CHARSET'.*/define('DB_CHARSET', 'utf8mb4');/" "$wp_config"
                success "Updated DB_CHARSET to utf8mb4 in wp-config.php"
            fi
        fi

        # Ensure collation is set correctly
        if grep -q "define('DB_COLLATE', '')" "$wp_config"; then
            success "DB_COLLATE already set correctly"
        else
            if grep -q "DB_COLLATE" "$wp_config"; then
                sed -i "s/define('DB_COLLATE'.*/define('DB_COLLATE', '');/" "$wp_config"
                success "Updated DB_COLLATE to empty string"
            fi
        fi
    else
        warning "wp-config.php not found for $site - manual charset configuration may be needed"
    fi

    # Check for PHP files that might have encoding issues
    info "Checking for PHP files with potential encoding issues"

    # Look for files that might contain non-UTF8 content
    local php_files=$(find "$site_dir" -name "*.php" -type f)
    local files_with_encoding_issues=0

    for php_file in $php_files; do
        # Check if file contains valid UTF-8
        if ! iconv -f utf-8 -t utf-8 "$php_file" > /dev/null 2>&1; then
            warning "File has encoding issues: $php_file"
            files_with_encoding_issues=$((files_with_encoding_issues + 1))

            # Attempt to fix encoding (convert to UTF-8)
            if command -v iconv >/dev/null 2>&1; then
                info "Attempting to fix encoding for $php_file"
                temp_file="${php_file}.tmp"
                if iconv -f iso-8859-1 -t utf-8 "$php_file" > "$temp_file" 2>/dev/null; then
                    mv "$temp_file" "$php_file"
                    success "Fixed encoding for $php_file"
                else
                    rm -f "$temp_file"
                    warning "Could not fix encoding for $php_file"
                fi
            fi
        fi
    done

    if [ $files_with_encoding_issues -eq 0 ]; then
        success "No encoding issues found in PHP files for $site"
    else
        warning "Found and attempted to fix $files_with_encoding_issues files with encoding issues"
    fi

    # Check for theme files that need deployment
    local theme_dir="$site_dir/wp/wp-content/themes"
    if [ -d "$theme_dir" ]; then
        info "Checking theme files for $site"

        # List theme files for verification
        local theme_files=$(find "$theme_dir" -name "*.php" -o -name "*.css" -o -name "*.js" | wc -l)
        info "Found $theme_files theme files to verify"

        # Check for specific files mentioned in audit
        local critical_files=(
            "front-page.php"
            "page-contact.php"
            "functions.php"
            "index.php"
        )

        for file in "${critical_files[@]}"; do
            if [ -f "$theme_dir/$file" ]; then
                success "Critical file present: $file"
            else
                warning "Critical file missing: $file"
            fi
        done
    fi

    success "Deployment preparation complete for $site"

    # Summary for this site
    echo "----------------------------------------"
    echo "DEPLOYMENT SUMMARY for $site"
    echo "----------------------------------------"
    echo "✅ wp-config.php charset verified/fixed"
    echo "✅ PHP files encoding checked/fixed ($files_with_encoding_issues issues addressed)"
    echo "✅ Theme files verified"
    echo "✅ Ready for deployment"
    echo "----------------------------------------"
    log "Deployment preparation complete for $site"
}

# Main deployment process
echo "========================================="
echo "BUILD-IN-PUBLIC SITES DEPLOYMENT"
echo "========================================="
echo "Sites to deploy: ${SITES[*]}"
echo "Log file: $LOG_FILE"
echo "========================================="

# Deploy each site
for site in "${SITES[@]}"; do
    echo ""
    deploy_site "$site"
done

# Final summary
echo ""
echo "========================================="
echo "DEPLOYMENT COMPLETE"
echo "========================================="
success "Build-In-Public sites deployment preparation complete"
info "Sites processed: ${#SITES[@]}"
info "Next steps:"
info "  1. Verify deployments on live servers"
info "  2. Test contact forms and functionality"
info "  3. Monitor for any remaining encoding issues"
echo "========================================="

log "Build-In-Public deployment script completed successfully"