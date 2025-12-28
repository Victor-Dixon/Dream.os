<?php
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
define( 'DB_NAME', 'u996867598_Bcdu2' );

/** Database username */
define( 'DB_USER', 'u996867598_h0ve7' );

/** Database password */
define( 'DB_PASSWORD', 'yGYxwN3bug' );

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
define( 'AUTH_KEY',          'w=Xq6#Vco{g:Lv /&?#X+r$ybjgKo=oS#$H=csUUk&VBp${,h{-h|Pvr*zn4P5H>' );
define( 'SECURE_AUTH_KEY',   ';jGlMU,,jnh2rfI7b8~rjS.gInE:M`lPM:X$3+.ZpyNO)RKg!1.{bnI*Q<ajoj{2' );
define( 'LOGGED_IN_KEY',     '$%|zG&S3DOGV}xv:^iY!#zI}<>hU~d3Y=X=y~A<b?cuRxs^.,hiWQG0LX+dD8ZVs' );
define( 'NONCE_KEY',         '!H7rjC2RzP2I#i{CD}g-hyfnZ&GI]Ba__12Fd6^Q(UFQrFt2JggAHh:kqxfRLC44' );
define( 'AUTH_SALT',         'I6lR)AEv??YX4=#CKlqZ>s7io+!+o*kCQHmRz]vlcR4+iW%tp303;ZE6td`^7C-i' );
define( 'SECURE_AUTH_SALT',  'g7uz[/`p+B>P&~3:UaU[|iv1.c(N 6B.Th% K,j;;9]W}yb6m)GCM#icOiAblxZ9' );
define( 'LOGGED_IN_SALT',    'dRcz.d+4P+>id%tAEgdHlk1yT`T9h>U~F-W G:P*VBkku]NM |?SyVRo.ilI%JXq' );
define( 'NONCE_SALT',        'Rj?R00~I&E0-sk&+.!ZJfY{}$wG,[*-]h#xQM_M!MSRLn-R8Cqq~D$LD_a}H*!AS' );
define( 'WP_CACHE_KEY_SALT', 'r<~uPUDncM.}DF9oSGZ@#Mlx]mK:!Y6qFJx6SE&Xz?<NN8@c[fj/:D(-BH,. -6]' );


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
define( 'COOKIEHASH', 'd70554f8b0fbf29e797d342b1a773d05' );
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
