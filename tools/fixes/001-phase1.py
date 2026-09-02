#!/usr/bin/env python3
"""Phase-1 fixes for dirk.it (justdirk/vibe). Idempotent; run from repo root."""
import re, glob, html, json, os, sys

ROOT = os.getcwd()
assert os.path.isfile("CNAME") and open("CNAME").read().strip() == "dirk.it", "run from the vibe repo root"
TODAY = "2026-09-02"
BUNDLE_OLD = "8x2cN515hbyQ3e2eYpfw40a"
BUNDLE_NEW = "fZu7sL3dpbyQ4i69E5fw404"

L = {  # locale → labels/paths
 "en": dict(pre="", courses="Courses", speaking="Speaking", about="About", privacy="Privacy", terms="Terms", tools="Tools"),
 "de": dict(pre="/de", courses="Kurse", speaking="Keynotes", about="Über mich", privacy="Datenschutz", terms="AGB", tools="Tools"),
 "es": dict(pre="/es", courses="Cursos", speaking="Conferencias", about="Sobre mí", privacy="Privacidad", terms="Términos", tools="Herramientas"),
 "pt": dict(pre="/pt", courses="Cursos", speaking="Palestras", about="Sobre", privacy="Privacidade", terms="Termos", tools="Ferramentas"),
 "it": dict(pre="/it", courses="Corsi", speaking="Keynote", about="Chi sono", privacy="Privacy", terms="Termini", tools="Strumenti"),
}
def locale_of(path):
    top = path.split("/")[0]
    return top if top in ("de","es","pt","it") else "en"

def footer_html(loc):
    l = L[loc]; p = l["pre"]
    a = lambda href, label, extra="": f'<a href="{href}" style="font-size:14px;color:#9B958A"{extra}>{label}</a>'
    main = [a(f"{p}/courses/", l["courses"]), a(f"{p}/speaking/", l["speaking"]), a(f"{p}/about/", l["about"]),
            a(f"{p}/culinaris/", "Culinaris"), a("/privacy/", l["privacy"]), a("/terms/", l["terms"])]
    tools = [a("/chat/", "dirk.it AI"),
             a("https://starterfuel.com", "StarterFuel", ' rel="noopener"'),
             a("https://dna.dirk.it", "Venture DNA", ' rel="noopener"'),
             a("https://remixer.dirk.it", "Remixer", ' rel="noopener"'),
             a("https://pressduo.com", "PressDuo", ' rel="noopener"'),
             a("https://condivida.com", "Condivida", ' rel="noopener"')]
    home = p + "/" if p else "/"
    return ("  <footer class=\"site\">\n"
            "    <div class=\"sig\" style=\"font-size:30px\">Dirk Ahlborn</div>\n"
            "    <div class=\"footlinks\">\n"
            "      <div class=\"footrow\">" + "\n      ".join(main) + "</div>\n"
            "      <div class=\"footrow\"><span class=\"footlbl\">" + l["tools"] + "</span>" + "\n      ".join(tools) + "</div>\n"
            "    </div>\n"
            f"    <div style=\"font-size:13px;color:#8A8478\">© 2026 Dirk Ahlborn · <a href=\"{home}\" style=\"color:#E0B15C\">dirk.it</a></div>\n"
            "  </footer>")

