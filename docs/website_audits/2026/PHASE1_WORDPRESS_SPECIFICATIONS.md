# Phase 1: Brand Core WordPress Implementation Specifications

**Author:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-12-25  
**Status:** READY FOR IMPLEMENTATION  
**Implementation:** Agent-7 (Web Development Specialist)

<!-- SSOT Domain: web -->

## Executive Summary

This document provides detailed WordPress implementation specifications for Phase 1 Brand Core fixes across all 4 revenue engine websites. The architecture has been validated and approved for implementation.

**Phase 1 Scope:**
- Positioning Statements (BRAND-01)
- Offer Ladders (BRAND-02)
- ICP Definitions (BRAND-03)

**Sites:** freerideinvestor.com, tradingrobotplug.com, dadudekc.com, crosbyultimateevents.com

---

## WordPress Custom Post Types Specification

### 1. Positioning Statements Custom Post Type

**Post Type Name:** `positioning_statement`  
**Slug:** `positioning-statements`  
**Public:** No (admin only)  
**Show in REST API:** Yes

**Custom Fields (ACF or Meta Box):**
- `target_audience` (text) - "For [target audience]"
- `pain_points` (textarea) - List of pain points
- `unique_value` (textarea) - What we provide
- `differentiation` (textarea) - Unlike competitors because...
- `site_assignment` (select) - freerideinvestor.com, tradingrobotplug.com, dadudekc.com, crosbyultimateevents.com

**Template Structure:**
```
For [target_audience] who [pain_points], 
we provide [unique_value] 
(unlike [competitors] because [differentiation])
```

**Usage:**
- Display on homepage hero section
- Display in About page
- Use in meta descriptions
- Reference in email sequences

### 2. Offer Ladder Custom Post Type

**Post Type Name:** `offer_ladder`  
**Slug:** `offer-ladders`  
**Public:** No (admin only)  
**Show in REST API:** Yes  
**Hierarchical:** Yes (parent/child for ladder progression)

**Custom Fields (ACF or Meta Box):**
- `ladder_level` (number) - 1, 2, 3, 4, 5 (progression order)
- `offer_name` (text) - Name of offer
- `offer_description` (textarea) - What the offer includes
- `price_point` (text) - Free, $X, or price range
- `cta_text` (text) - Call-to-action button text
- `cta_url` (url) - Link to offer landing page
- `parent_offer` (relationship) - Link to previous level offer
- `site_assignment` (select) - Site this ladder belongs to

**Template Structure:**
```
Level 1: [offer_name] - [price_point]
  Description: [offer_description]
  CTA: [cta_text] → [cta_url]

Level 2: [offer_name] - [price_point]
  Description: [offer_description]
  CTA: [cta_text] → [cta_url]
  ...
```

**Usage:**
- Display on homepage (visual ladder component)
- Display in pricing/services page
- Reference in email sequences
- Use in conversion funnels

### 3. ICP Definitions Custom Post Type

**Post Type Name:** `icp_definition`  
**Slug:** `icp-definitions`  
**Public:** No (admin only)  
**Show in REST API:** Yes

**Custom Fields (ACF or Meta Box):**
- `target_demographic` (text) - Who they are (age, income, role)
- `pain_points` (textarea) - What problems they face
- `desired_outcomes` (textarea) - What they want to achieve
- `site_assignment` (select) - Site this ICP belongs to

**Template Structure:**
```
For [target_demographic] who [pain_points],
we eliminate [problems].
Your outcome: [desired_outcomes]
```

**Usage:**
- Display on homepage (ICP section)
- Display in About page
- Reference in email sequences
- Use in ad targeting

---

## WordPress Component Templates

### Positioning Statement Component

**File:** `template-parts/components/positioning-statement.php`

