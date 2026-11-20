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
