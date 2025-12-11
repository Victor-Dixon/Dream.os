# Swarm Logo Assets

Official Swarm Intelligence branding assets for all WordPress sites.

## Files

- `logo.svg` - Vector logo (scalable, preferred format)
- `favicon.ico` - Favicon for browser tabs
- PNG versions in multiple sizes (to be generated)

## Usage

### WordPress Integration

1. Upload logo files to theme directory: `wp-content/themes/{theme-name}/assets/logo/`
2. Update `functions.php` to register custom logo:
   ```php
   add_theme_support('custom-logo', array(
       'height'      => 48,
       'width'       => 48,
       'flex-height' => true,
       'flex-width'  => true,
   ));
   ```
3. Update `header.php` to display logo:
   ```php
   if (has_custom_logo()) {
       the_custom_logo();
   } else {
       // Fallback to SVG or emoji
       echo '<div class="logo-icon">🐝</div>';
   }
   ```

## Brand Colors

- **Primary Blue**: `#00d4ff`
- **Primary Purple**: `#8b5cf6`
- **Electric Green**: `#00ff88`
- **Dark Background**: `#0a0e27`

## Brand Text

- **Tagline**: "WE. ARE. SWARM."
- **Full Name**: "Swarm Intelligence"
- **Description**: "Multi-Agent Swarm Coordination System"

## License

Swarm Intelligence branding - Internal use only.

