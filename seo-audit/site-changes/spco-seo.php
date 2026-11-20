<?php
/**
 * SPCO SEO fixes (20 Nov 2026). Loaded from functions.php.
 * 1. Loads spco-heading-preserve.css, which keeps headings looking the same after their tags
 *    were changed to fix skipped heading levels.
 * 2. Stops duplicate stylesheets: Ultimate Addons (UAE) registers its own copies of icon and
 *    nav-menu files that Elementor already loads. A UAE copy is removed only when Elementor's
 *    identical (or minified) file is on the same page.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'wp_enqueue_scripts', function () {
	$file = get_stylesheet_directory() . '/spco-heading-preserve.css';
	if ( file_exists( $file ) ) {
		wp_enqueue_style( 'spco-heading-preserve', get_stylesheet_directory_uri() . '/spco-heading-preserve.css', array(), (string) filemtime( $file ) );
	}
}, 30 );

function spco_seo_dedupe_styles() {
	$pairs = array(
		'hfe-elementor-icons'                    => 'elementor-icons',
		'hfe-nav-menu-widget'                    => 'widget-nav-menu',
		'hfe-nav-menu-icons'                     => 'elementor-icons-fa-solid',
		'hfe-social-share-icons-fontawesome'     => 'elementor-icons-shared-0',
		'hfe-social-share-icons-brands'          => 'elementor-icons-fa-brands',
	);
	foreach ( $pairs as $duplicate => $keep ) {
		$keep_loaded = wp_style_is( $keep, 'enqueued' ) || wp_style_is( $keep, 'done' );
		if ( $keep_loaded && wp_style_is( $duplicate, 'enqueued' ) && ! wp_style_is( $duplicate, 'done' ) ) {
			wp_dequeue_style( $duplicate );
		}
	}
}
add_action( 'wp_print_styles', 'spco_seo_dedupe_styles', 100 );
add_action( 'wp_print_footer_scripts', 'spco_seo_dedupe_styles', 1 );

/**
 * 3. Sitemap stylesheet. Yoast SEO 28.9 stopped linking its sitemap stylesheet ("removed temporarily,
 *    to be restored in a future release"), so sitemaps showed as raw XML in browsers. This re-attaches
 *    a Yoast-style XSL view (spco-child/main-sitemap.xsl, clickable links) with Yoast's own CSS
 *    stylesheet (/main-sitemap.css) as the fallback for browsers without XSLT. It runs only on sitemap URLs and steps aside if
 *    Yoast, or anything else, already outputs an xml-stylesheet line. Search engines ignore it.
 */
add_action( 'init', function () {
	$path = isset( $_SERVER['REQUEST_URI'] ) ? (string) strtok( wp_unslash( $_SERVER['REQUEST_URI'] ), '?' ) : '';
	if ( ! preg_match( '#/([a-z0-9_-]+-)?sitemap(_index|[0-9]+)?\.xml$#i', $path ) ) {
		return;
	}
	ob_start( function ( $buffer ) {
		if ( strpos( $buffer, '<?xml' ) !== 0 || strpos( $buffer, 'xml-stylesheet' ) !== false || strpos( $buffer, 'Yoast SEO' ) === false ) {
			return $buffer;
		}
		// XSLT view (clickable links) for browsers that still support it; Yoast's CSS view as the fallback.
		$pi  = '<?xml-stylesheet type="text/xsl" href="' . esc_url( get_stylesheet_directory_uri() . '/main-sitemap.xsl' ) . '"?>';
		$pi .= '<?xml-stylesheet type="text/css" href="' . esc_url( home_url( '/main-sitemap.css' ) ) . '"?>';
		return preg_replace( '/^(<\?xml[^>]*\?>)/', '$1' . $pi, $buffer, 1 );
	} );
}, 0 );

/**
 * 4. Mobile speed (20 Nov 2026).
 *    a) Homepage hero: preload the hero background (it is a CSS background, so browsers otherwise only
 *       find it after reading the stylesheets). One preload per Elementor breakpoint, each matching the
 *       file Elementor serves there (mobile 1536px, tablet 2048px, desktop 2560px).
 *    b) Google Fonts: Elementor loaded 4 separate font stylesheets (incl. Roboto and Roboto Slab, which no
 *       text on the site uses) and Astra a 5th. Replaced by one request for the families actually used.
 *       Same font files and font-display: swap, so text renders identically.
 */
add_action( 'wp_head', function () {
	if ( ! is_front_page() ) {
		return;
	}
	$base = content_url( '/uploads/2026/11/StrathdeePolley_Homepage_Background_Web' );
	$hero = array(
		'(max-width: 767px)'                         => $base . '-1536x683.jpg',
		'(min-width: 768px) and (max-width: 1024px)' => $base . '-2048x910.jpg',
		'(min-width: 1025px)'                        => $base . '-scaled.jpg',
	);
	foreach ( $hero as $media => $url ) {
		printf( "<link rel=\"preload\" as=\"image\" href=\"%s\" media=\"%s\" fetchpriority=\"high\" />\n", esc_url( $url ), esc_attr( $media ) );
	}
}, 1 );

add_filter( 'elementor/frontend/print_google_fonts', '__return_false' );
add_action( 'wp_enqueue_scripts', function () {
	wp_dequeue_style( 'astra-google-fonts' );
	wp_enqueue_style(
		'spco-google-fonts',
		'https://fonts.googleapis.com/css?family=Montserrat:300,400,500,600,700|Rubik:300,400,500,600,700|Source+Sans+Pro:400&display=swap',
		array(),
		null
	);
}, 20 );
