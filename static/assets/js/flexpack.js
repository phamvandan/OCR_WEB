/**
 * Theme JS
 */

'use strict';


/*** Preloader ***/

var preloader = (function() {

	// Variables
	var $window = $(window);
	var loader = $("#preloader");

	// Methods
	$window.on({
		'load': function() {

			loader.fadeOut();

		}
	});

	// Events

})();


/*** Alerts ***/

var Alert = (function() {

	// Variables
	// =========

	var LIFETIME = 5000;

	// Methods
	// =======

	function generate(type, message) {

		// Create alert
		var $alert = $('<div class="alert alert-' + type + ' alert-fixed fade show" role="alert">' + message + '</div>');

		// Append alert to the body
		$('body').append($alert);

		// Remove alert
		setTimeout(function() {
			$alert.alert('close');
		}, LIFETIME);
	};

	// Events
	// ======

	$(document).on({
		'alert.show': function(e, type, message) {
			generate(type, message);
		}
	});

})();


/*** Button to top page ***/

var toTopButton = (function() {

	// Variables
	// =========

	var topButton = $('#back-to-top');
	var scrollTop = $(window).scrollTop();
	var isActive = false;
	if (scrollTop > 100) {
		isActive = true;
	}

	// Methods	
	// =======

	// Events
	// ======
	
	$(window).scroll(function() {
		scrollTop = $(window).scrollTop();

		if (scrollTop > 100 && !isActive) {
	        isActive = true;
	        topButton.fadeIn();
	    } else if (scrollTop <= 100 && isActive) {
	        isActive = false;
	        topButton.fadeOut();
	    }

	});

})();


/*** Navbar ***/

var navbar = (function() {

	// Variables
	var navbar = $('.navbar');
	var navbarCollapse = $('.navbar-collapse');
	var navbarLink = $('.nav-link');

	// Methods
	function makeNavbarDark() {
		navbar.removeClass('navbar-light').addClass('navbar-dark');
	}
	function makeNavbarLight() {
		navbar.removeClass('navbar-dark').addClass('navbar-light');
	}
	function toggleNavbarClass() {
		var scrollTop = $(window).scrollTop();

		if ( scrollTop > 5 ) {
			makeNavbarDark();
		} else {
			makeNavbarLight();
		}
	}
	// Events

	// Toggle navbar on page load if needed
	toggleNavbarClass();

	// Toggle navbar on scroll
	$(window).scroll(function() {
		toggleNavbarClass();
	});

	// Toggle navbar class on collapse
	navbarCollapse.on({
		'show.bs.collapse': function() {
			makeNavbarDark();
		},
		'hidden.bs.collapse': function() {
			var scrollTop = $(window).scrollTop();

			if (scrollTop == 0) { 
				makeNavbarLight();
			}
		}
	});

	// Close collapsed navbar on click
	navbarLink.on('click', function() {
		
		if ( $(this).filter('[href^="#section-"]').length ) {
			navbarCollapse.collapse('hide');
		}
	});

	// Navbar active links fix
	$(window).on('activate.bs.scrollspy', function() {
		navbarLink.filter('.active').focus();
	});

})();


/*** Testimonials Slider ***/

var testimonials = (function() {
	
	// Variables
	// =========

	var $testimonialSlider = $('.testimonial-slider');

	// Methods
	// =======

	function initSlider() {
		
		$testimonialSlider.each(function() {
			var $this = $(this);
			var testimonialSlider = $this.flickity({
				cellAlign: 'center',
				initialIndex: 2,
				prevNextButtons: false,
				pageDots: false,
				contain: true,
				wrapAround: true,
				imagesLoaded: true,
				percentPosition: true
			});
		});
	}

	// Events
	// ======

	// Init slider

	if ( $testimonialSlider.length ) {
		initSlider();
	}

})();


/*** Bg Slider ***/

var slider = (function() {
	
	// Variables
	// =========

	var $bgSlider = $('.bg-slider');

	// Methods
	// =======

	function initSlider() {
		
		$bgSlider.each(function() {
			var $this = $(this);
			var bgSlider = $this.flickity({
				cellAlign: 'center',
				initialIndex: 0,
				prevNextButtons: true,
				pageDots: true,
				wrapAround: true,
				fullscreen: true,
				lazyLoad: true,
				imagesLoaded: true
			});
		});
	}

	// Events
	// ======

	// Init slider

	if ( $bgSlider.length ) {
		initSlider();
	}

})();


/*** Product Slider ***/

