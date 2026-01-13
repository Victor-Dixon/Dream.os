<?php

/**
 * Test Business Plan Plugin Output
 * 
 * This file can be accessed directly to test if the plugin is working.
 * Upload to WordPress root and access via: yoursite.com/test_plugin_output.php
 * 
 * WARNING: Remove this file after testing for security!
 */

// Load WordPress
require_once('wp-load.php');

// Check if plugin class exists
if (!class_exists('Crosby_Business_Plan')) {
    die('<h1>Plugin Not Active</h1><p>The Crosby Business Plan plugin is not active. Please activate it in WordPress Admin → Plugins.</p>');
}

// Test shortcode
echo '<h1>Business Plan Plugin Test</h1>';
echo '<p>If you see the business plan content below, the plugin is working correctly.</p>';
echo '<hr>';

// Test full business plan
echo '<h2>Full Business Plan:</h2>';
echo do_shortcode('[crosby_business_plan]');

echo '<hr>';
echo '<p><strong>Test completed.</strong> If you see content above, the plugin is working. You can now remove this test file.</p>';
