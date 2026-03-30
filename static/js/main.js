/* ════════════════════════════════════════════
   BookNest — main.js  (animations + interactions)
   ════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. Scroll Progress Bar ── */
  const progressBar = document.createElement('div');
  progressBar.id = 'scroll-progress';
  document.body.prepend(progressBar);
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    progressBar.style.width = max > 0 ? (scrolled / max * 100) + '%' : '0%';
  }, { passive: true });

  /* ── 2. Navbar shadow on scroll ── */
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  /* ── 3. Flash messages — auto-dismiss + manual close ── */
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => {
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      el.style.opacity = '0';
      el.style.transform = 'translateX(20px)';
      setTimeout(() => el.remove(), 500);
    });
  }, 4500);
  document.querySelectorAll('.alert-close').forEach(btn => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.alert');
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(20px)';
      setTimeout(() => alert.remove(), 500);
    });
  });

  /* ── 4. Star rating — submit AFTER radio is committed ── */
  document.querySelectorAll('.star-input input[type="radio"]').forEach(radio => {
    radio.addEventListener('change', () => {
      setTimeout(() => radio.closest('form')?.submit(), 10);
    });
  });

  /* ── 5. Search input — clear on Escape ── */
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('keydown', e => {
      if (e.key === 'Escape') { searchInput.value = ''; searchInput.blur(); }
    });
  }

  /* ── 6. Staggered card entrance (IntersectionObserver) ── */
  const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('card-revealed');
        cardObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.06, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.book-card, .stat-card, .card').forEach((el, i) => {
    // Assign stagger delay class (cycles through 1-8)
    const staggerClass = 'stagger-' + ((i % 8) + 1);
    el.classList.add(staggerClass);
    cardObserver.observe(el);
  });

  /* ── 7. Genre pill pop-in with stagger ── */
  document.querySelectorAll('.genre-pill').forEach((pill, i) => {
    setTimeout(() => pill.classList.add('pill-revealed'), 80 + i * 40);
  });

  /* ── 8. Button ripple effect ── */
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      const rect = this.getBoundingClientRect();
      ripple.style.left = (e.clientX - rect.left - 4) + 'px';
      ripple.style.top = (e.clientY - rect.top - 4) + 'px';
      this.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove());
    });
  });

  /* ── 9. Stat counter animation (admin dashboard) ── */
  document.querySelectorAll('.stat-value').forEach(el => {
    const target = parseInt(el.textContent.replace(/\D/g, ''), 10);
    if (isNaN(target) || target === 0) return;
    let current = 0;
    const step = Math.ceil(target / 40);
    const suffix = el.textContent.replace(/[\d,]/g, '');
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current.toLocaleString() + suffix;
      if (current >= target) clearInterval(timer);
    }, 30);
  });

  /* ── 10. Book cover shimmer — remove after image loads ── */
  document.querySelectorAll('.book-cover-wrap img').forEach(img => {
    const wrap = img.closest('.book-cover-wrap');
    if (!wrap) return;
    const done = () => wrap.classList.add('loaded');
    if (img.complete && img.naturalWidth > 0) {
      done();
    } else {
      img.addEventListener('load', done);
      img.addEventListener('error', done);  // also remove shimmer on error
    }
  });

  /* ── 11. Confirm delete ── */
  document.querySelectorAll('.delete-form').forEach(form => {
    form.addEventListener('submit', e => {
      if (!confirm('Are you sure you want to delete this? This action cannot be undone.')) {
        e.preventDefault();
      }
    });
  });

  /* ── 12. Page exit transition on navigation links ── */
  document.querySelectorAll('a[href]:not([href^="#"]):not([href^="mailto"]):not([target])').forEach(link => {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('javascript')) return;
      e.preventDefault();
      document.body.style.transition = 'opacity 0.25s ease';
      document.body.style.opacity = '0';
      setTimeout(() => window.location.href = href, 250);
    });
  });

});

/* ── Stars display helper (used if needed elsewhere) ── */
function getStars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(empty);
}
