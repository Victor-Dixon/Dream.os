<?php
/**
 * FreeRide Investor SEO Optimization
 * Applied: 2025-12-19
 */

if (!defined('ABSPATH')) {
    exit;
}

function freerideinvestor_com_seo_head() {
    ?>
<!-- FreeRide Investor SEO Optimization -->
<!-- Generated: 2025-12-19 by Agent-7 -->

<!-- Primary Meta Tags -->
<meta name="title" content="FreeRide Investor - Trading education and investment strategies">
<meta name="description" content="Trading education and investment strategies. trading">
<meta name="keywords" content="trading, investing, stock market, trading education, investment strategies">
<meta name="author" content="FreeRide Investor">
<meta name="robots" content="index, follow">
<meta name="language" content="English">
<meta name="revisit-after" content="7 days">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://freerideinvestor.com/">
<meta property="og:title" content="FreeRide Investor - Trading education and investment strategies">
<meta property="og:description" content="Trading education and investment strategies. trading">
<meta property="og:image" content="https://freerideinvestor.com/wp-content/uploads/og-image.jpg">
<meta property="og:site_name" content="FreeRide Investor">
<meta property="og:locale" content="en_US">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://freerideinvestor.com/">
<meta property="twitter:title" content="FreeRide Investor">
<meta property="twitter:description" content="Trading education and investment strategies. trading">
<meta property="twitter:image" content="https://freerideinvestor.com/wp-content/uploads/twitter-image.jpg">

<!-- Schema.org Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "FreeRide Investor",
  "url": "https://freerideinvestor.com",
  "description": "Trading education and investment strategies"

}
</script>

<!-- Canonical URL -->
<link rel="canonical" href="https://freerideinvestor.com/">
    <?php
}
add_action('wp_head', 'freerideinvestor_com_seo_head', 1);
