/* Home-page enhancements: planet belt, header transparency, smooth-scroll links. */
(function () {
  function initHome() {
    const belt = document.getElementById('belt-track');
    const header = document.querySelector('.md-header');
    const hero = document.getElementById('story-hero');

    // Tear down any previous instance before re-initializing.
    if (window.__mlopsHomeCleanup) {
      window.__mlopsHomeCleanup();
      window.__mlopsHomeCleanup = null;
    }

    // Only the home page has these elements; on other pages just clean up.
    if (!belt || !header || !hero) {
      return;
    }

    const sections = [
      document.getElementById('section-about'),
      document.getElementById('section-intro'),
      document.getElementById('section-part-1'),
      document.getElementById('section-part-2'),
      document.getElementById('section-part-3'),
      document.getElementById('section-part-4'),
      document.getElementById('section-part-5'),
      document.getElementById('section-reentry'),
    ].filter(Boolean);

    const sectionPlanets = Array.from(belt.querySelectorAll('.belt-planet[data-section]'));
    const fillers = Array.from(belt.querySelectorAll('.belt-planet.filler'));

    function absoluteCenter(el) {
      const rect = el.getBoundingClientRect();
      return window.scrollY + rect.top + rect.height / 2;
    }

    function sectionMultiplier(i) {
      // Even sections (0, 2, 4…) have left-aligned cards -> planet on right.
      // Odd sections (1, 3, 5…) have right-aligned cards -> planet on left.
      return i % 2 === 0 ? 1 : -1;
    }

    function horizontalPercent(planetCenterY, centers) {
      if (!centers.length) return 50;
      const last = centers.length - 1;

      let i = 0;
      while (i < last && planetCenterY > centers[i + 1]) i++;

      let t;
      if (planetCenterY <= centers[0]) {
        i = 0;
        t = 0;
      } else if (planetCenterY >= centers[last]) {
        i = last;
        t = 0;
      } else {
        t = (planetCenterY - centers[i]) / (centers[i + 1] - centers[i]);
      }

      // Wave: +1 at section i, 0 at midpoint, -1 at section i+1.
      const h = sectionMultiplier(i) * Math.cos(Math.PI * t);
      // Map -1..1 to 18%..82% (left..right), keeping clear of the viewport edges.
      return 50 + 32 * h;
    }

    function layoutBelt() {
      const centers = sections.map(absoluteCenter);

      // Category planets: their center in the belt lines up with the section
      // center. As the belt scrolls at the same rate as the page, the planet
      // stays vertically aligned with its section.
      sectionPlanets.forEach((planet, i) => {
        if (centers[i] !== undefined) {
          const size = planet.offsetHeight || 132;
          const top = centers[i] - size / 2;
          planet.style.top = `${top}px`;
          planet.style.left = `${horizontalPercent(centers[i], centers)}%`;
        }
      });

      // Filler planets sit midway between consecutive section centers.
      // Any extra fillers trail beyond the last section using the average gap.
      const lastIdx = centers.length - 1;
      const avgGap = lastIdx > 0 ? (centers[lastIdx] - centers[0]) / lastIdx : 0;
      fillers.forEach((planet, i) => {
        let centerY;
        if (i < lastIdx) {
          centerY = (centers[i] + centers[i + 1]) / 2;
        } else if (lastIdx >= 0) {
          centerY = centers[lastIdx] + (i - lastIdx + 1) * avgGap;
        } else {
          return;
        }
        const size = planet.offsetHeight || 92;
        const top = centerY - size / 2;
        planet.style.top = `${top}px`;
        planet.style.left = `${horizontalPercent(centerY, centers)}%`;
      });

      const last = belt.lastElementChild;
      if (last) {
        const lastRect = last.getBoundingClientRect();
        const lastBottom = window.scrollY + lastRect.bottom;
        belt.style.height = `${lastBottom}px`;
      }
    }

    function updateBelt() {
      const scroll = window.scrollY;
      belt.style.transform = `translateY(${-scroll}px)`;

      // Highlight whichever planet is currently crossing the viewport center.
      const viewportCenter = scroll + window.innerHeight / 2;
      let closest = null;
      let minDist = Infinity;
      belt.querySelectorAll('.belt-planet').forEach(planet => {
        const top = parseFloat(planet.style.top) || 0;
        const center = top + planet.offsetHeight / 2;
        const dist = Math.abs(center - viewportCenter);
        if (dist < minDist) {
          minDist = dist;
          closest = planet;
        }
      });
      belt.querySelectorAll('.belt-planet').forEach(p => p.classList.remove('active'));
      if (closest) closest.classList.add('active');
    }

    layoutBelt();
    updateBelt();

    function onResize() {
      layoutBelt();
      updateBelt();
    }

    window.addEventListener('scroll', updateBelt, { passive: true });
    window.addEventListener('resize', onResize, { passive: true });

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

    function onDocumentClick(e) {
      const link = e.target.closest('.next-section');
      if (!link) return;
      const hash = new URL(link.getAttribute('href'), window.location.href).hash;
      const target = hash ? document.querySelector(hash) : null;
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    document.addEventListener('click', onDocumentClick);

    // Expose a cleanup function so instant navigation can tear down the old
    // home-page handlers before creating a new instance.
    window.__mlopsHomeCleanup = function () {
      window.removeEventListener('scroll', updateBelt, { passive: true });
      window.removeEventListener('resize', onResize, { passive: true });
      window.removeEventListener('scroll', updateHeader, { passive: true });
      document.removeEventListener('click', onDocumentClick);
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