var product = (function() {
	
	// Variables
	// =========

	var $productSlider = $('.product-slider');

	// Methods
	// =======

	function initSlider() {
		
		$productSlider.each(function() {
			var $this = $(this);
			var productSlider = $this.flickity({
				cellAlign: 'center',
				initialIndex: 1,
				prevNextButtons: false,
				pageDots: true,
				contain: true,
				wrapAround: true,
				imagesLoaded: true
			});
		});
	}

	// Events
	// ======

	// Init slider

	if ( $productSlider.length ) {
		initSlider();
	}

})();


/*** Feature Slider ***/

var feature = (function() {
	
	// Variables
	// =========

	var $featureSlider = $('.feature-slider');

	// Methods
	// =======

	function initSlider() {
		
		$featureSlider.each(function() {
			var $this = $(this);
			var featureSlider = $this.flickity({
				cellAlign: 'center',
				initialIndex: 0,
				prevNextButtons: false,
				pageDots: true,
				contain: true,
				wrapAround: true,
				imagesLoaded: true
			});
		});
	}

	// Events
	// ======

	// Init slider

	if ( $featureSlider.length ) {
		initSlider();
	}

})();


/*** Blog Slider ***/

var blog = (function() {
	
	// Variables
	// =========

	var $blogSlider = $('.blog-slider');

	// Methods
	// =======

	function initSlider() {
		
		$blogSlider.each(function() {
			var $this = $(this);
			var blogSlider = $this.flickity({
				cellAlign: 'left',
				initialIndex: 0,
				prevNextButtons: true,
				pageDots: false,
				contain: true,
				wrapAround: true,
				imagesLoaded: true
			});
		});
	}

	// Events
	// ======

	// Init slider

	if ( $blogSlider.length ) {
		initSlider();
	}

})();


/*** Modal ***/

var Modal = (function() {
	
	// Variables
	// =========

	var $modal = $('.modal');

	// Methods
	// =======

	function startVideo(video) {
		video.play();

		console.log('Video started');
	}
	function pauseVideo(video) {
		video.pause();

		console.log('Video paused');
	}

	// Events
	// ======

	$modal.on({
		'shown.bs.modal': function() {
			var $this = $(this);

			if ( $this.find('.modal-dialog-video').length ) {
				var video = $(this).find('video');

				if ( video.length ) {
					startVideo(video.get(0));
				}
			}
		},
		'hide.bs.modal': function() {
			var $this = $(this);

			if ( $this.find('.modal-dialog-video').length ) {
				var video = $(this).find('video');

				if ( video.length ) {
					pauseVideo(video.get(0));
				}
			}	
		}
	});

})();


/*** Smooth scroll to anchor ***/

var SmoothScroll = (function() {
	
	// Variables
	// =========

	var $root = $('html, body');
	var $anchorLink = $('a[href^="#"]:not([href="#"]):not([data-toggle]):not([data-slide]):not([data-anchor-link])');

	var DURATION = 500;

	// Methods
	// =======

	function scrollTo(elem) {
		var $target = $(elem);

		$root.animate({
			scrollTop: $target.offset().top
		}, DURATION);
	}

	// Events
	// ======

	$anchorLink.on({
		'click': function(e) {

			e.preventDefault();

			scrollTo( $(this).attr('href') );
		}
	});

})();


/*** Sidebar menu ***/

var Sidebar = (function() {

	// Variables
	// =========

	var $toggle = $('[data-toggle="sidebar-menu"]');

	// Methods
	// =======

	function toggle($this) {
		var target = $this.data('target');
		var $target = $(target);

		$target.toggleClass('active');
	}

	// Events
	// ======

	$toggle.on('click', function() {
		toggle($(this));
	});
  
})();


/*** Count to (Fearure section) ***/

var countTo = (function() {

	// Variables
	var statsItem = $('.countdown-item-number');

	// Methods
	function init() {
		statsItem.each(function() {
			var $this = $(this);

			$this.waypoint(function(direction) {
				$this.not('.finished').countTo();
				}, {
				offset: 1000
			});
		});
	}
	
	// Events
	if ( statsItem.length ) {
		init();
	}
	
})();


/*** Countdown ***/

var countdown = (function() {

	// Variables
	// =========
	var clock = $('.countdown');
	var toDate = '2019/10/09';

	// Methods
	// =======

	function init() {
		clock.countdown(toDate, function(event) {
			$(this).html(event.strftime(''
				+ '<span class="clock-number display-1 h1 mx-sm-3">%D</span> days '
				+ '<span class="clock-number display-1 h1 mx-sm-3">%H</span> hr '
				+ '<span class="clock-number display-1 h1 mx-sm-3">%M</span> min '
				+ '<span class="clock-number display-1 h1 mx-sm-3">%S</span> sec'));
		});
	}

	// Events
	// ======

	if ( clock.length ) {
		init();
	}

})();


