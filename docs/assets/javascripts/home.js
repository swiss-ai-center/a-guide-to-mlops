  /* Planet belt scroll linkage */
  (function () {
    const belt = document.getElementById('belt-track');
    if (!belt) return;

    const sections = [
      document.getElementById('section-about'),
      document.getElementById('section-intro'),
      document.getElementById('section-part-1'),
      document.getElementById('section-part-2'),
      document.getElementById('section-part-3'),
      document.getElementById('section-part-4'),
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
      fillers.forEach((planet, i) => {
        if (centers[i] !== undefined && centers[i + 1] !== undefined) {
          const mid = (centers[i] + centers[i + 1]) / 2;
          const size = planet.offsetHeight || 92;
          const top = mid - size / 2;
          planet.style.top = `${top}px`;
          planet.style.left = `${horizontalPercent(mid, centers)}%`;
        }
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

    window.addEventListener('scroll', updateBelt, { passive: true });
    window.addEventListener('resize', () => {
      layoutBelt();
      updateBelt();
    });
  })();

  /* Make header opaque once user leaves the hero */
  (function () {
    const header = document.querySelector('.md-header');
    const hero = document.getElementById('story-hero');
    if (!header || !hero) return;

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
  })();

  /* Smooth scroll for Next section links */
  (function () {
    document.addEventListener('click', function (e) {
      const link = e.target.closest('.next-section');
      if (!link) return;
      const hash = new URL(link.getAttribute('href'), window.location.href).hash;
      const target = hash ? document.querySelector(hash) : null;
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  })();
