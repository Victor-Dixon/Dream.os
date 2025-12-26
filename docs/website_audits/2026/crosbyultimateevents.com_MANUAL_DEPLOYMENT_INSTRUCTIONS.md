
# Manual Deployment Instructions for crosbyultimateevents.com

## Option 1: WordPress Admin → Appearance → Theme Editor
1. Log in to WordPress admin: https://crosbyultimateevents.com/wp-admin
2. Navigate to: Appearance → Theme Editor
3. Select: functions.php (from active theme)
4. Scroll to the end of the file
5. Paste the following code:

```php
<?php
/**
 * GA4 Analytics Integration
 * Site: crosbyultimateevents.com
 * GA4 Measurement ID: {GA4_MEASUREMENT_ID}
 */

function add_ga4_analytics() {
    $ga4_id = '{GA4_MEASUREMENT_ID}'; // Replace with actual GA4 Measurement ID
    
    if (empty($ga4_id) || $ga4_id === '{GA4_MEASUREMENT_ID}') {
        return; // Don't output if ID not configured
    }
    ?>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($ga4_id); ?>"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '<?php echo esc_js($ga4_id); ?>');
        
        // Track CTA clicks
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('a[href*="#cta"], .cta-button, .btn-primary').forEach(function(button) {
                button.addEventListener('click', function() {
                    gtag('event', 'cta_click', {
                        'event_category': 'engagement',
                        'event_label': this.textContent.trim() || this.href
                    });
                });
            });
            
            // Track form submissions
            document.querySelectorAll('form').forEach(function(form) {
                form.addEventListener('submit', function() {
                    gtag('event', 'form_submit', {
                        'event_category': 'engagement',
                        'event_label': form.id || form.className
                    });
                });
            });
        });
    </script>
    <?php
}
add_action('wp_head', 'add_ga4_analytics', 10);
```

6. Click "Update File"
7. Verify: Check page source for analytics scripts

## Option 2: SFTP/File Manager
1. Connect to your hosting via SFTP or File Manager
2. Navigate to: wp-content/themes/crosbyultimateevents.com/functions.php
3. Download functions.php (backup first!)
4. Open in text editor
5. Paste the analytics code at the end (before closing ?> if present)
6. Upload the modified functions.php
7. Verify: Check page source for analytics scripts

## Option 3: Hosting Control Panel File Manager
1. Log in to hosting control panel (cPanel, etc.)
2. Open File Manager
3. Navigate to: public_html/wp-content/themes/[ACTIVE_THEME]/functions.php
4. Edit the file
5. Paste analytics code at the end
6. Save and verify

## Analytics Code to Deploy:
```php
<?php
/**
 * GA4 Analytics Integration
 * Site: crosbyultimateevents.com
 * GA4 Measurement ID: {GA4_MEASUREMENT_ID}
 */

function add_ga4_analytics() {
    $ga4_id = '{GA4_MEASUREMENT_ID}'; // Replace with actual GA4 Measurement ID
    
    if (empty($ga4_id) || $ga4_id === '{GA4_MEASUREMENT_ID}') {
        return; // Don't output if ID not configured
    }
    ?>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($ga4_id); ?>"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '<?php echo esc_js($ga4_id); ?>');
        
        // Track CTA clicks
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('a[href*="#cta"], .cta-button, .btn-primary').forEach(function(button) {
                button.addEventListener('click', function() {
                    gtag('event', 'cta_click', {
                        'event_category': 'engagement',
                        'event_label': this.textContent.trim() || this.href
                    });
                });
            });
            
            // Track form submissions
            document.querySelectorAll('form').forEach(function(form) {
                form.addEventListener('submit', function() {
                    gtag('event', 'form_submit', {
                        'event_category': 'engagement',
                        'event_label': form.id || form.className
                    });
                });
            });
        });
    </script>
    <?php
}
add_action('wp_head', 'add_ga4_analytics', 10);
```

## Configuration Required:
After deployment, add these lines to wp-config.php (before "That's all, stop editing!"):
```php
define('GA4_MEASUREMENT_ID', 'G-XXXXXXXXXX');
define('FACEBOOK_PIXEL_ID', '123456789012345');
```

Replace the IDs with your actual GA4 Measurement ID and Facebook Pixel ID.
