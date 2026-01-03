<?php
/**
 * Debug script to test plugin functionality
 * Upload this to wp-content/plugins/crosby-business-plan/debug.php
 * Then access: https://crosbyultimateevents.com/wp-content/plugins/crosby-business-plan/debug.php
 */

// Load WordPress
require_once('../../../wp-load.php');

// Check if plugin is loaded
echo "<h1>Plugin Debug Test</h1>";

// Check if class exists
if (class_exists('Crosby_Business_Plan')) {
    echo "<p style='color:green'>✅ Crosby_Business_Plan class exists</p>";
} else {
    echo "<p style='color:red'>❌ Crosby_Business_Plan class NOT found</p>";
}

// Check if shortcode is registered
if (shortcode_exists('crosby_business_plan')) {
    echo "<p style='color:green'>✅ Shortcode 'crosby_business_plan' is registered</p>";
} else {
    echo "<p style='color:red'>❌ Shortcode 'crosby_business_plan' NOT registered</p>";
}

// Check plugin constants
echo "<h2>Plugin Constants:</h2>";
echo "<p>CROSBY_BP_PLUGIN_DIR: " . (defined('CROSBY_BP_PLUGIN_DIR') ? CROSBY_BP_PLUGIN_DIR : 'NOT DEFINED') . "</p>";
echo "<p>CROSBY_BP_PLUGIN_URL: " . (defined('CROSBY_BP_PLUGIN_URL') ? CROSBY_BP_PLUGIN_URL : 'NOT DEFINED') . "</p>";

// Check if template file exists
$template_file = plugin_dir_path(__FILE__) . 'templates/business-plan-display.php';
echo "<h2>Template File:</h2>";
echo "<p>Expected path: " . $template_file . "</p>";
echo "<p>File exists: " . (file_exists($template_file) ? 'YES ✅' : 'NO ❌') . "</p>";

// Try to execute shortcode directly
echo "<h2>Shortcode Test:</h2>";
try {
    $output = do_shortcode('[crosby_business_plan]');
    if (!empty($output)) {
        echo "<p style='color:green'>✅ Shortcode executed successfully</p>";
        echo "<p>Output length: " . strlen($output) . " characters</p>";
        echo "<div style='border:1px solid #ccc; padding:10px; margin:10px 0;'>";
        echo substr($output, 0, 500) . "...";
        echo "</div>";
    } else {
        echo "<p style='color:red'>❌ Shortcode executed but returned empty output</p>";
    }
} catch (Exception $e) {
    echo "<p style='color:red'>❌ Error executing shortcode: " . $e->getMessage() . "</p>";
}

// Check for PHP errors
echo "<h2>PHP Errors:</h2>";
$errors = error_get_last();
if ($errors) {
    echo "<pre style='color:red'>";
    print_r($errors);
    echo "</pre>";
} else {
    echo "<p style='color:green'>✅ No PHP errors detected</p>";
}

// List all registered shortcodes
echo "<h2>All Registered Shortcodes:</h2>";
global $shortcode_tags;
echo "<pre>";
foreach ($shortcode_tags as $tag => $callback) {
    if (strpos($tag, 'crosby') !== false || strpos($tag, 'business') !== false) {
        echo "✅ $tag\n";
    }
}
echo "</pre>";

