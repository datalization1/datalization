// Datalization - Main JavaScript

// Smooth scrolling to sections
function scrollToSection(id) {
  const section = document.getElementById(id);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
}

// Toggle language
function toggleLanguage() {
  const currentLang = document.documentElement.lang;
  const newLang = currentLang === "de" ? "en" : "de";

  const currentPath = window.location.pathname;
  const currentSearch = window.location.search;

  // Simple language toggle - in Django you'd use i18n URLs
  window.location.href = `/${newLang}/${currentPath.replace(
    /^\/(de|en)\//,
    ""
  )}${currentSearch}`;
}

// Intersection Observer for scroll animations
function initScrollAnimations() {
  const elements = document.querySelectorAll(".fade-in-on-scroll");
  if (!elements.length) return;

  // Fallback: wenn IntersectionObserver nicht unterstützt wird,
  // machen wir alles direkt sichtbar.
  if (!("IntersectionObserver" in window)) {
    elements.forEach((el) => el.classList.add("visible"));
    return;
  }

  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  elements.forEach((el) => observer.observe(el));
}

// Toast notification system
function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    toast.style.animation = "slideIn 0.3s ease-out reverse";
    setTimeout(() => {
      container.removeChild(toast);
    }, 300);
  }, 5000);
}

function getCookie(name) {
  const cookieStr = document.cookie;
  if (!cookieStr) return null;
  const cookies = cookieStr.split(";").map((c) => c.trim());
  for (const c of cookies) {
    if (c.startsWith(name + "="))
      return decodeURIComponent(c.substring(name.length + 1));
  }
  return null;
}

/**
 * Handle contact form submission
 * - Prevents double-binding and double-submit
 * - Sends AJAX (fetch) with CSRF and X-Requested-With
 * - Expects JSON from Django; falls back to generic message
 */
function initContactForm() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  // Prevent the listener from being bound multiple times
  if (form.dataset.bound === "1") return;
  form.dataset.bound = "1";

  form.addEventListener(
    "submit",
    async (e) => {
      e.preventDefault();

      // Guard against double-submit while a request is in-flight
      if (form.dataset.submitting === "1") return;
      form.dataset.submitting = "1";

      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());

      // Client-side required validation (keep in sync with Django form)
      const required = ["first_name", "last_name", "email", "message"];
      const invalid = required.some(
        (key) => !data[key] || data[key].trim() === ""
      );
      if (invalid) {
        const msg =
          document.documentElement.lang === "de"
            ? "Bitte füllen Sie alle Pflichtfelder aus."
            : "Please fill in all required fields.";
        showToast(msg, "error");
        form.dataset.submitting = "0";
        return;
      }

      // Button state
      const btn = form.querySelector('button[type="submit"]');
      const originalHTML = btn.innerHTML;
      const sendingText =
        document.documentElement.lang === "de"
          ? "Wird gesendet…"
          : "Sending…";
      btn.disabled = true;
      btn.textContent = sendingText;

      try {
        // CSRF token
        const csrfCookie = getCookie("csrftoken");
        // Fallback: wenn kein Cookie, dann wenigstens den Hidden-Input nutzen
        const csrfHeader =
          csrfCookie ||
          (document.querySelector("[name=csrfmiddlewaretoken]")?.value || "");

        const response = await fetch(form.action, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfHeader,
            "X-Requested-With": "XMLHttpRequest",
          },
          body: formData,
          credentials: "same-origin", // <- WICHTIG: Cookies mitsenden!
        });

        let payload = null;
        try {
          payload = await response.json();
        } catch (_) {
          // If server didn't return JSON, continue with generic handling
        }

        if (response.ok && (!payload || payload.ok !== false)) {
          const successMsg =
            payload && payload.message
              ? payload.message
              : document.documentElement.lang === "de"
              ? "Vielen Dank! Wir melden uns bald bei Ihnen."
              : "Thank you! We'll get back to you soon.";
          showToast(successMsg, "success");
          form.reset();
        } else {
          const errorMsg =
            document.documentElement.lang === "de"
              ? "Bitte prüfen Sie Ihre Eingaben."
              : "Please check your input.";
          showToast(errorMsg, "error");
          if (payload && payload.errors) {
            console.warn("Form errors:", payload.errors);
          }
        }
      } catch (err) {
        console.error("Error submitting form:", err);
        const fallbackMsg =
          document.documentElement.lang === "de"
            ? "Ein unerwarteter Fehler ist aufgetreten."
            : "An unexpected error occurred.";
        showToast(fallbackMsg, "error");
      } finally {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
        form.dataset.submitting = "0";
      }
    },
    { passive: false }
  );
}

// Set current year in footer
function setCurrentYear() {
  const yearElement = document.getElementById("current-year");
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
}

// Handle page visibility for animations (Re-Init, falls Tab gewechselt wurde)
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    initScrollAnimations();
  }
});

// === DOMContentLoaded: alles initialisieren ===
document.addEventListener("DOMContentLoaded", () => {
  // Basis-Initialisierung
  initScrollAnimations();
  initContactForm();
  setCurrentYear();

  // === Mobile Navigation Toggle ===
  const toggle = document.querySelector(".nav__toggle");
  const links = document.querySelector(".nav__links");
  const body = document.body;

  if (!toggle || !links) return;

  function openNav() {
    links.classList.add("nav__links--open");
    body.classList.add("nav-open", "no-scroll");
    toggle.setAttribute("aria-expanded", "true");
  }

  function closeNav() {
    links.classList.remove("nav__links--open");
    body.classList.remove("nav-open", "no-scroll");
    toggle.setAttribute("aria-expanded", "false");
  }

  let open = false;

  toggle.addEventListener("click", () => {
    if (open) {
      closeNav();
    } else {
      openNav();
    }
    open = !open;
  });

  links.addEventListener("click", (e) => {
    const target = e.target.closest("a, button");
    if (!target) return;
    if (target.classList.contains("nav__dropdown-toggle")) {
      // Service-Dropdown im Mobile nicht sofort schließen
      e.preventDefault();
      e.stopPropagation();
      return;
    }
    if (target.tagName.toLowerCase() === "a") {
      closeNav();
      open = false;
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 768 && open) {
      closeNav();
      open = false;
    }
  });
});

// Smooth scroll polyfill for older browsers
if (!("scrollBehavior" in document.documentElement.style)) {
  const originalScrollTo = window.scrollTo;
  window.scrollTo = function (x, y) {
    if (typeof x === "object") {
      const options = x;
      if (options.behavior === "smooth") {
        smoothScrollTo(options.top || 0, 500);
        return;
      }
    }
    originalScrollTo.call(window, x, y);
  };

  function smoothScrollTo(targetY, duration) {
    const startY = window.pageYOffset;
    const diff = targetY - startY;
    const startTime = performance.now();

    function step(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const ease = progress * (2 - progress); // easeOutQuad

      originalScrollTo.call(window, 0, startY + diff * ease);

      if (progress < 1) {
        requestAnimationFrame(step);
      }
    }

    requestAnimationFrame(step);
  }
}

// Expose functions globally for onclick handlers
window.scrollToSection = scrollToSection;
window.toggleLanguage = toggleLanguage;
window.showToast = showToast;
