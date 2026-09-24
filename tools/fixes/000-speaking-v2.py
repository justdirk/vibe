#!/usr/bin/env python3
"""One-time migration: upgrades the speaker-page generator (003) to the v2
"cinematic" layout and the Sep 2026 positioning (a founder who is invited to
speak, not a keynote-speaker listing). Runs before 003 in apply-fixes;
idempotent (each edit is skipped once applied). Safe to delete afterwards."""
assert open("CNAME").read().strip() == "dirk.it"
P = "tools/fixes/003-speaking-i18n.py"
s = open(P, encoding="utf-8").read()
o = s

def rep(a, b):
    global s
    if b in s:
        return
    if a not in s:
        raise SystemExit("000: anchor not found: " + a[:70])
    s = s.replace(a, b, 1)

# --- positioning strings ---
for a, b in [
    ('eyebrow="Keynote speaker · Founder, HyperloopTT"', 'eyebrow="Founder, HyperloopTT · Entrepreneur &amp; educator"'),
    ('eyebrow="Keynote-Speaker · Gründer, HyperloopTT"', 'eyebrow="Gründer, HyperloopTT · Unternehmer &amp; Dozent"'),
    ('eyebrow="Conferenciante · Fundador, HyperloopTT"', 'eyebrow="Fundador, HyperloopTT · Emprendedor y docente"'),
    ('eyebrow="Palestrante · Fundador, HyperloopTT"', 'eyebrow="Fundador, HyperloopTT · Empreendedor e educador"'),
    ('eyebrow="Keynote speaker · Fondatore, HyperloopTT"', 'eyebrow="Fondatore, HyperloopTT · Imprenditore e docente"'),
    ("Keynote speaker on innovation, crowd-powered companies and working in the age of AI. Founder of HyperloopTT, 80+ stages from Davos to Austin. Check availability.",
     "Dirk Ahlborn on stage: innovation, crowd-powered companies and working in the age of AI. Founder of HyperloopTT, 80+ stages from Davos to Austin. Invite Dirk to your event."),
    ("Keynote-Speaker zu Innovation, Crowd-getriebenen Unternehmen und Arbeiten im KI-Zeitalter. Gründer von HyperloopTT, über 80 Bühnen von Davos bis Austin. Verfügbarkeit anfragen.",
     "Dirk Ahlborn auf der Bühne: Innovation, Crowd-getriebene Unternehmen und Arbeiten im KI-Zeitalter. Gründer von HyperloopTT, über 80 Bühnen von Davos bis Austin. Laden Sie Dirk ein."),
    ("Conferenciante sobre innovación, empresas impulsadas por multitudes y el trabajo en la era de la IA. Fundador de HyperloopTT, más de 80 escenarios de Davos a Austin. Consulta disponibilidad.",
     "Dirk Ahlborn en el escenario: innovación, empresas impulsadas por multitudes y el trabajo en la era de la IA. Fundador de HyperloopTT, más de 80 escenarios de Davos a Austin. Invita a Dirk a tu evento."),
    ("Palestrante sobre inovação, empresas movidas por multidões e trabalho na era da IA. Fundador da HyperloopTT, mais de 80 palcos de Davos a Austin. Consulte a disponibilidade.",
     "Dirk Ahlborn no palco: inovação, empresas movidas por multidões e trabalho na era da IA. Fundador da HyperloopTT, mais de 80 palcos de Davos a Austin. Convide o Dirk para o seu evento."),
    ("Keynote speaker su innovazione, aziende costruite con la crowd e lavoro nell'era dell'IA. Fondatore di HyperloopTT, oltre 80 palchi da Davos ad Austin. Verifica la disponibilità.",
     "Dirk Ahlborn sul palco: innovazione, aziende costruite con la crowd e lavoro nell'era dell'IA. Fondatore di HyperloopTT, oltre 80 palchi da Davos ad Austin. Invita Dirk al tuo evento."),
    ('h1="Put a builder on your stage."', 'h1="Put a <em>builder</em> on your stage."'),
    ('h1="Ein Macher auf Ihrer Bühne."', 'h1="Ein <em>Macher</em> auf Ihrer Bühne."'),
    ('h1="Sube a un constructor a tu escenario."', 'h1="Sube a un <em>constructor</em> a tu escenario."'),
    ('h1="Coloque um construtor no seu palco."', 'h1="Coloque um <em>construtor</em> no seu palco."'),
    ('h1="Porta chi costruisce sul tuo palco."', 'h1="Porta <em>chi costruisce</em> sul tuo palco."'),
    ('cta="Book Dirk"', 'cta="Invite Dirk"'),
    ('cta="Dirk buchen"', 'cta="Dirk einladen"'),
    ('cta="Contratar a Dirk"', 'cta="Invitar a Dirk"'),
    ('cta="Contratar Dirk"', 'cta="Convidar Dirk"'),
    ('cta="Prenota Dirk"', 'cta="Invita Dirk"'),
    ('booking="Booking"', 'booking="Invitations"'),
    ('booking="Buchung"', 'booking="Einladungen"'),
    ('booking="Contratación", booking_h="Consulta disponibilidad."', 'booking="Invitaciones", booking_h="Consulta disponibilidad."'),
    ('booking="Contratação"', 'booking="Convites"'),
    ('booking="Prenotazione"', 'booking="Inviti"'),
    (' og="en_US"),', ' og="en_US", cue="Scroll"),'),
    (' og="de_DE"),', ' og="de_DE", cue="Scrollen"),'),
    (' og="es_ES"),', ' og="es_ES", cue="Desliza"),'),
    (' og="pt_BR"),', ' og="pt_BR", cue="Role"),'),
    (' og="it_IT"),', ' og="it_IT", cue="Scorri"),'),
]:
    rep(a, b)

