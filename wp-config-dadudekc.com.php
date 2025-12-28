<?php
define( 'WPCACHEHOME', '/home/u996867598/domains/dadudekc.com/public_html/wp-content/plugins/wp-super-cache/' );
define( 'WP_CACHE', true );

/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * Localized language
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'u996867598_8ZrHJ' );

/** Database username */
define( 'DB_USER', 'u996867598_X4xY1' );

/** Database password */
define( 'DB_PASSWORD', 'yDnyj5xtZy' );

/** Database hostname */
define( 'DB_HOST', '127.0.0.1' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',          'sP[#Qodbi6+UhWt*#=*$OWj7$<AXk89TDN+VW^M.E^MgU`nmtlG#$*A*f?uCC~Gx' );
define( 'SECURE_AUTH_KEY',   'AAe? Mm2x57.&}>vvkI8^y&#z`pu0C({~80mp|ka-;lZ,I*{zH<eY2D;_aBONJHb' );
define( 'LOGGED_IN_KEY',     '4Bm~] kGGu!-m>}TDhQ_Z~WU$)]!!_4Tl@&>+9m?Ee1vinxAgL^v.rH!5?/3~1A$' );
define( 'NONCE_KEY',         'Q~k/A3(xK|W:Zwq}eWQ2qcc~/UK_=}5$nBgC,(?@khkd[}WICVetss9/N+}Nq9St' );
define( 'AUTH_SALT',         'aXZxy-.#^^D zHdF:jaS b%>0Ma1ULmS><8C+>hrOs[[no-m-r2BDyWv&N3tMn/:' );
define( 'SECURE_AUTH_SALT',  'V8v<xLr~,^uW`!fwf~aEo]T0tUnSo#~C&+8QEuv&7z-`v#ViZM1lao(wuA-`,E)F' );
define( 'LOGGED_IN_SALT',    '-<RhX$:+0d7&]HJS&uUg8`9<hGf](wfbjyCl>9em8DoSK4od,4WWsr*L8vpG3|?U' );
define( 'NONCE_SALT',        '#u~y~3aD0c9r!JO4C2.Dv(]hOmqKgU(@Q<M[e[4X2kY> l*|#N##c*z>SXeF?JV:' );
define( 'WP_CACHE_KEY_SALT', '-76<;yLS1N~@9Vwah7[By?I9]hWc`ikWcv3/Ib:!8[-p00Wf}js1s2XKJg;DFFKj' );


/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';


/* Add any custom values between this line and the "stop editing" line. */



/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
if ( ! defined( 'WP_DEBUG' ) ) {
	define( 'WP_DEBUG', false );
}

define( 'FS_METHOD', 'direct' );
define( 'COOKIEHASH', '4e940bccb558138bfc64825be44fe4f1' );
define( 'WP_AUTO_UPDATE_CORE', 'minor' );

// GA4/Pixel Analytics Configuration
define('GA4_MEASUREMENT_ID', 'G-PLACEHOLDER');
define('FACEBOOK_PIXEL_ID', '000000000000000');
/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