TOOLS = {  # localized Founder Toolkit section (EN is already in index.html)
 "de": dict(eyebrow="Das Founder Toolkit", h2="Ein Founder File. Jedes Tool kennt deine Firma bereits.",
   p="Die Kurse lehren das Playbook. Diese Tools führen es aus. Alles, was du aufbaust — dein Problem, dein Kunde, deine getestete Botschaft, dein Geschäftsmodell — reist mit deinem Login als dein Founder File, sodass jedes Tool dort weitermacht, wo das letzte aufgehört hat.",
   sf="Deine Firma, fertig aus der Box. Gründung in 15 Ländern, Banking, deine Domain — und ein KI-Team, das den Alltag erledigt. Du gibst alles frei.",
   dna="Dein Gründerprofil: 72 Fragen, 12 Dimensionen. Erkenne, wofür du gebaut bist — und vergleiche Profile mit einem möglichen Mitgründer, bevor du dich festlegst.",
   rmx="Eine Idee, durch 110 Geschäftsmodelle gespielt — bewertet an dir, deinem Problem und dem Markt. Behalte zwei Überlebende und verteidige sie.",
   pd="Verwandle echte Kundeninterviews in eine Botschaft, die an echten Interessenten getestet wird — und pitche damit die Presse. Nur Belege, nichts Erfundenes.",
   ai="Dein privater KI-Workspace — kuratierte Frontier-Modelle mit wöchentlichen Credits, in den Kursen inklusive. Frag alles; bau alles.",
   cv="Dein Investoren-Datenraum: Pitch Deck, Finanzen und Rechtsdokumente hinter sicheren Einladungen — mit Seite-für-Seite-Analytics, was Investoren wirklich lesen."),
 "es": dict(eyebrow="El Founder Toolkit", h2="Un Founder File. Cada herramienta ya conoce tu empresa.",
   p="Los cursos enseñan el playbook. Estas herramientas lo ejecutan. Todo lo que construyes — tu problema, tu cliente, tu mensaje probado, tu modelo de negocio — viaja con tu login como tu Founder File, así cada herramienta sigue donde la anterior lo dejó.",
   sf="Tu empresa, lista para usar. Constitución en 15 países, banca, tu dominio — y un equipo de IA que lleva el día a día. Tú apruebas todo.",
   dna="Tu perfil de fundador: 72 preguntas, 12 dimensiones. Descubre para qué estás hecho — y compara perfiles con un posible cofundador antes de comprometerte.",
   rmx="Una idea, jugada a través de 110 modelos de negocio — puntuados según tú, tu problema y el mercado. Quédate con dos supervivientes y defiéndelos.",
   pd="Convierte entrevistas reales con clientes en un mensaje probado con prospectos reales — y usa eso para presentarte a la prensa. Solo evidencia, nada inventado.",
   ai="Tu espacio privado de IA — modelos frontera seleccionados con créditos semanales incluidos en los cursos. Pregunta lo que sea; construye lo que sea.",
   cv="Tu data room para inversores: pitch deck, finanzas y documentos legales tras invitaciones seguras — con analítica página a página de lo que los inversores realmente leen."),
 "pt": dict(eyebrow="O Founder Toolkit", h2="Um Founder File. Cada ferramenta já conhece a sua empresa.",
   p="Os cursos ensinam o playbook. Estas ferramentas o executam. Tudo o que você constrói — seu problema, seu cliente, sua mensagem testada, seu modelo de negócio — viaja com o seu login como o seu Founder File, e cada ferramenta continua de onde a anterior parou.",
   sf="Sua empresa, pronta para usar. Abertura em 15 países, banco, seu domínio — e um time de IA que cuida do dia a dia. Você aprova tudo.",
   dna="Seu perfil de fundador: 72 perguntas, 12 dimensões. Saiba para o que você foi feito — e compare perfis com um possível cofundador antes de se comprometer.",
   rmx="Uma ideia, jogada através de 110 modelos de negócio — pontuados contra você, seu problema e o mercado. Fique com dois sobreviventes e defenda-os.",
   pd="Transforme entrevistas reais com clientes em uma mensagem testada com prospects reais — e use isso para falar com a imprensa. Só evidência, nada inventado.",
   ai="Seu espaço privado de IA — modelos de fronteira selecionados com créditos semanais incluídos nos cursos. Pergunte qualquer coisa; construa qualquer coisa.",
   cv="Seu data room para investidores: pitch deck, financeiro e documentos legais atrás de convites seguros — com analytics página a página do que os investidores realmente leem."),
 "it": dict(eyebrow="Il Founder Toolkit", h2="Un Founder File. Ogni strumento conosce già la tua azienda.",
   p="I corsi insegnano il playbook. Questi strumenti lo eseguono. Tutto ciò che costruisci — il tuo problema, il tuo cliente, il tuo messaggio testato, il tuo modello di business — viaggia con il tuo login come Founder File, così ogni strumento riprende da dove l'altro ha lasciato.",
   sf="La tua azienda, pronta all'uso. Costituzione in 15 paesi, banca, il tuo dominio — e un team di IA che gestisce il quotidiano. Approvi tu ogni cosa.",
   dna="Il tuo profilo da founder: 72 domande, 12 dimensioni. Scopri per cosa sei fatto — e confronta i profili con un possibile cofondatore prima di impegnarti.",
   rmx="Un'idea, giocata attraverso 110 modelli di business — valutati su di te, sul tuo problema e sul mercato. Tieni due sopravvissuti e difendili.",
   pd="Trasforma interviste reali ai clienti in un messaggio testato su prospect reali — e con quello presentati alla stampa. Solo evidenze, niente di inventato.",
   ai="Il tuo spazio IA privato — modelli frontier selezionati con crediti settimanali inclusi nei corsi. Chiedi qualsiasi cosa; costruisci qualsiasi cosa.",
   cv="La tua data room per investitori: pitch deck, finanze e documenti legali dietro inviti sicuri — con analytics pagina per pagina su ciò che gli investitori leggono davvero."),
}
def tools_section(loc):
    t = TOOLS[loc]
    NOOP = ' rel="noopener"'
    card = lambda href, name, desc, link, ext=True: (
      f'      <a href="{href}"{NOOP if ext else ""} style="background:#0A0A09;padding:36px;display:flex;flex-direction:column;gap:12px;color:#F2EFE9">\n'
      f'        <div style="font-weight:500;font-size:22px">{name}</div>\n'
      f'        <p style="font-size:15px;line-height:1.55;color:#9B958A;margin:0">{desc}</p>\n'
      f'        <span style="font-size:14px;font-weight:600;color:#E0B15C;margin-top:auto">{link} →</span>\n'
      f'      </a>\n')
    return ("  <!-- TOOLS:start -->\n"
      '  <section class="padx" style="border-top:1px solid rgba(242,239,233,.1);padding:104px 56px;max-width:1440px;margin:0 auto;box-sizing:border-box">\n'
      '    <div style="display:flex;flex-direction:column;gap:16px;margin-bottom:56px;max-width:760px">\n'
      f'      <div style="font-size:12px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:#E0B15C">{t["eyebrow"]}</div>\n'
      f'      <h2 style="font-weight:500;font-size:clamp(34px,4vw,52px);line-height:1.05;margin:0">{t["h2"]}</h2>\n'
      f'      <p style="font-size:17px;line-height:1.6;color:#9B958A;margin:0;text-wrap:pretty">{t["p"]}</p>\n'
      '    </div>\n'
      '    <div class="g3" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1px;background:rgba(242,239,233,.1);border:1px solid rgba(242,239,233,.1)">\n'
      + card("https://starterfuel.com", "StarterFuel", t["sf"], "starterfuel.com")
      + card("https://dna.dirk.it", "Venture DNA", t["dna"], "dna.dirk.it")
      + card("https://remixer.dirk.it", "Business Model Remixer", t["rmx"], "remixer.dirk.it")
      + card("https://pressduo.com", "PressDuo", t["pd"], "pressduo.com")
      + card("/chat/", "dirk.it AI", t["ai"], "dirk.it AI", ext=False)
      + card("https://condivida.com", "Condivida", t["cv"], "condivida.com")
      + '    </div>\n  </section>\n  <!-- TOOLS:end -->\n')

