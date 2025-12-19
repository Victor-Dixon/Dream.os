<?php
/**
 * Southwest Secret SEO Optimization
 * Applied: 2025-12-19
 */

if (!defined('ABSPATH')) {
    exit;
}

function southwestsecret_com_seo_head() {
    ?>
<!-- Southwest Secret SEO Optimization -->
<!-- Generated: 2025-12-19 by Agent-7 -->

<!-- Primary Meta Tags -->
<meta name="title" content="Southwest Secret - Music releases, DJ mixes, and events">
<meta name="description" content="Music releases, DJ mixes, and events. music">
<meta name="keywords" content="music, DJ, mixes, releases, electronic music, events">
<meta name="author" content="Southwest Secret">
<meta name="robots" content="index, follow">
<meta name="language" content="English">
<meta name="revisit-after" content="7 days">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://southwestsecret.com/">
<meta property="og:title" content="Southwest Secret - Music releases, DJ mixes, and events">
<meta property="og:description" content="Music releases, DJ mixes, and events. music">
<meta property="og:image" content="https://southwestsecret.com/wp-content/uploads/og-image.jpg">
<meta property="og:site_name" content="Southwest Secret">
<meta property="og:locale" content="en_US">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://southwestsecret.com/">
<meta property="twitter:title" content="Southwest Secret">
<meta property="twitter:description" content="Music releases, DJ mixes, and events. music">
<meta property="twitter:image" content="https://southwestsecret.com/wp-content/uploads/twitter-image.jpg">

<!-- Schema.org Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Southwest Secret",
  "url": "https://southwestsecret.com",
  "description": "Music releases, DJ mixes, and events"

}
</script>

<!-- Canonical URL -->
<link rel="canonical" href="https://southwestsecret.com/">
    <?php
}
add_action('wp_head', 'southwestsecret_com_seo_head', 1);
