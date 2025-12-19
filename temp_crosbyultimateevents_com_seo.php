<?php
/**
 * Crosby Ultimate Events SEO Optimization
 * Applied: 2025-12-19
 */

if (!defined('ABSPATH')) {
    exit;
}

function crosbyultimateevents_com_seo_head() {
    ?>
<!-- Crosby Ultimate Events SEO Optimization -->
<!-- Generated: 2025-12-19 by Agent-7 -->

<!-- Primary Meta Tags -->
<meta name="title" content="Crosby Ultimate Events - Professional event planning and coordination services">
<meta name="description" content="Professional event planning and coordination services in Houston, TX. event planning">
<meta name="keywords" content="event planning, weddings, corporate events, party planning, event coordination">
<meta name="author" content="Crosby Ultimate Events">
<meta name="robots" content="index, follow">
<meta name="language" content="English">
<meta name="revisit-after" content="7 days">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Houston, TX">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://crosbyultimateevents.com/">
<meta property="og:title" content="Crosby Ultimate Events - Professional event planning and coordination services">
<meta property="og:description" content="Professional event planning and coordination services in Houston, TX. event planning">
<meta property="og:image" content="https://crosbyultimateevents.com/wp-content/uploads/og-image.jpg">
<meta property="og:site_name" content="Crosby Ultimate Events">
<meta property="og:locale" content="en_US">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://crosbyultimateevents.com/">
<meta property="twitter:title" content="Crosby Ultimate Events">
<meta property="twitter:description" content="Professional event planning and coordination services in Houston, TX. event planning">
<meta property="twitter:image" content="https://crosbyultimateevents.com/wp-content/uploads/twitter-image.jpg">

<!-- Schema.org Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Crosby Ultimate Events",
  "url": "https://crosbyultimateevents.com",
  "description": "Professional event planning and coordination services"
,
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Houston, TX",
    "addressRegion": "TX",
    "addressCountry": "US"
  }
}
</script>

<!-- Canonical URL -->
<link rel="canonical" href="https://crosbyultimateevents.com/">
    <?php
}
add_action('wp_head', 'crosbyultimateevents_com_seo_head', 1);
