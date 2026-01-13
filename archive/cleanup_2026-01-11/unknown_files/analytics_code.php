/**
 * Add Google Analytics 4 and Facebook Pixel tracking codes
 * Generated for FreeRide Investor deployment
 */
function add_analytics_tracking_codes() {
    // Google Analytics 4 (GA4)
    if (defined('GA4_MEASUREMENT_ID') && GA4_MEASUREMENT_ID) {
        echo '<!-- Google Analytics 4 (GA4) -->\n';
        echo '<script async src="https://www.googletagmanager.com/gtag/js?id=' . GA4_MEASUREMENT_ID . '"></script>\n';
        echo '<script>\n';
        echo 'window.dataLayer = window.dataLayer || [];\n';
        echo 'function gtag(){dataLayer.push(arguments);}\n';
        echo 'gtag(\'js\', new Date());\n';
        echo 'gtag(\'config\', \'' . GA4_MEASUREMENT_ID . '\', {\n';
        echo '\'page_path\': window.location.pathname,\n';
        echo '\'page_title\': document.title,\n';
        echo '});\n';
        echo '// Custom Events Tracking\n';
        echo '// Track contact form submissions\n';
        echo 'gtag("event", "contact_form_submit", {\n';
        echo '"event_category": "engagement",\n';
        echo '"event_label": "contact_form_submit"\n';
        echo '});\n';
        echo '</script>\n';
        echo '<!-- End GA4 -->\n';
    }

    // Facebook Pixel
    if (defined('FACEBOOK_PIXEL_ID') && FACEBOOK_PIXEL_ID) {
        echo '<!-- Facebook Pixel Code -->\n';
        echo '<script>\n';
        echo '!function(f,b,e,v,n,t,s)\n';
        echo '{if(f.fbq)return;n=f.fbq=function(){n.callMethod?\n';
        echo 'n.callMethod.apply(n,arguments):n.queue.push(arguments)};\n';
        echo 'if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version=\'2.0\';\n';
        echo 'n.queue=[];t=b.createElement(e);t.async=!0;\n';
        echo 't.src=v;s=b.getElementsByTagName(e)[0];\n';
        echo 's.parentNode.insertBefore(t,s)}(window, document,\'script\',\n';
        echo '\'https://connect.facebook.net/en_US/fbevents.js\');\n';
        echo 'fbq(\'init\', \'' . FACEBOOK_PIXEL_ID . '\');\n';
        echo 'fbq(\'track\', \'PageView\');\n';
        echo '</script>\n';
        echo '<noscript>\n';
        echo '<img height="1" width="1" style="display:none"\n';
        echo 'src="https://www.facebook.com/tr?id=' . FACEBOOK_PIXEL_ID . '&ev=PageView&noscript=1"/>\n';
        echo '</noscript>\n';
        echo '<!-- End Facebook Pixel Code -->\n';
    }
}
add_action('wp_head', 'add_analytics_tracking_codes', 99);