META = {  # file → (title or None, description or None)
 "ai/index.html": ("AI in Practice — Dirk Ahlborn", "13 hands-on masterclasses: writing, images, video, voice, no-code apps and automation — ending with your first paid AI gig. Workspace included. $79, then $20/mo."),
 "founder/index.html": ("Startup Founder: Zero to Launch — Dirk Ahlborn", "14 masterclasses on the full founder journey — idea, validation, business model, go-to-market, fundraising. Vault for plan and pitch included. $129, then $20/mo."),
 "culinaris/index.html": (None, "Bite-size daily cooking lessons, streaks and real kitchen missions — from home cook to pro technique. 5 courses, 280+ lessons in 5 languages. First lessons free."),
 "de/ai/index.html": ("KI in der Praxis — Dirk Ahlborn", "13 Masterclasses: Texte, Bilder, Video, Stimme, No-Code-Apps und Automatisierung mit KI — bis zu deinem ersten bezahlten KI-Auftrag. Eigener KI-Workspace inklusive."),
 "de/culinaris/index.html": (None, "Tägliche Kochlektionen in kleinen Häppchen, Streaks und echte Küchenmissionen — bis zur Profitechnik. 5 Kurse, 280+ Lektionen in 5 Sprachen. Erste Lektionen gratis."),
 "de/founder/index.html": ("Startup-Gründer: Von null zum Launch — Dirk Ahlborn", "14 Masterclasses über die komplette Gründerreise — Idee, Validierung, Geschäftsmodell, Go-to-Market, Finanzierung. Inklusive Vault für Businessplan und Pitch."),
 "de/index.html": (None, "Dreißig Jahre Firmen aufbauen — von der Berliner Bank bis zum Hyperloop. Kurse, Keynotes und das Playbook: wie du im KI-Zeitalter startest, aufbaust und verdienst."),
 "es/ai/index.html": ("IA en la Práctica — Dirk Ahlborn", "13 masterclasses: textos, imágenes, vídeo, voz, apps no-code y automatización con IA — hasta tu primer encargo pagado. Incluye tu propio espacio de IA."),
 "es/courses/index.html": (None, "Playbooks, no clases teóricas. IA en la Práctica — y Fundador de Startup: De Cero al Lanzamiento. Impartidos por el fundador de HyperloopTT."),
 "es/culinaris/index.html": (None, "Lecciones diarias de cocina en pequeñas dosis, rachas y misiones reales — hasta la técnica profesional. 5 cursos, 280+ lecciones, 5 idiomas. Primeras lecciones gratis."),
 "es/founder/index.html": ("Fundador de Startup: De Cero al Lanzamiento — Dirk Ahlborn", "14 masterclasses sobre todo el camino del fundador — idea, validación, modelo de negocio, salida al mercado, financiación. Incluye Vault para tu plan y tu pitch."),
 "es/index.html": (None, "Treinta años construyendo empresas — de la banca en Berlín al Hyperloop. Cursos, conferencias y el playbook: cómo empezar, construir y ganar en la era de la IA."),
 "es/speaking/index.html": (None, "Más de 80 escenarios, de Davos a Austin. Conferencias sobre innovación, el futuro del transporte y empresas construidas con multitudes, por el fundador de HyperloopTT."),
 "it/ai/index.html": ("IA in Pratica — Dirk Ahlborn", "13 masterclass: scrittura, immagini, video, voce, app no-code e automazione con l'IA — fino al tuo primo incarico pagato. Include il tuo spazio IA personale."),
 "it/culinaris/index.html": (None, "Lezioni di cucina quotidiane in piccole dosi, streak e missioni vere — fino alla tecnica professionale. 5 corsi, 280+ lezioni in 5 lingue. Prime lezioni gratis."),
 "it/founder/index.html": ("Startup Founder: Da Zero al Lancio — Dirk Ahlborn", "14 masterclass sull'intero percorso del founder — idea, validazione, modello di business, go-to-market, raccolta fondi. Include Vault per business plan e pitch."),
 "pt/ai/index.html": (None, "13 masterclasses: textos, imagens, vídeo, voz, apps no-code e automação com IA — até o seu primeiro trabalho pago. Inclui o seu próprio espaço de IA."),
 "pt/culinaris/index.html": (None, "Aulas diárias de culinária em doses rápidas, ofensivas e missões reais — até a técnica profissional. 5 cursos, 280+ aulas em 5 idiomas. Primeiras aulas grátis."),
 "pt/founder/index.html": ("Fundador de Startup: Do Zero ao Lançamento — Dirk Ahlborn", "14 masterclasses sobre toda a jornada do fundador — ideia, validação, modelo de negócio, go-to-market, captação. Inclui o Vault para seu plano e seu pitch."),
}
PRIVACY_LABEL = {"en":"Privacy","de":"Datenschutz","es":"Privacidad","pt":"Privacidade","it":"Privacy"}
TERMS_LABEL = {"en":"Terms","de":"AGB","es":"Términos","pt":"Termos","it":"Termini"}

