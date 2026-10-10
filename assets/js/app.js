'use strict';
(() => {
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
  // Tracking is intentionally dormant until explicit consent and an analytics service are configured.
  const consentedEvent = (name, params={}) => {
    if (!window.hbAnalyticsConsented) return;
    if (typeof window.gtag === 'function') window.gtag('event', name, params);
  };
  for (const element of document.querySelectorAll('[data-track]')) {
    element.addEventListener('click', () => consentedEvent('hb_click', {destination:element.dataset.track, page:document.body.dataset.page}));
  }
  for (const button of document.querySelectorAll('[data-filter]')) {
    button.addEventListener('click', () => {
      const chosen=button.dataset.filter;
      document.querySelectorAll('[data-filter]').forEach(b => {b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button));});
      document.querySelectorAll('[data-category]').forEach(tile => {tile.hidden = chosen !== 'all' && tile.dataset.category !== chosen;});
      consentedEvent('hb_filter', {category: chosen});
    });
    button.setAttribute('aria-pressed',String(button.classList.contains('active')));
  }
  // View-item can fire only if analytics has been enabled after appropriate consent.
  if (document.body.dataset.page.startsWith('hb-')) {
    consentedEvent('view_item', {item_id: document.body.dataset.page});
  }
  const enquiry=document.querySelector('#inquiryForm');
  if (enquiry) {
    const piece=new URLSearchParams(location.search).get('piece');
    if (piece) enquiry.querySelector('#piece').value=piece.slice(0,150);
    enquiry.addEventListener('submit',async event=>{
      event.preventDefault();
      const name=enquiry.querySelector('#name').value.trim();
      const country=enquiry.querySelector('#country').value.trim();
      const product=enquiry.querySelector('#piece').value.trim();
      const message=enquiry.querySelector('#message').value.trim();
      const status=enquiry.querySelector('#formStatus');
      if (!name||!message){status.textContent='Please enter your name and message before copying.';status.classList.add('show');return;}
      const text=`Hello Horodetska Boho,\n\n${message}\n\nName: ${name}\nCountry: ${country||'Not specified'}\nPiece / enquiry: ${product||'General enquiry'}`;
      try{await navigator.clipboard.writeText(text);status.textContent='Enquiry copied. Open Instagram and paste it into a message. Nothing has been sent by this website.';consentedEvent('hb_copy_inquiry',{category:product?'item':'general'});}
      catch(err){const fallback=document.createElement('textarea');fallback.value=text;fallback.readOnly=true;fallback.style.cssText='width:100%;min-height:130px;padding:12px;margin-top:12px;font-size:13px;border:1px solid #d4cec5';status.textContent='Automatic copying is unavailable. Select and copy the text below, then open Instagram and paste it into a message. Nothing has been sent.';status.appendChild(fallback);fallback.focus();fallback.select();}
      status.classList.add('show');
    });
  }
})();
