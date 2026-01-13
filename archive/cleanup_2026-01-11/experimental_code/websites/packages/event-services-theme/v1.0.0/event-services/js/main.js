/**
 * Event Services Theme JavaScript
 * Professional event planning and catering services functionality
 */

(function($) {
    'use strict';

    // Document ready
    $(document).ready(function() {
        initEventBookingForm();
        initSmoothScrolling();
        initServiceCardAnimations();
        initTestimonialSlider();
    });

    /**
     * Initialize event booking form
     */
    function initEventBookingForm() {
        $('#event-booking-form').on('submit', function(e) {
            e.preventDefault();

            // Basic form validation
            var formData = {
                event_type: $('#event-type').val(),
                event_date: $('#event-date').val(),
                guest_count: $('#guest-count').val(),
                contact_name: $('#contact-name').val(),
                contact_email: $('#contact-email').val(),
                contact_phone: $('#contact-phone').val(),
                message: $('#message').val()
            };

            // Validate required fields
            if (!formData.event_type || !formData.event_date || !formData.guest_count ||
                !formData.contact_name || !formData.contact_email || !formData.contact_phone) {
                alert('Please fill in all required fields.');
                return;
            }

            // Email validation
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(formData.contact_email)) {
                alert('Please enter a valid email address.');
                return;
            }

            // Submit form via AJAX
            $.ajax({
                url: eventServicesAjax.ajax_url,
                type: 'POST',
                data: {
                    action: 'submit_event_booking',
                    nonce: eventServicesAjax.nonce,
                    form_data: formData
                },
                success: function(response) {
                    if (response.success) {
                        alert('Thank you! We\'ll contact you within 24 hours to discuss your event.');
                        $('#event-booking-form')[0].reset();
                    } else {
                        alert('Sorry, there was an error submitting your request. Please try again.');
                    }
                },
                error: function() {
                    alert('Sorry, there was an error submitting your request. Please try again.');
                }
            });
        });
    }

    /**
     * Initialize smooth scrolling for anchor links
     */
    function initSmoothScrolling() {
        $('a[href^="#"]').on('click', function(e) {
            var target = $(this.getAttribute('href'));
            if (target.length) {
                e.preventDefault();
                $('html, body').animate({
                    scrollTop: target.offset().top - 100
                }, 1000);
            }
        });
    }

    /**
     * Initialize service card animations
     */
    function initServiceCardAnimations() {
        $('.service-card').hover(
            function() {
                $(this).addClass('animated');
            },
            function() {
                $(this).removeClass('animated');
            }
        );
    }

    /**
     * Initialize testimonial slider
     */
    function initTestimonialSlider() {
        if ($('.testimonials-grid').length && $('.testimonial-card').length > 1) {
            var currentIndex = 0;
            var testimonials = $('.testimonial-card');
            var totalTestimonials = testimonials.length;

            // Hide all testimonials except the first
            testimonials.hide().first().show();

            // Auto-rotate testimonials
            setInterval(function() {
                testimonials.eq(currentIndex).fadeOut(500, function() {
                    currentIndex = (currentIndex + 1) % totalTestimonials;
                    testimonials.eq(currentIndex).fadeIn(500);
                });
            }, 5000);

            // Add navigation dots
            var dotsHtml = '<div class="testimonial-dots">';
            for (var i = 0; i < totalTestimonials; i++) {
                dotsHtml += '<span class="dot" data-index="' + i + '"></span>';
            }
            dotsHtml += '</div>';

            $('.testimonials-grid').after(dotsHtml);

            // Handle dot clicks
            $('.dot').on('click', function() {
                var targetIndex = $(this).data('index');
                if (targetIndex !== currentIndex) {
                    testimonials.eq(currentIndex).fadeOut(500, function() {
                        currentIndex = targetIndex;
                        testimonials.eq(currentIndex).fadeIn(500);
                        updateDots();
                    });
                }
            });

            function updateDots() {
                $('.dot').removeClass('active');
                $('.dot').eq(currentIndex).addClass('active');
            }

            updateDots();
        }
    }

    /**
     * Handle catering menu interactions
     */
    function initCateringMenu() {
        $('.menu-category h4').on('click', function() {
            $(this).next('ul').slideToggle();
            $(this).toggleClass('expanded');
        });
    }

    /**
     * Form validation helpers
     */
    function validateEmail(email) {
        var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePhone(phone) {
        var re = /^[\+]?[1-9][\d]{0,15}$/;
        return re.test(phone.replace(/[\s\-\(\)]/g, ''));
    }

})(jQuery);