document.addEventListener("DOMContentLoaded", function () {
  const wrappers = document.querySelectorAll(".case-icon-wrapper");
  const prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hasFinePointer = window.matchMedia && window.matchMedia("(pointer: fine)").matches;

  if (!wrappers.length || prefersReducedMotion) {
    return; // Safety: nichts machen bei reduzierter Motion
  }

  // Helper zum Anwenden der kombinierten Transform
  function applyTransform(wrapper) {
    const py = parseFloat(wrapper.dataset.parallaxY || "0");
    const tiltX = parseFloat(wrapper.dataset.tiltX || "0");
    const tiltY = parseFloat(wrapper.dataset.tiltY || "0");
    const hoverScale = parseFloat(wrapper.dataset.hoverScale || "1");

    // WICHTIG: Basis-Scale kommt jetzt NICHT mehr aus JS, sondern nur aus CSS.
    // JS macht nur noch Parallax + Tilt + Hover-Scale.
    const scale = hoverScale;

    wrapper.style.transform =
      `translate3d(0, ${py}px, 0) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale(${scale})`;
  }

  // Initiale Random-Settings + Animation-Duration / Delay pro Icon
  const illustrations = document.querySelectorAll(".case-icon-illustration");
  illustrations.forEach((img, index) => {
    const depth = 0.9 + Math.random() * 0.3; // 0.9 – 1.2, nur noch für Parallax-Intensität
    const baseFloat = 7 + Math.random() * 3; // 7–10s
    const baseRotate = 8.5 + Math.random() * 3;
    const baseScale = 5.5 + Math.random() * 2;
    const baseGlow = 5 + Math.random() * 2;
    const delayBase = Math.random() * 0.8;

    img.style.animationDuration =
      `${baseFloat}s, ${baseRotate}s, ${baseScale}s, ${baseGlow}s`;
    img.style.animationDelay =
      `${delayBase}s, ${delayBase + 0.25}s, ${delayBase + 0.5}s, ${delayBase + 0.75}s`;

    const wrapper = wrappers[index];
    if (wrapper) {
      wrapper.dataset.depth = depth.toFixed(2);    // nur für Parallax
      wrapper.dataset.hoverScale = "1";            // Basis-Scale 1, nur Hover ändert
      wrapper.dataset.parallaxY = "0";
      wrapper.dataset.tiltX = "0";
      wrapper.dataset.tiltY = "0";
      applyTransform(wrapper);
    }
  });

  // Parallax-Update bei Scroll
  function updateParallax() {
    const viewportHeight = window.innerHeight || 800;
    wrappers.forEach((wrapper) => {
      const rect = wrapper.getBoundingClientRect();
      const center = rect.top + rect.height / 2;
      const relative = (center - viewportHeight / 2) / viewportHeight; // -0.5 .. 0.5
      const depth = parseFloat(wrapper.dataset.depth || "1");
      const intensity = 40 * depth; // Parallax-Stärke (bleibt)
      const parallaxY = -relative * intensity;
      wrapper.dataset.parallaxY = parallaxY.toFixed(2);
      applyTransform(wrapper);
    });
  }

  updateParallax();
  window.addEventListener("scroll", updateParallax, { passive: true });
  window.addEventListener("resize", updateParallax);

  // Hover-Tilt nur auf Desktop / „fine pointer“
  if (hasFinePointer) {
    wrappers.forEach((wrapper) => {
      wrapper.addEventListener("mousemove", (event) => {
        const rect = wrapper.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width;  // 0..1
        const y = (event.clientY - rect.top) / rect.height; // 0..1

        const maxTilt = 10;
        const tiltX = (0.5 - y) * maxTilt; // oben/unten
        const tiltY = (x - 0.5) * maxTilt; // links/rechts

        wrapper.dataset.tiltX = tiltX.toFixed(2);
        wrapper.dataset.tiltY = tiltY.toFixed(2);
        wrapper.dataset.hoverScale = "1.04"; // leichtes Zoom im Hover
        applyTransform(wrapper);
      });

      wrapper.addEventListener("mouseleave", () => {
        wrapper.dataset.tiltX = "0";
        wrapper.dataset.tiltY = "0";
        wrapper.dataset.hoverScale = "1";
        applyTransform(wrapper);
      });
    });
  }
});