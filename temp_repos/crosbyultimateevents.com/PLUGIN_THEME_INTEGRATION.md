# Plugin & Theme Integration Guide
## How the Business Plan Plugin Works with the Sales Funnel Theme

**Date:** December 2024

---

## Overview

You have two separate but complementary systems:

1. **Business Plan Plugin** (`crosby-business-plan`) - Displays business plan content
2. **Sales Funnel Theme** (updated `crosbyultimateevents` theme) - Implements sales funnel structure

This guide explains how they interact and how to use them together.

---

## Current Architecture

### Business Plan Plugin
**Location:** `wordpress-plugins/crosby-business-plan/`

**Purpose:** Displays business plan content on pages via shortcode

**Features:**
- Shortcode: `[crosby_business_plan]`
- Section-specific display: `[crosby_business_plan section="executive"]`
- Admin settings page
- Custom styling via plugin CSS

**How It Works:**
- Plugin registers shortcode handler
- When shortcode is used, it loads `templates/business-plan-display.php`
- Displays formatted business plan content

### Sales Funnel Theme
**Location:** `wordpress-theme/crosbyultimateevents/`

**Purpose:** Provides sales funnel structure (homepage, consultation, services, etc.)

**Features:**
- `front-page.php` - Sales funnel homepage
- `page-consultation.php` - Consultation booking page
- `header.php` - Navigation with CTA buttons
- `style.css` - Theme styling

**How It Works:**
- WordPress uses these templates for pages/posts
- No direct interaction with plugin
- Uses standard WordPress template hierarchy

---

## How They Interact

### Current State: Independent Systems

**The plugin and theme currently work independently:**
- ✅ Plugin can be used on any page via shortcode
- ✅ Theme templates work regardless of plugin status
- ✅ They don't conflict with each other
- ⚠️ They don't automatically share data or styling

### Integration Options

You can integrate them in several ways:

---

## Integration Method 1: Business Plan Page

**Use Case:** Create a dedicated "Business Plan" page accessible from navigation

**Implementation:**

1. **Create a WordPress Page:**
   - Go to WordPress Admin → Pages → Add New
   - Title: "Business Plan" or "Our Business Plan"
   - Add shortcode: `[crosby_business_plan]`
   - Publish

2. **Add to Navigation:**
   - Go to Appearance → Menus
   - Add the Business Plan page to your navigation menu

3. **Optional: Create Custom Template:**
   - Create `page-business-plan.php` in theme
   - Can add custom header/content around the shortcode

**Result:** Visitors can view full business plan from navigation menu

---

## Integration Method 2: Link from Sales Funnel Pages

**Use Case:** Add business plan links strategically in sales funnel

**Where to Add:**
- **About Page:** Link to business plan in credentials section
- **Consultation Page:** Link for investors/partners who want details
- **Footer:** Link to business plan for transparency

**Example Code (in theme templates):**

```php
<!-- Add to page-consultation.php or other pages -->
<div class="business-plan-link">
    <p>Want to learn more about our business? <a href="<?php echo esc_url(home_url('/business-plan')); ?>">View our Business Plan</a></p>
</div>
```

---

## Integration Method 3: Section Integration

**Use Case:** Display specific business plan sections on relevant pages

**Examples:**

1. **Services Page:**
   ```php
   <?php echo do_shortcode('[crosby_business_plan section="products"]'); ?>
   ```

2. **About Page:**
   ```php
   <?php echo do_shortcode('[crosby_business_plan section="company"]'); ?>
   <?php echo do_shortcode('[crosby_business_plan section="management"]'); ?>
   ```

3. **Financial/Investor Page:**
   ```php
   <?php echo do_shortcode('[crosby_business_plan section="financial"]'); ?>
   ```

**Implementation:**
- Edit theme template files (e.g., `page-services.php`)
- Add shortcode calls where appropriate

---

## Integration Method 4: Enhanced Theme Functions

**Use Case:** Create helper functions in theme to easily access business plan content

**Add to `functions.php`:**

```php
/**
 * Check if Business Plan plugin is active
 */
function crosby_is_business_plan_active() {
    return class_exists('Crosby_Business_Plan');
}

/**
 * Display business plan section (with plugin check)
 */
function crosby_display_business_plan_section($section = 'all') {
    if (crosby_is_business_plan_active()) {
        echo do_shortcode("[crosby_business_plan section='{$section}']");
    } else {
        echo '<p>Business plan content not available.</p>';
    }
}

/**
 * Get business plan link
 */
function crosby_get_business_plan_link() {
    $page = get_page_by_path('business-plan');
    if ($page) {
        return get_permalink($page->ID);
    }
    return home_url('/business-plan');
}
```

