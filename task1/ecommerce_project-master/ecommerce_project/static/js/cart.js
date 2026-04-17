// static/js/cart.js

// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity    = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

  // Prevent double-submission on Add to Cart
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function () {
      const btn = this.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled    = true;
        btn.textContent = 'Adding…';
      }
    });
  });
});