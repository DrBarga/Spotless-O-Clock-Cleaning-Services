const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('[data-menu-button]');
const nav = document.querySelector('[data-nav]');
const form = document.querySelector('[data-quote-form]');
const serviceSelect = document.querySelector('#service');

const onScroll = () => header?.classList.toggle('scrolled', window.scrollY > 20);
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });

menuButton?.addEventListener('click', () => {
  const open = !nav.classList.contains('open');
  nav.classList.toggle('open', open);
  menuButton.setAttribute('aria-expanded', String(open));
});

document.querySelectorAll('.site-nav a').forEach(link => {
  link.addEventListener('click', () => {
    nav.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
  });
});

const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -50px' });

document.querySelectorAll('.reveal').forEach(element => revealObserver.observe(element));

document.querySelectorAll('[data-service-link]').forEach(link => {
  link.addEventListener('click', () => {
    if (serviceSelect) serviceSelect.value = link.dataset.serviceLink;
  });
});

document.querySelectorAll('[data-plan]').forEach(plan => {
  plan.addEventListener('click', () => {
    document.querySelectorAll('[data-plan]').forEach(item => item.classList.remove('active'));
    plan.classList.add('active');
    if (serviceSelect) serviceSelect.value = 'Home cleaning';
    document.querySelector('#details').value = `I’m interested in a ${plan.dataset.plan.toLowerCase()} cleaning plan.`;
    document.querySelector('#quote').scrollIntoView({ behavior: 'smooth' });
  });
});

document.querySelectorAll('[data-accordion] details').forEach(item => {
  item.addEventListener('toggle', () => {
    if (!item.open) return;
    document.querySelectorAll('[data-accordion] details').forEach(other => {
      if (other !== item) other.removeAttribute('open');
    });
  });
});

form?.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(form);
  const lines = [
    `Hi Spotless O'Clock, I'd like a cleaning quote.`,
    '',
    `Name: ${data.get('name')}`,
    `Postcode: ${data.get('postcode')}`,
    `Service: ${data.get('service')}`,
    data.get('details') ? `Details: ${data.get('details')}` : ''
  ].filter(Boolean);
  window.open(`https://wa.me/447915847472?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener');
});

document.querySelector('[data-year]').textContent = new Date().getFullYear();
