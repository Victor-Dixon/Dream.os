<?php
/**
 * Prism Blossom SEO Optimization
 * Applied: 2025-12-19
 */

if (!defined('ABSPATH')) {
    exit;
}

function prismblossom_online_seo_head() {
    ?>
<!-- Prism Blossom SEO Optimization -->
<!-- Generated: 2025-12-19 by Agent-7 -->

<!-- Primary Meta Tags -->
<meta name="title" content="Prism Blossom - Personal blog and creative writing">
<meta name="description" content="Personal blog and creative writing. blog">
<meta name="keywords" content="blog, writing, creative, personal, stories">
<meta name="author" content="Prism Blossom">
<meta name="robots" content="index, follow">
<meta name="language" content="English">
<meta name="revisit-after" content="7 days">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://prismblossom.online/">
<meta property="og:title" content="Prism Blossom - Personal blog and creative writing">
<meta property="og:description" content="Personal blog and creative writing. blog">
<meta property="og:image" content="https://prismblossom.online/wp-content/uploads/og-image.jpg">
<meta property="og:site_name" content="Prism Blossom">
<meta property="og:locale" content="en_US">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://prismblossom.online/">
<meta property="twitter:title" content="Prism Blossom">
<meta property="twitter:description" content="Personal blog and creative writing. blog">
<meta property="twitter:image" content="https://prismblossom.online/wp-content/uploads/twitter-image.jpg">

<!-- Schema.org Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Prism Blossom",
  "url": "https://prismblossom.online",
  "description": "Personal blog and creative writing"

}
</script>

<!-- Canonical URL -->
<link rel="canonical" href="https://prismblossom.online/">
    <?php
}
add_action('wp_head', 'prismblossom_online_seo_head', 1);
