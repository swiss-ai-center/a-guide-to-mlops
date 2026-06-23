// Reveal and fade-out animations, re-initialized on instant navigation.
(function () {
    let revealObserver = null;

    function initScrollAnimations() {
        // Fade-out elements on scroll
        const fadeElements = document.getElementsByClassName('scroll-fade-out');
        document.removeEventListener('scroll', scrollFadeOutHandler);
        if (fadeElements.length > 0) {
            document.addEventListener('scroll', scrollFadeOutHandler, { passive: true });
        }

        // Reveal elements when they enter the viewport
        const revealElements = document.querySelectorAll('.reveal');
        if (revealObserver) {
            revealObserver.disconnect();
            revealObserver = null;
        }
        if (revealElements.length > 0) {
            if ('IntersectionObserver' in window) {
                revealObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');
                            revealObserver.unobserve(entry.target);
                        }
                    });
                }, {
                    threshold: 0.15,
                    rootMargin: '0px 0px -50px 0px'
                });
                revealElements.forEach(el => revealObserver.observe(el));
            } else {
                // Graceful degradation for browsers without IntersectionObserver
                // (e.g. terminal browsers that run JS but lack the API).
                revealElements.forEach(el => el.classList.add('visible'));
            }
        }
    }

    function scrollFadeOutHandler() {
        const elements = document.getElementsByClassName('scroll-fade-out');
        const scroll = window.scrollY;
        for (let i = 0; i < elements.length; i++) {
            const element = elements[i];
            const offset = parseFloat(element.getAttribute('data-offset'));
            if (!isNaN(offset) && scroll > offset) {
                element.style.opacity = 0;
            } else {
                element.style.opacity = '';
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollAnimations);
    } else {
        initScrollAnimations();
    }

    // Re-run when the document is replaced by instant navigation.
    if (typeof document$ !== 'undefined') {
        document$.subscribe(initScrollAnimations);
    }
})();
