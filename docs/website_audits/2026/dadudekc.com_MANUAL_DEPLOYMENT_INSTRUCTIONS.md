
# Manual Deployment Instructions for dadudekc.com

## Option 1: WordPress Admin → Appearance → Theme Editor
1. Log in to WordPress admin: https://dadudekc.com/wp-admin
2. Navigate to: Appearance → Theme Editor
3. Select: functions.php (from active theme)
4. Scroll to the end of the file
5. Paste the following code:

```php
<?php
/**
 * Combined Analytics Integration (GA4 + Facebook Pixel)
 * Site: dadudekc.com
 */

function add_analytics_tracking() {
    $ga4_id = defined('GA4_MEASUREMENT_ID') ? GA4_MEASUREMENT_ID : '';
    $pixel_id = defined('FACEBOOK_PIXEL_ID') ? FACEBOOK_PIXEL_ID : '';
    
    // GA4
    if (!empty($ga4_id)) {
        ?>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($ga4_id); ?>"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '<?php echo esc_js($ga4_id); ?>');
        </script>
        <?php
    }
    
    // Facebook Pixel
    if (!empty($pixel_id)) {
        ?>
        <!-- Facebook Pixel Code -->
        <script>
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '<?php echo esc_js($pixel_id); ?>');
            fbq('track', 'PageView');
        </script>
        <noscript>
            <img height="1" width="1" style="display:none"
            src="https://www.facebook.com/tr?id=<?php echo esc_attr($pixel_id); ?>&ev=PageView&noscript=1"/>
        </noscript>
        <?php
    }
    
    // Combined event tracking
    if (!empty($ga4_id) || !empty($pixel_id)) {
        ?>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Track CTA clicks
                document.querySelectorAll('a[href*="#cta"], .cta-button, .btn-primary, [data-cta]').forEach(function(button) {
                    button.addEventListener('click', function() {
                        var label = this.textContent.trim() || this.href || this.getAttribute('data-cta');
                        <?php if (!empty($ga4_id)): ?>
                        gtag('event', 'cta_click', {
                            'event_category': 'engagement',
                            'event_label': label
                        });
                        <?php endif; ?>
                        <?php if (!empty($pixel_id)): ?>
                        fbq('track', 'Lead', { content_name: label });
                        <?php endif; ?>
                    });
                });
                
                // Track form submissions
                document.querySelectorAll('form').forEach(function(form) {
                    form.addEventListener('submit', function() {
                        var label = form.id || form.className || 'form_submission';
                        <?php if (!empty($ga4_id)): ?>
                        gtag('event', 'form_submit', {
                            'event_category': 'engagement',
                            'event_label': label
                        });
                        <?php endif; ?>
                        <?php if (!empty($pixel_id)): ?>
                        fbq('track', 'Lead', { content_name: label });
                        <?php endif; ?>
                    });
                });
            });
        </script>
        <?php
    }
}
add_action('wp_head', 'add_analytics_tracking', 10);
```

6. Click "Update File"
7. Verify: Check page source for analytics scripts

## Option 2: SFTP/File Manager
1. Connect to your hosting via SFTP or File Manager
2. Navigate to: wp-content/themes/dadudekc.com/functions.php
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
 * Combined Analytics Integration (GA4 + Facebook Pixel)
 * Site: dadudekc.com
 */

function add_analytics_tracking() {
    $ga4_id = defined('GA4_MEASUREMENT_ID') ? GA4_MEASUREMENT_ID : '';
    $pixel_id = defined('FACEBOOK_PIXEL_ID') ? FACEBOOK_PIXEL_ID : '';
    
    // GA4
    if (!empty($ga4_id)) {
        ?>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($ga4_id); ?>"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '<?php echo esc_js($ga4_id); ?>');
        </script>
        <?php
    }
    
    // Facebook Pixel
    if (!empty($pixel_id)) {
        ?>
        <!-- Facebook Pixel Code -->
        <script>
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '<?php echo esc_js($pixel_id); ?>');
            fbq('track', 'PageView');
        </script>
        <noscript>
            <img height="1" width="1" style="display:none"
            src="https://www.facebook.com/tr?id=<?php echo esc_attr($pixel_id); ?>&ev=PageView&noscript=1"/>
        </noscript>
        <?php
    }
    
    // Combined event tracking
    if (!empty($ga4_id) || !empty($pixel_id)) {
        ?>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Track CTA clicks
                document.querySelectorAll('a[href*="#cta"], .cta-button, .btn-primary, [data-cta]').forEach(function(button) {
                    button.addEventListener('click', function() {
                        var label = this.textContent.trim() || this.href || this.getAttribute('data-cta');
                        <?php if (!empty($ga4_id)): ?>
                        gtag('event', 'cta_click', {
                            'event_category': 'engagement',
                            'event_label': label
                        });
                        <?php endif; ?>
                        <?php if (!empty($pixel_id)): ?>
                        fbq('track', 'Lead', { content_name: label });
                        <?php endif; ?>
                    });
                });
                
                // Track form submissions
                document.querySelectorAll('form').forEach(function(form) {
                    form.addEventListener('submit', function() {
                        var label = form.id || form.className || 'form_submission';
                        <?php if (!empty($ga4_id)): ?>
                        gtag('event', 'form_submit', {
                            'event_category': 'engagement',
                            'event_label': label
                        });
                        <?php endif; ?>
                        <?php if (!empty($pixel_id)): ?>
                        fbq('track', 'Lead', { content_name: label });
                        <?php endif; ?>
                    });
                });
            });
        </script>
        <?php
    }
}
add_action('wp_head', 'add_analytics_tracking', 10);
```

## Configuration Required:
After deployment, add these lines to wp-config.php (before "That's all, stop editing!"):
```php
define('GA4_MEASUREMENT_ID', 'G-XXXXXXXXXX');
define('FACEBOOK_PIXEL_ID', '123456789012345');
```

Replace the IDs with your actual GA4 Measurement ID and Facebook Pixel ID.
