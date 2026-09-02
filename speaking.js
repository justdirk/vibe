/* dirk.it — speaking page: video facade, copy-bio, inquiry form (shared by all locales) */
(function () {
  var T = {
    en: { ok: "Received — thank you. Dirk's office will get back to you within two working days.", req: "Please fill in the event, date, city, your name, email and a note.", reqGeneral: "Please add your name, email and a message.", fail: "Couldn't send right now — please email mail@dirk.it.", sending: "Sending…", btn: "Send inquiry →", copied: "Copied", copy: "Copy bio" },
    de: { ok: "Angekommen — danke. Dirks Büro meldet sich innerhalb von zwei Werktagen.", req: "Bitte Event, Datum, Stadt, Name, E-Mail und eine Notiz ausfüllen.", reqGeneral: "Bitte Name, E-Mail und Nachricht ausfüllen.", fail: "Senden gerade nicht möglich — bitte an mail@dirk.it schreiben.", sending: "Wird gesendet…", btn: "Anfrage senden →", copied: "Kopiert", copy: "Bio kopieren" },
    es: { ok: "Recibido — gracias. La oficina de Dirk responderá en dos días laborables.", req: "Por favor, completa evento, fecha, ciudad, nombre, email y una nota.", reqGeneral: "Por favor, añade tu nombre, email y un mensaje.", fail: "No se pudo enviar — escribe a mail@dirk.it.", sending: "Enviando…", btn: "Enviar solicitud →", copied: "Copiado", copy: "Copiar bio" },
    pt: { ok: "Recebido — obrigado. O escritório do Dirk responde em até dois dias úteis.", req: "Preencha evento, data, cidade, nome, e-mail e uma nota.", reqGeneral: "Preencha nome, e-mail e mensagem.", fail: "Não foi possível enviar — escreva para mail@dirk.it.", sending: "Enviando…", btn: "Enviar pedido →", copied: "Copiado", copy: "Copiar bio" },
    it: { ok: "Ricevuto — grazie. L'ufficio di Dirk risponde entro due giorni lavorativi.", req: "Compila evento, data, città, nome, email e una nota.", reqGeneral: "Inserisci nome, email e messaggio.", fail: "Invio non riuscito — scrivi a mail@dirk.it.", sending: "Invio…", btn: "Invia richiesta →", copied: "Copiato", copy: "Copia bio" }
  };
  var lang = (document.documentElement.lang || "en").slice(0, 2);
  var t = T[lang] || T.en;

  var fac = document.getElementById("facade");
  if (fac) {
    var play = function () {
      if (fac.querySelector("iframe")) return;
      var i = document.createElement("iframe");
      i.src = "https://www.youtube.com/embed/JUSHQc6ueKs?autoplay=1&rel=0";
      i.title = "Dirk Ahlborn — keynote";
      i.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      i.allowFullscreen = true;
      fac.innerHTML = ""; fac.appendChild(i);
    };
    fac.addEventListener("click", play);
    fac.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); play(); } });
  }

  document.querySelectorAll(".copybtn").forEach(function (b) {
    b.addEventListener("click", function () {
      var el = document.getElementById(b.getAttribute("data-copy")); if (!el || !navigator.clipboard) return;
      navigator.clipboard.writeText(el.textContent.trim()).then(function () { b.textContent = t.copied; setTimeout(function () { b.textContent = t.copy; }, 1600); });
    });
  });

  var f = document.getElementById("book"), m = document.getElementById("fmsg"), btn = document.getElementById("fbtn"), opened = Date.now();
  if (!f) return;
  function say(text, err) { m.hidden = false; m.className = "msg" + (err ? " err" : ""); m.textContent = text; m.scrollIntoView({ block: "nearest" }); }
  f.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var kind = f.getAttribute("data-kind") || "speaking";
    var d = { kind: kind, opened: opened, lang: lang, page: location.pathname };
    new FormData(f).forEach(function (v, k) { d[k] = v; });
    var missing = kind === "speaking" ? (!d.event_name || !d.event_date || !d.event_city || !d.name || !d.email || !d.message) : (!d.name || !d.email || !d.message);
    if (missing) { say(kind === "speaking" ? t.req : t.reqGeneral, true); return; }
    btn.disabled = true; btn.textContent = t.sending;
    fetch("https://jbbvoajtbgzhxnbcpkcc.supabase.co/functions/v1/contact", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(d) })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) {
        if (x.ok && x.j.ok) { say(t.ok); f.querySelectorAll("input,select,textarea,button").forEach(function (el) { el.disabled = true; }); }
        else { say((x.j && x.j.error) || t.fail, true); btn.disabled = false; btn.textContent = t.btn; }
      })
      .catch(function () { say(t.fail, true); btn.disabled = false; btn.textContent = t.btn; });
  });
})();