```php
<?php
/**
 * Positioning Statement Component
 * Displays positioning statement from Custom Post Type
 */
$site = get_site_url();
$positioning = get_posts([
    'post_type' => 'positioning_statement',
    'meta_key' => 'site_assignment',
    'meta_value' => $site,
    'posts_per_page' => 1
]);

if ($positioning) {
    $post = $positioning[0];
    $target = get_field('target_audience', $post->ID);
    $pain = get_field('pain_points', $post->ID);
    $value = get_field('unique_value', $post->ID);
    $diff = get_field('differentiation', $post->ID);
    ?>
    <div class="positioning-statement">
        <p class="positioning-text">
            For <strong><?php echo esc_html($target); ?></strong> 
            who <?php echo esc_html($pain); ?>, 
            we provide <?php echo esc_html($value); ?> 
            (unlike <?php echo esc_html($diff); ?> because...)
        </p>
    </div>
    <?php
}
?>
```

### Offer Ladder Component

**File:** `template-parts/components/offer-ladder.php`

```php
<?php
/**
 * Offer Ladder Component
 * Displays hierarchical offer ladder from Custom Post Type
 */
$site = get_site_url();
$ladder = get_posts([
    'post_type' => 'offer_ladder',
    'meta_key' => 'site_assignment',
    'meta_value' => $site,
    'orderby' => 'meta_value_num',
    'meta_key' => 'ladder_level',
    'order' => 'ASC'
]);

if ($ladder) {
    ?>
    <div class="offer-ladder">
        <?php foreach ($ladder as $offer): ?>
            <div class="offer-level" data-level="<?php echo get_field('ladder_level', $offer->ID); ?>">
                <h3><?php echo esc_html(get_field('offer_name', $offer->ID)); ?></h3>
                <p class="price"><?php echo esc_html(get_field('price_point', $offer->ID)); ?></p>
                <p class="description"><?php echo esc_html(get_field('offer_description', $offer->ID)); ?></p>
                <a href="<?php echo esc_url(get_field('cta_url', $offer->ID)); ?>" class="cta-button">
                    <?php echo esc_html(get_field('cta_text', $offer->ID)); ?>
                </a>
            </div>
        <?php endforeach; ?>
    </div>
    <?php
}
?>
```

### ICP Definition Component

**File:** `template-parts/components/icp-definition.php`

```php
<?php
/**
 * ICP Definition Component
 * Displays ICP definition from Custom Post Type
 */
$site = get_site_url();
$icp = get_posts([
    'post_type' => 'icp_definition',
    'meta_key' => 'site_assignment',
    'meta_value' => $site,
    'posts_per_page' => 1
]);

if ($icp) {
    $post = $icp[0];
    $demographic = get_field('target_demographic', $post->ID);
    $pain = get_field('pain_points', $post->ID);
    $outcomes = get_field('desired_outcomes', $post->ID);
    ?>
    <div class="icp-definition">
        <h2>Ideal Customer Profile</h2>
        <p class="icp-text">
            For <strong><?php echo esc_html($demographic); ?></strong> 
            who <?php echo esc_html($pain); ?>, 
            we eliminate workflow bottlenecks.
        </p>
        <p class="outcome-text">
            Your outcome: <?php echo esc_html($outcomes); ?>
        </p>
    </div>
    <?php
}
?>
```

---

## Site-Specific Content Specifications

### freerideinvestor.com

**Positioning Statement:**
- Target: Traders and investors tired of generic advice
- Pain: Generic advice, theory-heavy courses, signal services
- Value: Actionable TBOW tactics and proven strategies
- Differentiation: Focus on practical, tested methods that work in real markets

**Offer Ladder:**
1. Free TBOW tactics (blog)
2. Free resources (roadmap PDF, mindset journal)
3. Newsletter subscription
4. Premium membership (courses, strategies, cheat sheets)
5. Advanced coaching/community

**ICP:**
- Demographic: Active traders (day/swing traders, $10K-$500K accounts)
- Pain: Inconsistent results, guesswork
- Outcome: Consistent edge, reduced losses, trading confidence

### tradingrobotplug.com

**Positioning Statement:**
- Target: Traders seeking validated trading robots
- Pain: Unproven trading systems, lack of validation
- Value: Paper-trading validated robots
- Differentiation: Validation-first approach, transparency

**Offer Ladder:**
1. Trading Robot Validation Checklist (PDF) or waitlist
2. Development updates newsletter
3. Early access waitlist
4. Trading robot subscription (future)
5. Advanced robot configurations (future)

