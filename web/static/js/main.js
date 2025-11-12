// Datalization - Main JavaScript

// Smooth scrolling to sections
function scrollToSection(id) {
  const section = document.getElementById(id);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
}

// Toggle mobile menu
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');
    
    if (mobileMenu.classList.contains('active')) {
        mobileMenu.classList.remove('active');
        menuIcon.classList.remove('hidden');
        closeIcon.classList.add('hidden');
    } else {
        mobileMenu.classList.add('active');
        menuIcon.classList.add('hidden');
        closeIcon.classList.remove('hidden');
    }
}

// Toggle language
function toggleLanguage() {
    const currentLang = document.documentElement.lang;
    const newLang = currentLang === 'de' ? 'en' : 'de';
    
    // Redirect to the new language version
    const currentPath = window.location.pathname;
    const currentSearch = window.location.search;
    
    // Simple language toggle - in Django you'd use i18n URLs
    window.location.href = `/${newLang}/${currentPath.replace(/^\/(de|en)\//, '')}${currentSearch}`;
}

// Intersection Observer for scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Observe all elements with fade-in-on-scroll class
    document.querySelectorAll('.fade-in-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Toast notification system
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    }, 5000);
}


function getCookie(name) {
  const cookieStr = document.cookie;
  if (!cookieStr) return null;
  const cookies = cookieStr.split(';').map(c => c.trim());
  for (const c of cookies) {
    if (c.startsWith(name + '=')) return decodeURIComponent(c.substring(name.length + 1));
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
    const form = document.getElementById('contact-form');
    if (!form) return;

    // Prevent the listener from being bound multiple times
    if (form.dataset.bound === '1') return;
    form.dataset.bound = '1';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Guard against double-submit while a request is in-flight
        if (form.dataset.submitting === '1') return;
        form.dataset.submitting = '1';

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Client-side required validation (keep in sync with Django form)
        const required = ['first_name', 'last_name', 'email', 'message'];
        const invalid = required.some((key) => !data[key] || data[key].trim() === '');
        if (invalid) {
            const msg = document.documentElement.lang === 'de'
                ? 'Bitte füllen Sie alle Pflichtfelder aus.'
                : 'Please fill in all required fields.';
            showToast(msg, 'error');
            form.dataset.submitting = '0';
            return;
        }

        // Button state
        const btn = form.querySelector('button[type="submit"]');
        const originalHTML = btn.innerHTML;
        const sendingText = document.documentElement.lang === 'de' ? 'Wird gesendet…' : 'Sending…';
        btn.disabled = true;
        btn.textContent = sendingText;

        try {
            // CSRF token
                const csrfCookie = getCookie('csrftoken');
                // Fallback: wenn kein Cookie, dann wenigstens den Hidden-Input nutzen
                const csrfHeader = csrfCookie || (document.querySelector('[name=csrfmiddlewaretoken]')?.value || '');

                const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfHeader,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData,
                credentials: 'same-origin',   // <- WICHTIG: Cookies mitsenden!
            });

            let payload = null;
            try {
                payload = await response.json();
            } catch (_) {
                // If server didn't return JSON, continue with generic handling
            }

            if (response.ok && (!payload || payload.ok !== false)) {
                const successMsg = (payload && payload.message)
                    ? payload.message
                    : (document.documentElement.lang === 'de'
                        ? 'Vielen Dank! Wir melden uns bald bei Ihnen.'
                        : "Thank you! We'll get back to you soon.");
                showToast(successMsg, 'success');
                form.reset();
            } else {
                const errorMsg = document.documentElement.lang === 'de'
                    ? 'Bitte prüfen Sie Ihre Eingaben.'
                    : 'Please check your input.';
                showToast(errorMsg, 'error');
                if (payload && payload.errors) {
                    console.warn('Form errors:', payload.errors);
                }
            }
        } catch (err) {
            console.error('Error submitting form:', err);
            const fallbackMsg = document.documentElement.lang === 'de'
                ? 'Ein unerwarteter Fehler ist aufgetreten.'
                : 'An unexpected error occurred.';
            showToast(fallbackMsg, 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalHTML;
            form.dataset.submitting = '0';
        }
    }, { passive: false });
}

// Set current year in footer
function setCurrentYear() {
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

// Navbar background on scroll
function initNavbarScroll() {
    const nav = document.getElementById('navigation');
    if (!nav) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.style.backgroundColor = 'rgba(10, 10, 10, 0.98)';
        } else {
            nav.style.backgroundColor = 'rgba(10, 10, 10, 0.95)';
        }
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initScrollAnimations();
    initContactForm();
    setCurrentYear();
    initNavbarScroll();
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        const mobileMenu = document.getElementById('mobile-menu');
        const nav = document.getElementById('navigation');
        
        if (mobileMenu && mobileMenu.classList.contains('active')) {
            if (!nav.contains(e.target)) {
                toggleMobileMenu();
            }
        }
    });
});

// Handle page visibility for animations
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Re-trigger animations if needed
        initScrollAnimations();
    }
});

// Smooth scroll polyfill for older browsers
if (!('scrollBehavior' in document.documentElement.style)) {
    const originalScrollTo = window.scrollTo;
    window.scrollTo = function(x, y) {
        if (typeof x === 'object') {
            const options = x;
            if (options.behavior === 'smooth') {
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
            
            window.scrollTo(0, startY + diff * ease);
            
            if (progress < 1) {
                requestAnimationFrame(step);
            }
        }
        
        requestAnimationFrame(step);
    }
}

// Expose functions globally for onclick handlers
window.scrollToSection = scrollToSection;
window.toggleMobileMenu = toggleMobileMenu;
window.toggleLanguage = toggleLanguage;
window.showToast = showToast;