**Usage in Templates:**
```php
<?php crosby_display_business_plan_section('executive'); ?>
```

---

## Styling Integration

### Current State
- Plugin has its own CSS: `assets/style.css`
- Theme has its own CSS: `style.css`
- They may have conflicting styles

### Solution: Style Coordination

**Option 1: Plugin Respects Theme Colors**

Update plugin CSS to use theme CSS variables (if defined):

```css
/* In plugin assets/style.css */
.crosby-business-plan {
    --primary-color: #d4af37;
    --secondary-color: #2c3e50;
    /* Or inherit from theme if available */
}
```

**Option 2: Theme Adds Plugin Styles**

Add plugin-specific styles to theme's `style.css`:

```css
/* In theme style.css */
.crosby-business-plan {
    /* Override plugin styles to match theme */
}
```

**Option 3: Shared Color Variables**

Define colors in both, or use WordPress customizer to sync:

```php
// In functions.php - add customizer colors
// Both plugin and theme can use same color values
```

---

## Recommended Integration Strategy

### For Sales Funnel Use

**Primary Approach:** Keep them separate but linked

1. **Sales Funnel Pages** (Theme):
   - Homepage (`front-page.php`) - Main entry point
   - Consultation page - Lead capture
   - Services page - Service details
   - Portfolio page - Social proof

2. **Business Plan Page** (Plugin):
   - Separate page with full business plan
   - Accessible via footer link or About section
   - Useful for:
     - Investors
     - Partners
     - Credibility/transparency
     - Detailed information seekers

### Navigation Structure

```
Home (front-page.php - Sales Funnel)
├── Services (page-services.php)
├── Portfolio (page-portfolio.php)
├── About (page.php - includes business plan link)
├── Business Plan (page with [crosby_business_plan] shortcode)
├── Blog (index.php)
└── Contact/Consultation (page-consultation.php)
```

---

## Data Sharing (Future Enhancement)

### Potential Integrations

**1. Extract Data from Business Plan for Theme:**

The business plan has structured data (pricing, services, etc.). You could:

```php
// In functions.php or a custom integration plugin
function crosby_get_service_packages() {
    // Parse business plan or use custom post types
    return [
        'intimate-dining' => [
            'name' => 'Intimate Dining Experience',
            'price' => '$800-$1,500',
            'description' => '3-course meal for 2-6 guests...'
        ],
        // etc.
    ];
}
```

**2. Dynamic Pricing Display:**

```php
// In front-page.php
<?php 
$packages = crosby_get_service_packages();
foreach ($packages as $package) {
    echo "<div class='package'>";
    echo "<h3>{$package['name']}</h3>";
    echo "<p class='price'>{$package['price']}</p>";
    echo "</div>";
}
?>
```

**3. Service Data Sync:**

- Store service info in WordPress Custom Post Types
- Plugin reads from same data source
- Theme displays same data
- Single source of truth

---

## Implementation Checklist

### Immediate (Use Current Setup)

- [x] Plugin installed and activated
- [x] Theme updated with sales funnel templates
- [ ] Create "Business Plan" page with shortcode
- [ ] Add Business Plan link to navigation/footer
- [ ] Test plugin shortcode on a page

### Short-term (Basic Integration)

- [ ] Create helper functions in `functions.php`
- [ ] Add business plan links to relevant pages
- [ ] Coordinate CSS between plugin and theme
- [ ] Test styling consistency

### Medium-term (Enhanced Integration)

- [ ] Create custom post types for services/packages
- [ ] Build data sync between plugin and theme
- [ ] Create admin interface for managing shared data
- [ ] Add business plan sections to relevant theme pages

---

## Code Examples

### Example 1: Add Business Plan Section to About Page

