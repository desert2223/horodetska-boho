'use strict';
(() => {
  // Set this only after a GA4 web data stream is created and the privacy notice is reviewed.
  // No Google tag or consent banner is loaded while this is empty.
  const GA4_MEASUREMENT_ID = '';

  const toggle = document.querySelector('.mobile-toggle');
  const menu = document.querySelector('#mobileMenu');
  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      const expanded = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(expanded));
      toggle.setAttribute('aria-label', expanded ? 'Close menu' : 'Open menu');
      toggle.textContent = expanded ? '✕' : '☰';
      menu.classList.toggle('open', expanded);
      document.body.classList.toggle('menu-open', expanded);
    });
  }

  // GA4: basic consent mode. Google scripts do not load before opt-in.
  const consentKey = 'hb-ga4-consent-v1';
  let trackingStarted = false;
  window.hbAnalyticsConsented = false;

  function consentedEvent(name, params = {}) {
    if (window.hbAnalyticsConsented && typeof window.gtag === 'function') {
      window.gtag('event', name, params);
    }
  }

  function trackItemView() {
    const id = document.body.dataset.page || '';
    if (!/^hb-\d{2}$/.test(id)) return;
    const name = (document.querySelector('.page-hero h1')?.textContent || id).trim();
    consentedEvent('view_item', {
      items: [{ item_id: id.toUpperCase(), item_name: name, item_brand: 'Horodetska Boho' }]
    });
  }

  function startGoogleAnalytics() {
    if (trackingStarted || !/^G-[A-Z0-9]+$/.test(GA4_MEASUREMENT_ID)) return;
    trackingStarted = true;
    window.hbAnalyticsConsented = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {
      analytics_storage: 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
    window.gtag('js', new Date());
    window.gtag('consent', 'update', { analytics_storage: 'granted' });
    window.gtag('config', GA4_MEASUREMENT_ID, { send_page_view: true });

    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA4_MEASUREMENT_ID);
    document.head.appendChild(script);
    trackItemView();
  }

  function storedConsent() {
    try { return localStorage.getItem(consentKey); }
    catch (_) { return null; }
  }
  function saveConsent(value) {
    try { localStorage.setItem(consentKey, value); }
    catch (_) { /* Private browsing may block storage. */ }
  }

  function setupConsentUi() {
    if (!/^G-[A-Z0-9]+$/.test(GA4_MEASUREMENT_ID)) return;
    const box = document.createElement('div');
    box.className = 'analytics-consent-banner';
    box.setAttribute('role', 'region');
    box.setAttribute('aria-label', 'Analytics preferences');
    box.innerHTML = [
      '<div class="analytics-consent-copy">',
      '<strong>Optional website analytics</strong>',
      '<p>With your permission, Google Analytics helps us understand which collections visitors explore. It is optional. You can change your choice later. <a href="/contact/#privacy">Privacy information</a>.</p>',
      '</div>',
      '<div class="analytics-consent-actions">',
      '<button type="button" data-analytics-choice="reject">Reject</button>',
      '<button type="button" data-analytics-choice="accept">Accept analytics</button>',
      '</div>'
    ].join('');
    document.body.appendChild(box);

    const manage = document.createElement('a');
    manage.href = '#analytics-preferences';
    manage.textContent = 'Analytics preferences';
    manage.className = 'analytics-prefs-link';
    manage.addEventListener('click', (event) => {
      event.preventDefault();
      box.hidden = false;
      box.querySelector('[data-analytics-choice="reject"]').focus();
    });
    document.querySelector('.footer-bottom')?.appendChild(manage);

    box.querySelectorAll('[data-analytics-choice]').forEach(button => {
      button.addEventListener('click', () => {
        const accepted = button.dataset.analyticsChoice === 'accept';
        const previouslyActive = trackingStarted;
        saveConsent(accepted ? 'accepted' : 'rejected');
        box.hidden = true;
        if (accepted) startGoogleAnalytics();
        else if (previouslyActive) {
          // Reload prevents further events from the previously loaded Google tag.
          window.location.reload();
        }
      });
    });

    const preference = storedConsent();
    box.hidden = preference === 'accepted' || preference === 'rejected';
    if (preference === 'accepted') startGoogleAnalytics();
  }

  for (const element of document.querySelectorAll('[data-track]')) {
    element.addEventListener('click', () => {
      const destination = element.dataset.track;
      const page = document.body.dataset.page || 'unknown';
      consentedEvent('hb_click', { destination, page });

      const selection = /^look_(\d{2})_(?:open|details)$/.exec(destination);
      if (selection) {
        const itemName = (element.closest('.product-tile')?.querySelector('h3')?.textContent || 'Look ' + selection[1]).trim();
        consentedEvent('select_item', {
          item_list_name: 'Collections',
          items: [{ item_id: 'HB-' + selection[1], item_name: itemName, item_brand: 'Horodetska Boho' }]
        });
      }
      if (/^request_look_\d{2}$/.test(destination)) {
        // This is intent, NOT a submitted lead or a completed purchase.
        consentedEvent('hb_enquiry_intent', { item_id: page.toUpperCase() });
      }
    });
  }

  for (const button of document.querySelectorAll('[data-filter]')) {
    button.addEventListener('click', () => {
      const chosen = button.dataset.filter;
      document.querySelectorAll('[data-filter]').forEach(b => {
        b.classList.toggle('active', b === button);
        b.setAttribute('aria-pressed', String(b === button));
      });
      document.querySelectorAll('[data-category]').forEach(tile => {
        tile.hidden = chosen !== 'all' && tile.dataset.category !== chosen;
      });
      consentedEvent('hb_filter', { category: chosen });
    });
    button.setAttribute('aria-pressed', String(button.classList.contains('active')));
  }

  const enquiry = document.querySelector('#inquiryForm');
  if (enquiry) {
    const piece = new URLSearchParams(window.location.search).get('piece');
    if (piece) enquiry.querySelector('#piece').value = piece.slice(0, 150);
    enquiry.addEventListener('submit', async event => {
      event.preventDefault();
      const name = enquiry.querySelector('#name').value.trim();
      const country = enquiry.querySelector('#country').value.trim();
      const product = enquiry.querySelector('#piece').value.trim();
      const message = enquiry.querySelector('#message').value.trim();
      const status = enquiry.querySelector('#formStatus');
      if (!name || !message) {
        status.textContent = 'Please enter your name and message before copying.';
        status.classList.add('show');
        return;
      }
      const text = `Hello Horodetska Boho,\n\n${message}\n\nName: ${name}\nCountry: ${country || 'Not specified'}\nPiece / enquiry: ${product || 'General enquiry'}`;
      try {
        await navigator.clipboard.writeText(text);
        status.textContent = 'Enquiry copied. Open Instagram and paste it into a message. Nothing has been sent by this website.';
        // No name, country, free text, or other personal information is tracked.
        consentedEvent('hb_copy_inquiry', { category: product ? 'item' : 'general' });
      } catch (_) {
        const fallback = document.createElement('textarea');
        fallback.value = text;
        fallback.readOnly = true;
        fallback.style.cssText = 'width:100%;min-height:130px;padding:12px;margin-top:12px;font-size:13px;border:1px solid #d4cec5';
        status.textContent = 'Automatic copying is unavailable. Select and copy the text below, then open Instagram and paste it into a message. Nothing has been sent.';
        status.appendChild(fallback);
        fallback.focus();
        fallback.select();
      }
      status.classList.add('show');
    });
  }

  setupConsentUi();
})();
