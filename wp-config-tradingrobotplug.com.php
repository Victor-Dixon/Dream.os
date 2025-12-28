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
define( 'DB_NAME', 'u996867598_rZy2f' );

/** Database username */
define( 'DB_USER', 'u996867598_Z9bKl' );

/** Database password */
define( 'DB_PASSWORD', 'jmZ8qXv5PU' );

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
define( 'AUTH_KEY',          '5P,V=0nK=iSwwN.!5e-t8%tTxnQexay98z,Cz2Ud{}c#a.SA0)5R81^,!DDgD Vj' );
define( 'SECURE_AUTH_KEY',   '*fJ1cY>ew:)k#d5FV`;B&VQ]Bic3Ofb``9BeM57kC[yaRb$bOTq@w^|.nulhaiJi' );
define( 'LOGGED_IN_KEY',     'ARBdIvcVz:o~S6B$VOX0Ue>QA5~=l5RRaVh([y+tc}e3$4-MCRhKLuF6UXSuE8av' );
define( 'NONCE_KEY',         'oGP<{ U3A?XBna1,P@ 3]6pC^M]7(iS)+T!}hZOS2]ub!$J6%7+jrG(EJ-D~[B]%' );
define( 'AUTH_SALT',         '&`Kf7LP`;9P~EmvH]TpytLdx:#`:t2gT]Ang&&q!DDw]4Iit?xY+5$sEYM>N~l06' );
define( 'SECURE_AUTH_SALT',  'N p_Pm0b[i<F&1;M1D}r[!67Y/Z0b;q/MW5749}keb<JZc&<l3B6{Lk2Z{Y=41Jk' );
define( 'LOGGED_IN_SALT',    'jOG%[RIMU1_{C$$UR&UM?A qU)jm/|+yp|U~e>=y9i7U157m{-tl++vyh-FLBJ;>' );
define( 'NONCE_SALT',        'k aVjWjmf=A]U/2ydVYoZq*9f{PEsVyT_hVN?>{VTM^z:)8I?J?6LvWX*:~ehi<G' );
define( 'WP_CACHE_KEY_SALT', '6J9EjV]~Iyh! 0qUvcRQK+=A^27<V|58LDbn/(@;qns^#CTfLt}cYni+/(-%6f&y' );


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
	define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
}

define( 'FS_METHOD', 'direct' );
define( 'COOKIEHASH', '17a50cb50f9224c3aa0913d9518d5fec' );
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