/*** Newsletter ***/

var Newsletter = (function() {

	// Variables
	// =========

	var $form = $('#mc-embedded-subscribe-form');
	var $formEmail = $('#mce-EMAIL');
	var $formClone = $('.form-mailchimp-clone');
	var $formCloneEmail = $formClone.find('input[type="email"]');

	// Methods
	// =======

	function signup() {

		$.ajax({
			type: $form.attr('method'),
			url: $form.attr('action'),
			data: $form.serialize(),
			cache: false,
			dataType: 'json',
			contentType: "application/json; charset=utf-8",
			error: function(err) {
				$(document).trigger('alert.show', ['danger', 'Could not connect to the registration server. Please try again later.']);
			},
			success: function(data) {

				if (data.result != 'success') {
					var msg = data.msg;
						
					$(document).trigger('alert.show', ['danger', msg]);
				} else {

					// Show a confirmation
					$(document).trigger('alert.show', ['success', data.msg]);
					
					// Reset a form
					$form[0].reset();
				}
			}
		});
	}
	function signupImitation() {

		// Check if the original form exists on a page
		if ( $form ) {
			$form.submit();
		}
	}
	function copyInputContent() {

		// Check if the original form exists on a page
		if ( $formEmail.length ) {
			var content = $formCloneEmail.val();

			$formEmail.val(content);
		}
	}

	// Events
	// ======

	// Sign up to a Mailchimp newsletter campaign on form submit
	$form.on('submit', function(e) {
		e.preventDefault();

		signup();
	});

	// Imitate form submission on clone submit
	$formClone.on('submit', function(e) {
		e.preventDefault();

		signupImitation();
	});

	// Copy input content to the original form input field
	$formCloneEmail.on('keyup', function() {
		copyInputContent();
	});

})();


/*** Map ***/

var Map = (function() {
	
	// Variables
	// =========

	var $mapContainer = $('.map-container');

	// Methods
	// =======

	function init() {
		$mapContainer.each(function() {
			var $this = $(this);

			var zoom = $this.data('zoom');
			var markers = $this.data('markers');
			var center = {
				lat: markers[0][0],
				lng: markers[0][1]
			};
			var styles = [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#444444"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ef7521"},{"saturation":"3"},{"lightness":"17"},{"gamma":"1.11"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#a5c4c7"},{"visibility":"on"}]}];

			// Init map

			var map = new google.maps.Map($this.get(0), {
				center: center,
				styles: styles,
				zoom: zoom
			});

			// Create markers

			var bounds = new google.maps.LatLngBounds();
			// var markerColor = getComputedStyle(document.body).getPropertyValue('--primary');

			markers.forEach(function(item, i, arr) {
				var position = {
					lat: item[0],
					lng: item[1]
				};

				var icon = $this.data('icon');

				var marker = new google.maps.Marker({
					position: position,
					map: map,
					icon: icon
				});

				// Extend bounds
				bounds.extend(position);
			});

			// Fit bounds

			if ( !zoom ) {
				map.fitBounds(bounds);
			}
		});
	}

	// Events
	// ======

	// Init map

	if ( $mapContainer.length ) {
		init();
	}

})();


/*** Fullpage.js ***/

var Fullpage = (function() {

	// Variables
	// =========

	var $fullpage = $('#fp-wrapper');

	// Methods
	// =======

	function init($container) {

		$container.fullpage({

			// Navigation
			navigation: true,
			navigationPosition: 'right',
			anchors:['home', 'about', 'experience', 'skills', 'projects', 'facts', 'contacts'],

			// Custom selectors
			sectionSelector: '.fp-section',
			licenseKey: 'OPEN-SOURCE-GPLV3-LICENSE',

			// Scrolling
			scrollingSpeed: 700,
			easingcss3: 'cubic-bezier(0.55, 0.055, 0.675, 0.19)',
			scrollOverflow: true,
			loopBottom: true,
			bigSectionsDestination: 'top',

			// Design
			responsiveWidth: 768,
			controlArrows: true,

			// Events

		});
	}

	// Events
	// ======

	if ( $fullpage.length ) {
		init($fullpage);
	}

})();


/*** Code ***/

var Code = (function() {
	
	// Variables
	// =========

	var $code = $('.code');

	// Methods
	// =======

	function init(i, block) {
		hljs.highlightBlock(block);
	}

	// Events
	// ======

	$code.each(function(i, block) {
		init(i, block);
	});

})();


/*** Feather icons ***/

var FeatherIcons = (function() {
	
	// Variables
	// =========

	// Methods
	// =======

	feather.replace()

	// Events
	// ======

})();