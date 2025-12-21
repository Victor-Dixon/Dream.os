<?php
/**
 * Houston Sip Queen SEO Optimization
 * Applied: 2025-12-19
 */

if (!defined('ABSPATH')) {
    exit;
}

function hsq_seo_head() {
    ?>
<!-- Houston Sip Queen SEO Optimization -->
<!-- Generated: 2025-12-19 by Agent-7 -->

<!-- Primary Meta Tags -->
<meta name="title" content="Houston Sip Queen - Luxury Mobile Bartending Services | Houston, TX">
<meta name="description" content="Professional mobile bartending services in Houston, TX. Luxury bar service for weddings, corporate events, private parties, and special occasions. Request a quote today!">
<meta name="keywords" content="mobile bartending Houston, wedding bartender Houston, corporate event bartending, luxury bar service Houston, private party bartender, craft cocktails Houston, event bartending services">
<meta name="author" content="Houston Sip Queen">
<meta name="robots" content="index, follow">
<meta name="language" content="English">
<meta name="revisit-after" content="7 days">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Houston">
<meta name="geo.position" content="29.7604;-95.3698">
<meta name="ICBM" content="29.7604, -95.3698">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://houstonsipqueen.com/">
<meta property="og:title" content="Houston Sip Queen - Luxury Mobile Bartending Services | Houston, TX">
<meta property="og:description" content="Professional mobile bartending services in Houston, TX. Luxury bar service for weddings, corporate events, private parties, and special occasions.">
<meta property="og:image" content="https://houstonsipqueen.com/wp-content/uploads/hsq-og-image.jpg">
<meta property="og:site_name" content="Houston Sip Queen">
<meta property="og:locale" content="en_US">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://houstonsipqueen.com/">
<meta property="twitter:title" content="Houston Sip Queen - Luxury Mobile Bartending Services">
<meta property="twitter:description" content="Professional mobile bartending services in Houston, TX. Luxury bar service for weddings, corporate events, and private parties.">
<meta property="twitter:image" content="https://houstonsipqueen.com/wp-content/uploads/hsq-twitter-image.jpg">

<!-- Schema.org Structured Data - Local Business -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Houston Sip Queen",
  "image": "https://houstonsipqueen.com/wp-content/uploads/hsq-logo.jpg",
  "@id": "https://houstonsipqueen.com",
  "url": "https://houstonsipqueen.com",
  "telephone": "+1-713-XXX-XXXX",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Houston, TX",
    "addressLocality": "Houston",
    "addressRegion": "TX",
    "postalCode": "77000",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 29.7604,
    "longitude": -95.3698
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday"
    ],
    "opens": "09:00",
    "closes": "23:00"
  },
  "sameAs": [
    "https://www.facebook.com/houstonsipqueen",
    "https://www.instagram.com/houstonsipqueen"
  ],
  "description": "Luxury mobile bartending services in Houston, TX. Professional bar service for weddings, corporate events, private parties, and special occasions.",
  "areaServed": {
    "@type": "City",
    "name": "Houston"
  },
  "serviceType": "Mobile Bartending Services"
}
</script>

<!-- Canonical URL -->
<link rel="canonical" href="https://houstonsipqueen.com/">

    <?php
}
add_action('wp_head', 'hsq_seo_head', 1);
