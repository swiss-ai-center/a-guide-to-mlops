// Canvas-based parallax starfield for the story landing page.
(function () {
    function initStarfield() {
        const container = document.getElementById('starfield');
        if (!container) {
            if (window.__mlopsStarfieldCleanup) {
                window.__mlopsStarfieldCleanup();
                window.__mlopsStarfieldCleanup = null;
            }
            return;
        }

        // Tear down any previous instance before creating a new one.
        if (window.__mlopsStarfieldCleanup) {
            window.__mlopsStarfieldCleanup();
            window.__mlopsStarfieldCleanup = null;
        }

        const canvas = document.createElement('canvas');
        canvas.className = 'starfield-canvas';
        canvas.style.position = 'absolute';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        container.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        if (!ctx) return;
        let width, height;

        function isLightTheme() {
            return document.body && document.body.dataset.mdColorScheme === 'default';
        }

        function starColor() {
            return isLightTheme() ? '18, 22, 33' : '255, 255, 255';
        }

        // Star layers: farther layers move slower and have smaller, dimmer stars.
        const layerConfigs = [
            { count: 180, speed: 0.03, sizeMin: 1.0, sizeMax: 2.2, opacity: 0.65 },
            { count: 110, speed: 0.10, sizeMin: 1.4, sizeMax: 3.0, opacity: 0.85 },
            { count: 45,  speed: 0.22, sizeMin: 2.0, sizeMax: 4.0, opacity: 1.0 }
        ];

        let stars = [];
        let docHeight = 0;

        function resize() {
            const dpr = window.devicePixelRatio || 1;
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = Math.floor(width * dpr);
            canvas.height = Math.floor(height * dpr);
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            generateStars();
            draw();
        }

        function generateStars() {
            docHeight = Math.max(document.documentElement.scrollHeight, height * 2);
            stars = [];
            layerConfigs.forEach(cfg => {
                for (let i = 0; i < cfg.count; i++) {
                    stars.push({
                        x: Math.random() * width,
                        y: Math.random() * docHeight,
                        speed: cfg.speed,
                        size: cfg.sizeMin + Math.random() * (cfg.sizeMax - cfg.sizeMin),
                        opacity: cfg.opacity * (0.5 + Math.random() * 0.5),
                        twinklePhase: Math.random() * Math.PI * 2,
                        twinkleSpeed: 0.002 + Math.random() * 0.003
                    });
                }
            });
        }

        function draw() {
            const scroll = window.scrollY;
            ctx.clearRect(0, 0, width, height);

            const now = Date.now();
            stars.forEach(star => {
                const visibleY = star.y - scroll * star.speed;
                // Allow a little overscan so stars can enter/leave smoothly.
                if (visibleY < -10 || visibleY > height + 10) return;

                const twinkle = 0.7 + 0.3 * Math.sin(now * star.twinkleSpeed + star.twinklePhase);
                const alpha = star.opacity * twinkle;

                const radius = Math.max(star.size / 2, 0.8);
                const rgb = starColor();
                ctx.beginPath();
                ctx.arc(star.x, visibleY, radius, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(' + rgb + ', ' + alpha + ')';
                ctx.fill();

                // Soft glow for larger stars.
                if (star.size > 1.6) {
                    ctx.beginPath();
                    ctx.arc(star.x, visibleY, star.size * 2.2, 0, Math.PI * 2);
                    ctx.fillStyle = 'rgba(' + rgb + ', ' + (alpha * 0.22) + ')';
                    ctx.fill();
                }
            });
        }

        let ticking = false;
        function requestDraw() {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    draw();
                    ticking = false;
                });
                ticking = true;
            }
        }

        window.addEventListener('resize', resize, { passive: true });
        window.addEventListener('scroll', requestDraw, { passive: true });

        // Regenerate when document height changes (e.g. fonts loaded).
        const resizeObserver = new ResizeObserver(() => {
            generateStars();
            requestDraw();
        });
        resizeObserver.observe(document.documentElement);

        // Redraw when the user toggles between light and dark mode.
        const themeObserver = new MutationObserver(() => {
            requestDraw();
        });
        if (document.body) {
            themeObserver.observe(document.body, {
                attributes: true,
                attributeFilter: ['data-md-color-scheme']
            });
        }

        // Expose a cleanup function so instant navigation can tear down
        // the old starfield before creating a new one.
        window.__mlopsStarfieldCleanup = function () {
            window.removeEventListener('resize', resize, { passive: true });
            window.removeEventListener('scroll', requestDraw, { passive: true });
            resizeObserver.disconnect();
            themeObserver.disconnect();
            if (canvas.parentNode) {
                canvas.parentNode.removeChild(canvas);
            }
        };

        resize();
        requestDraw();
    }

    // Re-initialize on instant navigation; fall back to DOMContentLoaded
    // when instant navigation is not available.
    if (typeof document$ !== 'undefined') {
        document$.subscribe(initStarfield);
    } else if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initStarfield);
    } else {
        initStarfield();
    }
})();
