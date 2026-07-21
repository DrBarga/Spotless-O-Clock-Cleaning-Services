const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('[data-menu-button]');
const nav = document.querySelector('[data-nav]');
const serviceSelect = document.querySelector('#service');
const emailEndpoint = 'https://formsubmit.co/ajax/spotlessoclock@gmail.com';

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

document.querySelectorAll('[data-email-form]').forEach(form => {
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const status = form.querySelector('[data-form-status]');
    const button = form.querySelector('button[type="submit"]');
    const formType = form.dataset.formType;

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const payload = Object.fromEntries(new FormData(form).entries());
    if (payload._honey) return;
    delete payload._honey;
    payload._template = 'table';
    payload['Website page'] = window.location.href;

    button.disabled = true;
    status.className = 'form-status field-wide';
    status.textContent = 'Sending…';

    try {
      const response = await fetch(emailEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error('Submission failed');

      status.classList.add('success');
      status.textContent = formType === 'review'
        ? 'Thank you. Your review has been sent for approval.'
        : 'Thank you. Your quote request has been emailed to Spotless O’Clock.';
      form.reset();
    } catch (error) {
      status.classList.add('error');
      status.textContent = 'Sorry, we could not send this form. Please email spotlessoclock@gmail.com or contact us on WhatsApp.';
    } finally {
      button.disabled = false;
    }
  });
});

document.querySelector('[data-year]').textContent = new Date().getFullYear();