FAVICON = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'

def esc(s): return html.escape(s, quote=True)

changed = {}
def save(path, new, old):
    if new != old:
        open(path, "w", encoding="utf-8").write(new); changed[path] = True

for path in sorted(glob.glob("**/*.html", recursive=True)):
    if path.startswith("google") or path == "404.html": continue
    s = open(path, encoding="utf-8").read(); orig = s
    loc = locale_of(path)

    # A. bundle link
    s = s.replace(BUNDLE_OLD, BUNDLE_NEW)

    # B. analytics on every page
    if "/a.js" not in s and "</body>" in s:
        s = s.replace("</body>", '<script defer src="/a.js"></script>\n</body>', 1)

    # C. favicon
    if 'rel="icon"' not in s:
        s = s.replace('<link rel="stylesheet" href="/site.css">', FAVICON + '\n<link rel="stylesheet" href="/site.css">', 1) if '/site.css' in s \
            else s.replace("</title>", "</title>\n" + FAVICON, 1)

    # D. shared footer on site-template pages
    if '<footer class="site">' in s:
        s = re.sub(r'  <footer class="site">.*?</footer>', lambda m: footer_html(loc), s, count=1, flags=re.S)

    # E. sales-page footers (/ai/, /founder/): add Privacy (+Terms) links
    m = re.search(r'<footer>.*?</footer>', s, re.S)
    if m and '/privacy/' not in m.group(0):
        f = m.group(0)
        if '<a href="/terms/">' in f:
            f = f.replace('<a href="/terms/">', '<a href="/privacy/">' + PRIVACY_LABEL[loc] + '</a>\n    <a href="/terms/">', 1)
        else:
            f = f.replace('</footer>', ' · <a href="/privacy/">' + PRIVACY_LABEL[loc] + '</a> · <a href="/terms/">' + TERMS_LABEL[loc] + '</a></footer>', 1)
        s = s[:m.start()] + f + s[m.end():]

    # F. hero fixes on the five homepages
    if path.endswith("index.html") and path.count("/") <= 1 and 'min-height:640px">' in s and "class=\"hero\"" not in s:
        s = s.replace('<section style="position:relative;min-height:640px">', '<section class="hero" style="position:relative;min-height:640px;overflow:hidden">', 1)
        s = s.replace("<div style=\"position:absolute;inset:0;background-image:url(", "<div class=\"heroImg\" style=\"position:absolute;inset:0;background-image:url(", 1)
        s = s.replace('<div style="position:absolute;inset:0;background:linear-gradient(to top, rgba(10,10,9,0.85), transparent 40%);pointer-events:none"></div>',
                      '<div class="heroShade" style="position:absolute;inset:0;background:linear-gradient(to top, rgba(10,10,9,0.85), transparent 40%);pointer-events:none"></div>', 1)
        s = s.replace('<div class="padx" style="position:relative;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:28px;min-height:640px;',
                      '<div class="padx heroCopy" style="position:relative;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:28px;min-height:640px;', 1)
        s = s.replace('<div style="margin-left:auto;max-width:620px;display:flex;flex-direction:column;gap:28px;min-width:0">',
                      '<div class="heroCol" style="margin-left:auto;max-width:700px;display:flex;flex-direction:column;gap:28px;min-width:0">', 1)
        s = s.replace('font-size:clamp(48px,6vw,88px);line-height:1.0;margin:0;letter-spacing:-0.01em;text-wrap:balance;max-width:14ch;',
                      'font-size:clamp(34px,9vw,76px);line-height:1.0;margin:0;letter-spacing:-0.01em;text-wrap:balance;max-width:16ch;', 1)

    # G. Founder Toolkit on localized homepages
    if loc != "en" and path == f"{loc}/index.html" and "TOOLS:start" not in s:
        marker = '  <section class="padx" style="border-top:1px solid rgba(242,239,233,.1);padding:104px 56px">\n'
        i = s.find(marker)
        assert i > 0, path
        s = s[:i] + tools_section(loc) + "\n" + s[i:]

    # H. titles / descriptions
    if path in META:
        t, d = META[path]
        if t:
            s = re.sub(r"<title>.*?</title>", f"<title>{esc(t)}</title>", s, count=1, flags=re.S)
            s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1)+esc(t)+m.group(2), s)
            s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1)+esc(t)+m.group(2), s)
        if d:
            assert len(d) <= 168, (path, len(d))
            for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
                s = re.sub(pat, lambda m: m.group(1)+esc(d)+m.group(2), s)

    # I. speaking pages: one Person entity, lazy video
    if "/speaking/" in "/"+path:
        s = s.replace('"jobTitle":"Keynote Speaker"', '"jobTitle":"Founder & CEO, HyperloopTT"')
        s = s.replace('<iframe src="https://www.youtube.com/embed/', '<iframe loading="lazy" src="https://www.youtube.com/embed/')

    save(path, s, orig)