**ICP:**
- Demographic: Traders looking for automated solutions
- Pain: Unproven systems, lack of validation
- Outcome: Validated trading robots, proven performance

### dadudekc.com

**Positioning Statement:**
- Target: Service business owners drowning in manual workflows
- Value: Done-for-you automation sprints
- Differentiation: Deliver working automations in 2 weeks with zero technical knowledge required

**Offer Ladder:**
1. Free workflow audit (/audit)
2. Automation scoreboard (/scoreboard)
3. Discovery call/intake (/intake)
4. 2-Week Sprint ($X,XXX)
5. Ongoing automation retainer ($X,XXX/month)

**ICP:**
- Demographic: Service business owners ($50K-$500K revenue)
- Pain: Manual tasks, workflow bottlenecks
- Outcome: 10+ hours/week back, scalable operations, peace of mind

### crosbyultimateevents.com

**Positioning Statement:**
- Target: Affluent professionals/corporate clients
- Pain: Event planning stress, time constraints
- Value: Premium private dining and event experiences
- Differentiation: Personalized service, attention to detail

**Offer Ladder:**
1. Free consultation/event planning guide (lead magnet)
2. Intimate Dining ($800-$1,500)
3. Celebration Package ($3,000-$8,000)
4. Full Event Planning ($10,000+)
5. Corporate Event Services (custom pricing)

**ICP:**
- Demographic: Busy professionals ($150K+ income, 35-65)
- Pain: Event planning stress, time constraints
- Outcome: Unforgettable events without the stress

---

## Implementation Checklist

### Step 1: Create Custom Post Types
- [ ] Register `positioning_statement` post type
- [ ] Register `offer_ladder` post type (hierarchical)
- [ ] Register `icp_definition` post type
- [ ] Enable REST API for all post types

### Step 2: Create Custom Fields
- [ ] Set up ACF or Meta Box fields for positioning statements
- [ ] Set up ACF or Meta Box fields for offer ladders
- [ ] Set up ACF or Meta Box fields for ICP definitions
- [ ] Add site_assignment field to all post types

### Step 3: Create Component Templates
- [ ] Create `positioning-statement.php` component
- [ ] Create `offer-ladder.php` component
- [ ] Create `icp-definition.php` component
- [ ] Add CSS styling for components

### Step 4: Add Content
- [ ] Create positioning statements for all 4 sites
- [ ] Create offer ladders for all 4 sites
- [ ] Create ICP definitions for all 4 sites
- [ ] Assign content to correct sites via site_assignment field

### Step 5: Integrate into Themes
- [ ] Add positioning statement to homepage hero
- [ ] Add offer ladder to homepage/services page
- [ ] Add ICP definition to homepage/about page
- [ ] Test display on all 4 sites

### Step 6: Validation
- [ ] Verify Custom Post Types appear in admin
- [ ] Verify Custom Fields save correctly
- [ ] Verify components display correctly on frontend
- [ ] Verify site_assignment filtering works
- [ ] Test REST API endpoints

---

## Architecture Validation Notes

**Approved Patterns:**
- ✅ WordPress Custom Post Types for structured content
- ✅ Custom Fields (ACF/Meta Box) for metadata
- ✅ Component-based template structure
- ✅ Site assignment filtering for multi-site support
- ✅ REST API enabled for future integrations

**Implementation Guidelines:**
- Use ACF (Advanced Custom Fields) or Meta Box for custom fields
- Follow WordPress coding standards
- Ensure components are responsive
- Test on all 4 sites before deployment
- Document any deviations from specifications

---

## Handoff Status

**Architecture Review:** ✅ COMPLETE  
**Specifications:** ✅ READY  
**Implementation:** ⏳ READY FOR AGENT-7

**Next Steps:**
1. Agent-7 implements Custom Post Types and Custom Fields
2. Agent-7 creates component templates
3. Agent-7 adds content for all 4 sites
4. Agent-7 integrates into themes
5. Agent-2 reviews implementation structure
6. Proceed to Phase 2 (Funnel Infrastructure)

---

**Status:** Ready for Phase 1 implementation  
**ETA:** 5-7 days for Brand Core fixes across all 4 sites

