/* dirk.it first-party analytics — data stays in our own database.
   Meta Pixel: when a Pixel ID exists, set window.META_PIXEL_ID before this script loads. */
(function () {
  try {
    var v;
    try {
      v = localStorage.getItem('_did');
      if (!v) { v = Math.random().toString(36).slice(2) + Date.now().toString(36); localStorage.setItem('_did', v); }
    } catch (e) { v = null; }
    var utm = {};
    try {
      var q = new URLSearchParams(location.search);
      ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
        var x = q.get(k); if (x) utm[k] = x.slice(0, 100);
      });
    } catch (e) {}
    fetch('https://jbbvoajtbgzhxnbcpkcc.supabase.co/functions/v1/track', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        site: location.host,
        path: location.pathname,
        ref: document.referrer || null,
        lang: (navigator.language || '').slice(0, 20),
        vw: window.innerWidth,
        utm: Object.keys(utm).length ? utm : null,
        visitor: v
      }),
      keepalive: true
    }).catch(function () {});

    /* Outbound checkout clicks */
    document.addEventListener('click', function (ev) {
      var a = ev.target && ev.target.closest ? ev.target.closest('a[href*="buy.stripe.com"]') : null;
      if (!a) return;
      try {
        fetch('https://jbbvoajtbgzhxnbcpkcc.supabase.co/functions/v1/track', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ site: location.host, path: a.getAttribute('href'), event: 'checkout_click', visitor: v }),
          keepalive: true
        }).catch(function () {});
      } catch (e) {}
    }, true);

    /* Meta Pixel loader (activates only when an ID is provided) */
    if (window.META_PIXEL_ID) {
      !function(f,b,e,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src='https://connect.facebook.net/en_US/fbevents.js';s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script');
      window.fbq('init', window.META_PIXEL_ID);
      window.fbq('track', 'PageView');
    }
  } catch (e) {}
})();