# J. sitemap lastmod
sm = open("sitemap.xml", encoding="utf-8").read(); o = sm
sm = re.sub(r"\s*<lastmod>[^<]*</lastmod>", "", sm)
sm = re.sub(r"(<loc>[^<]+</loc>)", r"\1<lastmod>" + TODAY + "</lastmod>", sm)
save("sitemap.xml", sm, o)

# K. site.css additions
css = open("site.css", encoding="utf-8").read(); o = css
if "/* FIX1:hero+footer */" not in css:
    css += """
  /* FIX1:hero+footer */
  .hero h1{overflow-wrap:anywhere}
  @media(max-width:700px){
    .hero{min-height:0 !important}
    .heroImg{background-position:center 12% !important}
    .heroShade{background:linear-gradient(to top, rgba(10,10,9,.97) 0%, rgba(10,10,9,.92) 42%, rgba(10,10,9,.25) 70%, transparent) !important}
    .heroCopy{min-height:0 !important;padding:320px 20px 48px !important;justify-content:flex-end !important}
    .heroCol{max-width:100% !important;gap:18px !important}
    .hero h1{overflow-wrap:normal}
  }
  footer.site .footlinks{display:flex;flex-direction:column;gap:12px;min-width:0}
  footer.site .footrow{display:flex;gap:14px 24px;flex-wrap:wrap;align-items:center}
  footer.site .footlbl{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#8A8478}
  @media(max-width:900px){footer.site{flex-direction:column;align-items:flex-start;gap:28px}}
"""
save("site.css", css, o)