# --- template ---
rep('<link href="https://fonts.googleapis.com/css2?family=Mrs+Saint+Delafield&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@1,9..144,400&family=Mrs+Saint+Delafield&display=swap" rel="stylesheet">\n'
    '<script>document.documentElement.classList.add("js");addEventListener("load",function(){{setTimeout(function(){{if(!window.__rv)document.documentElement.classList.remove("js")}},2500)}})</script>')
rep('"description":"Entrepreneur, educator and keynote speaker on innovation, crowd-powered companies and working in the age of AI. 80+ stages worldwide."',
    '"description":"Entrepreneur and educator, founder of HyperloopTT. Speaks on innovation, crowd-powered companies and working in the age of AI on 80+ stages worldwide."')
rep('''    home = (p + "/") if p else "/"
    return f\'\'\'<!DOCTYPE html>''', '''    home = (p + "/") if p else "/"
    QS = '"\\u201c\\u201d\\u201e\\u00ab\\u00bb'
    q1 = s["q1"].strip(QS); q2 = s["q2"].strip(QS)
    return f\'\'\'<!DOCTYPE html>''')
rep('''        <a href="#watch" class="btnGhost">{s["cta2"]}</a>
      </div>
    </div>
  </section>''', '''        <a href="#watch" class="btnGhost">{s["cta2"]}</a>
      </div>
    </div>
    <div class="cue" aria-hidden="true">{n["cue"]}</div>
  </section>''')
rep('''  <section class="proof">
    <div><b>80+</b><span>{s["p1"]}</span></div>
    <div><b>40+</b><span>{s["p2"]}</span></div>
    <div><b>2</b><span>{s["p3"]}</span></div>
    <div><b>3</b><span>{s["p4"]}</span></div>
  </section>''', '''  <section class="proof">
    <div class="rv"><b data-count="80">80+</b><span>{s["p1"]}</span></div>
    <div class="rv d1"><b data-count="40">40+</b><span>{s["p2"]}</span></div>
    <div class="rv d2"><b data-count="2">2</b><span>{s["p3"]}</span></div>
    <div class="rv d3"><b data-count="3">3</b><span>{s["p4"]}</span></div>
  </section>

  <section class="marquee" aria-label="{s["stages"]}">
    <div class="track">{STAGES}{STAGES_DUP}</div>
  </section>''')