**File:** `page-about.php` (create if doesn't exist)

```php
<?php get_header(); ?>

<main class="site-main">
    <div class="content-area">
        <?php while (have_posts()) : the_post(); ?>
            <article <?php post_class(); ?>>
                <h1><?php the_title(); ?></h1>
                <?php the_content(); ?>
                
                <!-- Business Plan Section -->
                <?php if (function_exists('crosby_is_business_plan_active') && crosby_is_business_plan_active()) : ?>
                    <section class="business-plan-section">
                        <h2>Our Business Plan</h2>
                        <p>Learn more about our business strategy and goals:</p>
                        <?php echo do_shortcode('[crosby_business_plan section="executive"]'); ?>
                        <a href="<?php echo esc_url(home_url('/business-plan')); ?>" class="btn-primary">
                            View Full Business Plan
                        </a>
                    </section>
                <?php endif; ?>
            </article>
        <?php endwhile; ?>
    </div>
</main>

<?php get_footer(); ?>
```

### Example 2: Add Business Plan Link to Footer

**File:** `footer.php`

```php
<footer class="site-footer">
    <div class="container">
        <div class="footer-content">
            <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. All rights reserved.</p>
            
            <!-- Business Plan Link -->
            <?php if (function_exists('crosby_is_business_plan_active') && crosby_is_business_plan_active()) : ?>
                <p>
                    <a href="<?php echo esc_url(home_url('/business-plan')); ?>">
                        View Our Business Plan
                    </a>
                </p>
            <?php endif; ?>
            
            <?php wp_nav_menu(array(
                'theme_location' => 'footer',
                'menu_class' => 'footer-menu',
            )); ?>
        </div>
    </div>
</footer>
```

### Example 3: Services Page with Business Plan Data

**File:** `page-services.php`

```php
<?php get_header(); ?>

<main class="site-main">
    <div class="content-area">
        <h1>Our Services</h1>
        
        <!-- Services from theme -->
        <div class="services-grid">
            <!-- Your service cards -->
        </div>
        
        <!-- Detailed pricing from business plan -->
        <?php if (function_exists('crosby_is_business_plan_active') && crosby_is_business_plan_active()) : ?>
            <section class="detailed-pricing">
                <h2>Detailed Pricing Information</h2>
                <?php echo do_shortcode('[crosby_business_plan section="products"]'); ?>
            </section>
        <?php endif; ?>
    </div>
</main>

<?php get_footer(); ?>
```

---

## Troubleshooting

### Plugin Shortcode Not Working

**Symptoms:** Shortcode displays as text `[crosby_business_plan]`

**Solutions:**
1. Check plugin is activated: Plugins → Installed Plugins
2. Clear WordPress cache
3. Check for plugin errors: Enable WP_DEBUG in `wp-config.php`
4. Verify shortcode registration in plugin file

### Styling Conflicts

**Symptoms:** Business plan looks different from theme

**Solutions:**
1. Check plugin CSS loading order
2. Add theme overrides for plugin styles
3. Use CSS specificity to override plugin styles
4. Coordinate color schemes between plugin and theme

### Plugin Not Found

**Symptoms:** `crosby_is_business_plan_active()` returns false

**Solutions:**
1. Verify plugin is installed and activated
2. Check plugin class name matches
3. Use alternative check: `class_exists('Crosby_Business_Plan')`
4. Check for plugin loading errors

---

## Best Practices

1. **Keep Separation of Concerns:**
   - Plugin = Business plan content display
   - Theme = Sales funnel structure and design

2. **Use Checks Before Integration:**
   ```php
   if (function_exists('function_name') || class_exists('Class_Name')) {
       // Use plugin features
   }
   ```

3. **Graceful Degradation:**
   - Site should work if plugin is deactivated
   - Don't break theme if plugin is missing

4. **Consistent Styling:**
   - Coordinate colors between plugin and theme
   - Use shared CSS variables if possible

5. **Performance:**
   - Only load plugin CSS on pages that need it
   - Cache business plan content if possible

---

## Summary

**Current Relationship:**
- ✅ Plugin and theme are independent
- ✅ Plugin can be used via shortcode on any page
- ✅ Theme provides sales funnel structure
- ⚠️ They don't automatically share data/styling

**Recommended Usage:**
- Use theme for sales funnel (homepage, consultation, services)
- Use plugin for dedicated business plan page
- Link them via navigation and strategic page links
- Coordinate styling for consistency

**Future Enhancements:**
- Create shared data source (custom post types)
- Build admin interface for managing shared content
- Auto-sync service/pricing data between plugin and theme

---

**Last Updated:** December 2024  
**Related Files:**
- Plugin: `wordpress-plugins/crosby-business-plan/`
- Theme: `wordpress-theme/crosbyultimateevents/`
- Documentation: `PLUGIN_DEPLOYMENT_GUIDE.md`