# L. favicon + 404
if not os.path.exists("favicon.svg"):
    open("favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0A0A09"/><text x="32" y="44" font-family="Helvetica Neue,Helvetica,Arial,sans-serif" font-size="36" font-weight="700" fill="#E0B15C" text-anchor="middle">D</text></svg>\n')
    changed["favicon.svg"] = True
if not os.path.exists("404.html"):
    open("404.html","w").write("""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found — Dirk Ahlborn</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/site.css"></head>
<body><div style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;padding:40px 20px;text-align:center;background:#0A0A09;color:#F2EFE9">
<a href="/" class="sig" style="font-size:40px">Dirk Ahlborn</a>
<h1 style="font-weight:500;font-size:clamp(28px,5vw,44px);margin:0">That page isn't here.</h1>
<p style="color:#9B958A;max-width:46ch;margin:0;font-size:17px;line-height:1.6">The address may have changed. Everything still lives under the links below.</p>
<div style="display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-top:8px"><a href="/courses/" class="btnGold">Courses</a><a href="/speaking/" class="btnGhost">Speaking</a><a href="/chat/" class="btnGhost">dirk.it AI</a></div>
</div><script defer src="/a.js"></script></body></html>
""")
    changed["404.html"] = True

print(f"{len(changed)} files changed"); print("\n".join(sorted(changed)))