rep('    <div class="watch">', '    <div class="watch rv">')
rep('''    <div class="eyebrow">{s["talks"]}</div>
    <h2 class="h2 mt">{s["talks_h"]}</h2>
    <div class="talks">
      <div class="talk"><h3>{s["t1"]}</h3><p class="promise">{s["t1p"]}</p><ul><li>{s["t1a"]}</li><li>{s["t1b"]}</li><li>{s["t1c"]}</li></ul><div class="for">{s["t1f"]}</div></div>
      <div class="talk"><h3>{s["t2"]}</h3><p class="promise">{s["t2p"]}</p><ul><li>{s["t2a"]}</li><li>{s["t2b"]}</li><li>{s["t2c"]}</li></ul><div class="for">{s["t2f"]}</div></div>
      <div class="talk"><h3>{s["t3"]}</h3><p class="promise">{s["t3p"]}</p><ul><li>{s["t3a"]}</li><li>{s["t3b"]}</li><li>{s["t3c"]}</li></ul><div class="for">{s["t3f"]}</div></div>
    </div>''', '''    <div class="eyebrow rv">{s["talks"]}</div>
    <h2 class="h2 mt rv">{s["talks_h"]}</h2>
    <div class="tlist">
      <article class="trow rv"><div class="tnum">01</div><div class="tmain"><h3>{s["t1"]}</h3><p class="promise">{s["t1p"]}</p><div class="for">{s["t1f"]}</div></div><ul><li>{s["t1a"]}</li><li>{s["t1b"]}</li><li>{s["t1c"]}</li></ul></article>
      <article class="trow rv"><div class="tnum">02</div><div class="tmain"><h3>{s["t2"]}</h3><p class="promise">{s["t2p"]}</p><div class="for">{s["t2f"]}</div></div><ul><li>{s["t2a"]}</li><li>{s["t2b"]}</li><li>{s["t2c"]}</li></ul></article>
      <article class="trow rv"><div class="tnum">03</div><div class="tmain"><h3>{s["t3"]}</h3><p class="promise">{s["t3p"]}</p><div class="for">{s["t3f"]}</div></div><ul><li>{s["t3a"]}</li><li>{s["t3b"]}</li><li>{s["t3c"]}</li></ul></article>
    </div>''')
rep('''    <div class="eyebrow">{s["stages"]}</div>
    <div class="stages">
      <span>World Economic Forum</span><span>SXSW</span><span>CES</span><span>DLD</span><span>Pioneers</span><span>Nikkei Forum</span><span>Open Innovation Forum</span>
    </div>
    <div class="quotes">
      <blockquote><p>{s["q1"]}</p><cite>{s["q1c"]}</cite></blockquote>
      <blockquote><p>{s["q2"]}</p><cite>{s["q2c"]}</cite></blockquote>
    </div>''', '''    <div class="pull rv">
      <blockquote><p>{q1}</p><cite>{s["q1c"]}</cite></blockquote>
      <div class="rule"></div>
      <blockquote class="second"><p>{q2}</p><cite>{s["q2c"]}</cite></blockquote>
    </div>''')
rep('''    <div class="eyebrow">{s["formats"]}</div>
    <h2 class="h2 mt">{s["formats_h"]}</h2>
    <div class="formats">
      <div><b>{s["f1"]}</b><span>{s["f1p"]}</span></div>
      <div><b>{s["f2"]}</b><span>{s["f2p"]}</span></div>
      <div><b>{s["f3"]}</b><span>{s["f3p"]}</span></div>
      <div><b>{s["f4"]}</b><span>{s["f4p"]}</span></div>
    </div>''', '''    <div class="eyebrow rv">{s["formats"]}</div>
    <h2 class="h2 mt rv">{s["formats_h"]}</h2>
    <div class="formats">
      <div class="rv"><i>i.</i><b>{s["f1"]}</b><span>{s["f1p"]}</span></div>
      <div class="rv d1"><i>ii.</i><b>{s["f2"]}</b><span>{s["f2p"]}</span></div>
      <div class="rv d2"><i>iii.</i><b>{s["f3"]}</b><span>{s["f3p"]}</span></div>
      <div class="rv d3"><i>iv.</i><b>{s["f4"]}</b><span>{s["f4p"]}</span></div>
    </div>''')
rep('''    <div class="eyebrow">{s["kit"]}</div>
    <div class="kit">''', '''    <div class="eyebrow rv">{s["kit"]}</div>
    <div class="kit rv">''')
rep('''  <section class="wrap" id="inquire" style="border-top:1px solid rgba(242,239,233,.1)">
    <div class="inq">''', '''  <div class="inqWrap"><section class="wrap" id="inquire">
    <div class="inq rv">''')
rep('''      </form>
    </div>
  </section>''', '''      </form>
    </div>
  </section></div>''')
# don't advertise a no-fee path in the budget list
rep('<option>{s["bu4"]}</option><option>{s["bu5"]}</option><option>{s["bu6"]}</option>', '<option>{s["bu4"]}</option><option>{s["bu6"]}</option>')
rep('def langbar(loc):', '''_ST = ["World Economic Forum", "SXSW", "CES", "DLD", "Pioneers", "Nikkei Forum", "Open Innovation Forum"]
STAGES = "".join(f"<span>{x}</span>" for x in _ST)
STAGES_DUP = "".join(f'<span aria-hidden="true">{x}</span>' for x in _ST)

def langbar(loc):''')

if s != o:
    open(P, "w", encoding="utf-8").write(s)
    print("000: 003 generator upgraded to v2")
else:
    print("000: already v2")
