/* Home-page enhancements: header transparency on hero. */
(function () {
  function initHome() {
    const header = document.querySelector('.md-header');
    const hero = document.getElementById('story-hero');

    if (window.__mlopsHomeCleanup) {
      window.__mlopsHomeCleanup();
      window.__mlopsHomeCleanup = null;
    }

    // Only the home page has these elements; on other pages just clean up.
    if (!header || !hero) {
      return;
    }

    function updateHeader() {
      const heroBottom = hero.getBoundingClientRect().bottom;
      if (heroBottom <= window.innerHeight) {
        header.classList.add('md-header--shadow');
      } else {
        header.classList.remove('md-header--shadow');
      }
    }

    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();

    // Expose a cleanup function so instant navigation can tear down the old
    // home-page handlers before creating a new instance.
    window.__mlopsHomeCleanup = function () {
      window.removeEventListener('scroll', updateHeader, { passive: true });
      header.classList.remove('md-header--shadow');
    };
  }

  // Re-initialize on instant navigation; fall back to DOMContentLoaded
  // when instant navigation is not available.
  if (typeof document$ !== 'undefined') {
    document$.subscribe(initHome);
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHome);
  } else {
    initHome();
  }
})();
